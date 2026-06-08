from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LLM_WIKI = ROOT / "llm-wiki"

REQUIRED_PAGES = [
    LLM_WIKI / "index.md",
    LLM_WIKI / "concepts" / "skillops.md",
    LLM_WIKI / "concepts" / "skill.md",
    LLM_WIKI / "concepts" / "registry.md",
    LLM_WIKI / "concepts" / "health-score.md",
    LLM_WIKI / "decisions" / "ADR-0001-monorepo-foundation.md",
    LLM_WIKI / "glossary" / "glossary.md",
    LLM_WIKI / "playbooks" / "skill-maintenance-playbook.md",
]

REQUIRED_GLOSSARY_TERMS = [
    "Agent",
    "Agent Setup",
    "AGENTS.md",
    "CLAUDE.md",
    "Codex",
    "Claude Code",
    "Core Skill",
    "Dependency",
    "Evaluation",
    "Health Report",
    "Health Score",
    "Hook",
    "LLM-Wiki",
    "Manifest",
    "MCP Server",
    "Registry",
    "Risk Tier",
    "Skill",
    "SkillOps",
    "Status",
    "Validation",
]

REQUIRED_ADR_HEADINGS = [
    "## Status",
    "## Context",
    "## Decision",
    "## Consequences",
    "## Alternatives Considered",
    "## Follow-up Work",
]

REQUIRED_PLAYBOOK_COMMANDS = [
    "uv run skillops validate",
    "uv run skillops health --no-write",
    "uv run skillops list",
    "uv run skillops inspect skill-registry-maintenance",
    "uv run pytest",
    "uv run ruff check .",
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
    "not current implemented",
    "before introducing",
    "rejected",
]


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def assert_future_terms_are_qualified(text: str) -> None:
    paragraphs = [paragraph.lower() for paragraph in text.split("\n\n")]
    for term in FUTURE_FEATURE_TERMS:
        for paragraph in paragraphs:
            if term in paragraph:
                assert any(qualifier in paragraph for qualifier in FUTURE_QUALIFIERS), term


def test_required_llm_wiki_pages_exist_and_have_h1() -> None:
    for path in REQUIRED_PAGES:
        assert path.exists(), path
        assert "\n# " in f"\n{read(path)}", path


def test_llm_wiki_pages_do_not_contain_stale_or_placeholder_terms() -> None:
    for path in sorted(LLM_WIKI.rglob("*.md")):
        content = read(path)
        assert "TODO" not in content, path
        assert "agent-skillops" not in content, path


def test_glossary_contains_required_terms() -> None:
    content = read(LLM_WIKI / "glossary" / "glossary.md")
    for term in REQUIRED_GLOSSARY_TERMS:
        assert f"## {term}" in content


def test_adr_0001_has_required_structure_and_decision_text() -> None:
    content = read(LLM_WIKI / "decisions" / "ADR-0001-monorepo-foundation.md")
    for heading in REQUIRED_ADR_HEADINGS:
        assert heading in content
    assert "Accepted" in content
    assert (
        "We start with a clean public monorepo to establish shared schemas, registry validation, "
        "documentation, agent setup, and core SkillOps workflows before introducing federation, "
        "marketplace mechanics, observability, and self-improvement automation."
    ) in content


def test_skill_maintenance_playbook_contains_required_commands() -> None:
    content = read(LLM_WIKI / "playbooks" / "skill-maintenance-playbook.md")
    for command in REQUIRED_PLAYBOOK_COMMANDS:
        assert command in content


def test_llm_wiki_does_not_claim_future_systems_are_implemented() -> None:
    for path in sorted(LLM_WIKI.rglob("*.md")):
        assert_future_terms_are_qualified(read(path))
