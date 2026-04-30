"""CSV sanity checks for local/manual Meep diagnostics."""

from __future__ import annotations

import csv
import math
from dataclasses import asdict, dataclass, field
from pathlib import Path


@dataclass(slots=True)
class CsvSanityResult:
    """Result of a lightweight numeric CSV sanity check."""

    ok: bool
    rows_checked: int = 0
    errors: list[str] = field(default_factory=list)

    def to_dict(self) -> dict:
        return asdict(self)


def check_csv_numeric_sanity(path: Path) -> CsvSanityResult:
    """Check that a spectrum CSV has finite numeric wavelength and flux values.

    This helper is intentionally not part of the default execution success
    contract. It is used by manual/local hardening scripts to inspect generated
    research-preview artifacts.
    """
    csv_path = Path(path)
    if not csv_path.exists():
        return CsvSanityResult(ok=False, errors=[f"CSV file does not exist: {csv_path}"])

    try:
        with csv_path.open(newline="", encoding="utf-8") as handle:
            reader = csv.DictReader(handle)
            if not reader.fieldnames:
                return CsvSanityResult(ok=False, errors=["CSV file is missing a header"])

            wavelength_field = _find_column(reader.fieldnames, ["wavelength_nm"])
            flux_field = _find_column(
                reader.fieldnames,
                ["particle_induced_flux_relative", "scattering_flux", "scattering_flux_relative", "flux"],
            )
            errors: list[str] = []
            rows_checked = 0
            for row_number, row in enumerate(reader, start=2):
                rows_checked += 1
                _check_finite_number(row.get(wavelength_field), f"{wavelength_field} row {row_number}", errors)
                _check_finite_number(row.get(flux_field), f"{flux_field} row {row_number}", errors)
            if rows_checked == 0:
                errors.append("CSV file has no data rows")
            return CsvSanityResult(ok=(not errors), rows_checked=rows_checked, errors=errors)
    except (OSError, ValueError, csv.Error) as exc:
        return CsvSanityResult(ok=False, errors=[f"Could not read CSV file: {exc}"])


def _find_column(fieldnames: list[str], candidates: list[str]) -> str:
    for candidate in candidates:
        if candidate in fieldnames:
            return candidate
    # Let callers see a useful failure tied to an actual requested column name.
    raise ValueError(f"CSV header is missing one of {candidates}; found {fieldnames}")


def _check_finite_number(raw_value: str | None, label: str, errors: list[str]) -> None:
    if raw_value is None or raw_value == "":
        errors.append(f"{label} is missing")
        return
    try:
        value = float(raw_value)
    except ValueError:
        errors.append(f"{label} is not numeric: {raw_value!r}")
        return
    if math.isnan(value):
        errors.append(f"{label} is NaN")
    elif math.isinf(value):
        errors.append(f"{label} is Inf")
