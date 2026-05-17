from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_open_source_optical_design_ecosystem_doc_tracks_current_and_future_tools():
    path = ROOT / "docs" / "open_source_optical_design_ecosystem.md"
    assert path.exists()
    text = path.read_text(encoding="utf-8")
    for tool in ["Meep", "MPB", "Gmsh", "Elmer", "Optiland"]:
        assert tool in text
    for candidate in ["TorchOptics", "AOtools", "Simphony", "PyFocus"]:
        assert candidate in text
    for commercial in ["Zemax", "Lumerical", "COMSOL", "Ansys"]:
        assert commercial in text
    assert "not default" in text
    assert "No external solver is executed by default." in text
