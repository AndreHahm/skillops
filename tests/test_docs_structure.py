from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
README = ROOT / "README.md"
DOCS_DIR = ROOT / "docs"
MKDOCS = ROOT / "mkdocs.yml"

REQUIRED_README_HEADINGS = [
    "# skillops",
    "## What is SkillOps?",
    "## Why this project exists",
    "## Current Phase 1 MVP Scope",
    "## What is implemented now",
    "## What is intentionally not implemented yet",
    "## Repository Structure",
    "## Quickstart",
    "## CLI Usage",
    "## Core Concepts",
    "## Core Skills",
    "## Agent Setup",
    "## Documentation and LLM-Wiki",
    "## Roadmap",
    "## Contributing",
    "## Security",
    "## License",
]

REQUIRED_DOCS_PAGES = [
    DOCS_DIR / "index.md",
    DOCS_DIR / "architecture" / "overview.md",
    DOCS_DIR / "governance" / "skill-lifecycle.md",
    DOCS_DIR / "governance" / "risk-tiers.md",
    DOCS_DIR / "governance" / "ownership.md",
    DOCS_DIR / "skill-authoring" / "skill-manifest.md",
    DOCS_DIR / "skill-authoring" / "skill-testing.md",
    DOCS_DIR / "skill-authoring" / "skill-maintenance.md",
    DOCS_DIR / "roadmap" / "phase-1-foundation.md",
]

FUTURE_FEATURE_TERMS = [
    "marketplace",
    "dependency graph",
    "promptfoo",
    "deepeval",
    "langfuse",
    "phoenix",
    "self-improvement",
]

FUTURE_QUALIFIERS = [
    "future",
    "planned",
    "later",
    "out of scope",
    "not implemented",
    "does not implement",
    "does not include",
    "intentionally not implemented",
    "not current implemented",
    "before introducing",
    "rejected",
]


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def markdown_files(paths: list[Path]) -> list[Path]:
    files: list[Path] = []
    for path in paths:
        if path.is_dir():
            files.extend(sorted(path.rglob("*.md")))
        else:
            files.append(path)
    return files


def assert_future_terms_are_qualified(text: str) -> None:
    paragraphs = [paragraph.lower() for paragraph in text.split("\n\n")]
    for term in FUTURE_FEATURE_TERMS:
        for paragraph in paragraphs:
            if term in paragraph:
                assert any(qualifier in paragraph for qualifier in FUTURE_QUALIFIERS), term


def test_readme_exists_and_contains_required_headings() -> None:
    assert README.exists()
    content = read(README)
    for heading in REQUIRED_README_HEADINGS:
        assert heading in content


def test_readme_uses_current_project_name_only() -> None:
    content = read(README).lower()
    assert "skillops" in content
    assert "agent-skillops" not in content


def test_mkdocs_exists_and_is_valid_yaml() -> None:
    assert MKDOCS.exists()
    data = yaml.safe_load(read(MKDOCS))
    assert data["site_name"] == "skillops"
    assert data["docs_dir"] == "docs"
    assert "nav" in data


def test_required_docs_pages_exist_and_have_h1() -> None:
    for path in REQUIRED_DOCS_PAGES:
        assert path.exists(), path
        assert "\n# " in f"\n{read(path)}", path


def test_docs_do_not_contain_stale_or_placeholder_terms() -> None:
    for path in markdown_files([README, DOCS_DIR]):
        content = read(path)
        assert "TODO" not in content, path
        assert "agent-skillops" not in content, path


def test_docs_do_not_introduce_lower_python_versions() -> None:
    disallowed_versions = [f"3.{minor}" for minor in range(13)]
    for path in markdown_files([README, DOCS_DIR]):
        content = read(path).lower()
        for version in disallowed_versions:
            assert f"python {version}" not in content, path
            assert f">={version}" not in content, path


def test_readme_does_not_claim_future_features_are_implemented() -> None:
    assert_future_terms_are_qualified(read(README))
