"""Tests for mesh-resolution sanity diagnostics."""

from __future__ import annotations

import pytest

from optical_spec_agent.analysis import analyze_mesh_resolution


def test_mesh_sanity_flags_under_resolved_gap():
    result = analyze_mesh_resolution(
        resolution_px_per_um=12,
        gap_thickness_nm=5,
        particle_radius_nm=40,
        film_thickness_nm=100,
    )

    assert result.grid_size_nm == pytest.approx(83.3333333333)
    assert result.gap_cells == pytest.approx(0.06)
    assert result.recommended_resolution_for_gap == pytest.approx(1000.0)
    assert result.physically_resolved is False
    assert "gap is under-resolved" in result.warnings


def test_mesh_sanity_accepts_five_gap_cells():
    result = analyze_mesh_resolution(
        resolution_px_per_um=1000,
        gap_thickness_nm=5,
        particle_radius_nm=40,
        film_thickness_nm=100,
    )

    assert result.grid_size_nm == pytest.approx(1.0)
    assert result.gap_cells == pytest.approx(5.0)
    assert result.physically_resolved is True
    assert "gap is under-resolved" not in result.warnings
