from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SWITCHER = ROOT / "frontend" / "src" / "components" / "LanguageSwitcher.tsx"


def test_language_switcher_uses_local_state_and_no_external_operations():
    assert SWITCHER.exists()
    text = SWITCHER.read_text(encoding="utf-8")
    assert "English" in (ROOT / "frontend" / "src" / "i18n" / "en.ts").read_text(encoding="utf-8")
    assert "中文" in text
    assert "setLanguage" in text
    assert "aria-pressed" in text
    assert "localStorage" in (ROOT / "frontend" / "src" / "i18n" / "useI18n.tsx").read_text(encoding="utf-8")
    forbidden = [
        "fetch(",
        "twine upload",
        "gh release create",
        "git tag",
        "Upload to PyPI",
        "Upload to TestPyPI",
        "Create release",
    ]
    for phrase in forbidden:
        assert phrase not in text
