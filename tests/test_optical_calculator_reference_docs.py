"""Docs and example checks for optical calculator reference cases."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_optical_calculator_reference_docs_exist_and_bound_claims():
    en = ROOT / "docs" / "optical_calculator_reference_cases.md"
    zh = ROOT / "docs" / "optical_calculator_reference_cases.zh-CN.md"
    assert en.exists()
    assert zh.exists()
    text = en.read_text(encoding="utf-8") + "\n" + zh.read_text(encoding="utf-8")
    for phrase in [
        "R = |(n0 - ns) / (n0 + ns)|^2",
        "d = lambda / (4 * n_coating)",
        "z_R = pi * w0^2 / lambda",
        "1/f = 1/s + 1/s'",
        "V = (2*pi / lambda) * thickness",
        "No production-grade physical validation",
        "No formal convergence proof",
        "不声明生产级物理验证",
        "不声明形式化收敛证明",
    ]:
        assert phrase in text


def test_optics_reference_case_examples_exist_and_remain_preview_only():
    root = ROOT / "examples" / "optics_reference_cases"
    assert (root / "README.md").exists()
    cases = [
        "thin_film_single_interface_air_glass.json",
        "thin_film_quarter_wave_ar_550nm.json",
        "gaussian_beam_rayleigh_range.json",
        "paraxial_thin_lens_1to1.json",
        "waveguide_v_number_sanity.json",
    ]
    for name in cases:
        path = root / name
        assert path.exists()
        payload = json.loads(path.read_text(encoding="utf-8"))
        assert payload["preview_only"] is True
        assert payload["production_grade_validation_claimed"] is False
        assert payload["formal_convergence_proof_claimed"] is False
        assert payload["formula"]
