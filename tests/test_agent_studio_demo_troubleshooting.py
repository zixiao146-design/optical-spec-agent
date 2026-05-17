from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_agent_studio_demo_troubleshooting_covers_common_local_failures():
    path = ROOT / "docs" / "agent_studio_demo_troubleshooting.md"
    assert path.exists()
    text = path.read_text(encoding="utf-8")
    required = [
        "API Not Running",
        "./scripts/bootstrap_demo_env.sh",
        "./scripts/run_quickstart_demo.sh",
        "port 8000",
        "port 5173",
        "Playwright Browser Download Fails",
        "local Chrome fallback",
        "API Disconnected Demo Mode",
        "CORS Issue",
        "Stale frontend/dist",
        "node_modules Not Committed",
        "No token needed",
    ]
    for phrase in required:
        assert phrase in text
