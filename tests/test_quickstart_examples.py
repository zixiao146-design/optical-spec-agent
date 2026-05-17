import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_quickstart_examples_exist_and_are_offline_preview_fixtures():
    examples = ROOT / "examples" / "quickstart"
    readme = examples / "README.md"
    spec = examples / "nanoparticle_demo_spec.json"
    workflow = examples / "quickstart_workflow_request.json"
    assert readme.exists()
    assert spec.exists()
    assert workflow.exists()
    text = readme.read_text(encoding="utf-8")
    for phrase in [
        "No network access is required",
        "No solver is executed",
        "No external LLM is called",
        "No PyPI/TestPyPI upload is performed",
        "No tag or GitHub release is created",
    ]:
        assert phrase in text
    for path in [spec, workflow]:
        payload = json.loads(path.read_text(encoding="utf-8"))
        assert payload["safety"]["no_network"] is True
        assert payload["safety"]["external_solver_executed"] is False
        assert payload["safety"]["external_llm_required"] is False
        assert payload["safety"]["production_grade_validation_claimed"] is False
        assert payload["safety"]["formal_convergence_proof_claimed"] is False
