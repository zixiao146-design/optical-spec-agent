"""Mesh-resolution sanity checks for local/manual Meep diagnostics."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field


@dataclass(slots=True)
class MeshSanityResult:
    """JSON-serializable mesh sanity summary for a simple core geometry."""

    resolution_px_per_um: float
    grid_size_um: float
    grid_size_nm: float
    gap_thickness_nm: float
    gap_cells: float
    particle_radius_nm: float
    particle_radius_cells: float
    film_thickness_nm: float
    film_thickness_cells: float
    min_recommended_gap_cells: float
    recommended_resolution_for_gap: float
    warnings: list[str] = field(default_factory=list)
    physically_resolved: bool = False

    def to_dict(self) -> dict:
        return asdict(self)


def analyze_mesh_resolution(
    resolution_px_per_um: float,
    gap_thickness_nm: float,
    particle_radius_nm: float,
    film_thickness_nm: float,
    min_gap_cells: float = 5.0,
) -> MeshSanityResult:
    """Analyze whether the smallest gap is represented by enough grid cells.

    This is a conservative diagnostic helper, not a substitute for a true
    convergence study.
    """
    if resolution_px_per_um <= 0:
        raise ValueError("resolution_px_per_um must be positive")
    if gap_thickness_nm <= 0:
        raise ValueError("gap_thickness_nm must be positive")
    if particle_radius_nm <= 0:
        raise ValueError("particle_radius_nm must be positive")
    if film_thickness_nm <= 0:
        raise ValueError("film_thickness_nm must be positive")
    if min_gap_cells <= 0:
        raise ValueError("min_gap_cells must be positive")

    grid_size_um = 1.0 / resolution_px_per_um
    grid_size_nm = 1000.0 / resolution_px_per_um
    gap_cells = gap_thickness_nm / grid_size_nm
    particle_radius_cells = particle_radius_nm / grid_size_nm
    film_thickness_cells = film_thickness_nm / grid_size_nm
    recommended_resolution_for_gap = min_gap_cells * 1000.0 / gap_thickness_nm

    warnings: list[str] = []
    if gap_cells < min_gap_cells:
        warnings.append("gap is under-resolved")
    if particle_radius_cells < 3.0:
        warnings.append("particle radius has very few grid cells")
    if film_thickness_cells < 3.0:
        warnings.append("film thickness has very few grid cells")

    physically_resolved = gap_cells >= min_gap_cells
    return MeshSanityResult(
        resolution_px_per_um=resolution_px_per_um,
        grid_size_um=grid_size_um,
        grid_size_nm=grid_size_nm,
        gap_thickness_nm=gap_thickness_nm,
        gap_cells=gap_cells,
        particle_radius_nm=particle_radius_nm,
        particle_radius_cells=particle_radius_cells,
        film_thickness_nm=film_thickness_nm,
        film_thickness_cells=film_thickness_cells,
        min_recommended_gap_cells=min_gap_cells,
        recommended_resolution_for_gap=recommended_resolution_for_gap,
        warnings=warnings,
        physically_resolved=physically_resolved,
    )
