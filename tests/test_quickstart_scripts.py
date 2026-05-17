from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_quickstart_scripts_are_local_only_and_guided():
    bootstrap = ROOT / "scripts" / "bootstrap_demo_env.sh"
    run = ROOT / "scripts" / "run_quickstart_demo.sh"
    assert bootstrap.exists()
    assert run.exists()
    bootstrap_text = bootstrap.read_text(encoding="utf-8")
    run_text = run.read_text(encoding="utf-8")
    combined = bootstrap_text + "\n" + run_text
    required = [
        "python3.11",
        'pip install -e "$ROOT_DIR[test]"',
        "source /tmp/osa-agent-studio-demo/bin/activate",
        "Quickstart dependencies are not ready.",
        "./scripts/bootstrap_demo_env.sh",
        "python -m uvicorn optical_spec_agent.api.app:app",
        "npm run dev",
        "OSA_QUICKSTART_NO_HOLD",
        "OSA_QUICKSTART_WITH_VISUAL",
        "NO SOLVER EXECUTION PERFORMED",
        "NO EXTERNAL LLM CALLED",
        "NO UPLOAD PERFORMED",
        "NO TAG CREATED",
        "NO RELEASE CREATED",
    ]
    for phrase in required:
        assert phrase in combined
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
        assert phrase not in combined
