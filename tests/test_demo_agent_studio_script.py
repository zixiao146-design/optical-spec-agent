from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_demo_agent_studio_script_is_local_only_and_safe():
    path = ROOT / "scripts" / "demo_agent_studio.sh"
    assert path.exists()
    text = path.read_text(encoding="utf-8")
    required = [
        "python -m uvicorn optical_spec_agent.api.app:app",
        "npm run dev",
        "trap cleanup EXIT",
        "NO SOLVER EXECUTION PERFORMED",
        "NO EXTERNAL LLM CALLED",
        "NO PROPRIETARY SOLVER REQUIRED",
        "NO UPLOAD PERFORMED",
        "NO TAG CREATED",
        "NO RELEASE CREATED",
        "scripts/smoke_agent_api.sh",
        "scripts/smoke_frontend_mvp.sh",
        "./scripts/bootstrap_demo_env.sh",
        "./scripts/run_quickstart_demo.sh",
    ]
    for phrase in required:
        assert phrase in text
    forbidden = [
        "twine upload",
        "gh release create",
        "git tag",
        "TESTPYPI_TOKEN",
        "PYPI_TOKEN",
        "GH_TOKEN",
        "GITHUB_TOKEN",
    ]
    for phrase in forbidden:
        assert phrase not in text
