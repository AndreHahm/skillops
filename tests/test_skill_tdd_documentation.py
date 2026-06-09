from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

REQUIRED_DOCS = [
    ROOT / "docs" / "evaluation" / "skill-tdd.md",
    ROOT / "docs" / "evaluation" / "review-gates.md",
    ROOT / "docs" / "evaluation" / "overview.md",
    ROOT / "docs" / "evaluation" / "ci-gate.md",
    ROOT / "docs" / "evaluation" / "golden-sets.md",
    ROOT / "docs" / "evaluation" / "promptfoo.md",
    ROOT / "docs" / "evaluation" / "deepeval.md",
    ROOT / "llm-wiki" / "concepts" / "skill-tdd.md",
    ROOT / "llm-wiki" / "concepts" / "evaluation.md",
]

SKILL_TDD_DOC = ROOT / "docs" / "evaluation" / "skill-tdd.md"
REVIEW_GATES_DOC = ROOT / "docs" / "evaluation" / "review-gates.md"
OVERVIEW_DOC = ROOT / "docs" / "evaluation" / "overview.md"

DOC_SCOPE_ROOTS = [
    ROOT / "README.md",
    ROOT / "docs",
    ROOT / "evals",
    ROOT / "llm-wiki",
]

FORBIDDEN_OVERCLAIMS = [
    "production traces are implemented",
    "production observability is implemented",
    "langfuse is integrated",
    "langfuse integration is implemented",
    "phoenix is integrated",
    "phoenix integration is implemented",
    "dependency graph analysis is implemented",
    "marketplace behavior is implemented",
    "self-improvement automation is implemented",
    "automatic skill patching is implemented",
    "promptfoo execution is mandatory",
    "deepeval live scoring is mandatory",
]

REQUIRED_NOT_IMPLEMENTED_STATEMENTS = [
    "production observability is planned for phase 4",
    "marketplace behavior is planned for phase 5",
    "self-improvement automation",
    "not implemented in phase 2",
]

SECRET_PATTERNS = [
    re.compile(r"sk-[a-z0-9]{20,}", re.IGNORECASE),
    re.compile(r"ghp_[a-z0-9]{20,}", re.IGNORECASE),
    re.compile(r"xox[baprs]-[a-z0-9-]{20,}", re.IGNORECASE),
    re.compile(r"aws_secret_access_key\s*=\s*['\"]?[a-z0-9/+=]{20,}", re.IGNORECASE),
]

# noinspection RegExpUnnecessaryNonCapturingGroup
LOCAL_USER_PATH_PATTERN = re.compile(
    r"(?:[A-Za-z]:\\Users\\[A-Za-z0-9._\- ]+|/(?:Users|home)/[A-Za-z0-9._-]+)"
)


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def markdown_files() -> list[Path]:
    files: list[Path] = []
    for root in DOC_SCOPE_ROOTS:
        if root.is_file():
            files.append(root)
        else:
            files.extend(sorted(root.rglob("*.md")))
    return files


def normalized(path: Path) -> str:
    return read(path).lower()


def test_required_skill_tdd_documentation_files_exist() -> None:
    for path in REQUIRED_DOCS:
        assert path.is_file(), f"Required documentation file is missing: {path}"


def test_skill_tdd_doc_includes_required_workflow_terms() -> None:
    content = normalized(SKILL_TDD_DOC)
    for phrase in [
        "eval case first",
        "skill update",
        "local validation",
        "scenario eval",
        "review",
        "regression protection",
    ]:
        assert phrase in content, f"Required workflow term {phrase!r} not found in {SKILL_TDD_DOC}"


def test_skill_tdd_doc_connects_evaluation_layers() -> None:
    content = normalized(SKILL_TDD_DOC)
    for phrase in [
        "golden sets are canonical scenario assets",
        "promptfoo configs provide deterministic scenario-level assertions",
        "deepeval tests provide python/pytest-style evaluation skeletons",
        "review gates",
    ]:
        msg = f"Required evaluation layer connection phrase {phrase!r} not found in {SKILL_TDD_DOC}"
        assert phrase in content, msg


def test_review_gate_doc_includes_practical_checklist_and_risk_terms() -> None:
    content = normalized(REVIEW_GATES_DOC)
    for phrase in [
        "## skill-tdd review checklist",
        "### scenario coverage",
        "### golden set quality",
        "### promptfoo alignment",
        "### deepeval alignment",
        "### skill scope",
        "### safety and permissions",
        "### documentation accuracy",
        "### regression risk",
        "### final recommendation",
        "overfitting",
        "scope creep",
        "unsafe tool permission expansion",
        "broad shell access",
    ]:
        msg = f"Required checklist/risk term {phrase!r} not found in {REVIEW_GATES_DOC}"
        assert phrase in content, msg


def test_overview_documents_layer_status_without_ci_gate_overclaiming() -> None:
    content = normalized(OVERVIEW_DOC)
    for phrase in [
        "static validation",
        "golden scenario tests",
        "promptfoo configuration",
        "deepeval test skeletons",
        "review gate",
        "ci smoke gate",
        "not implemented by this package",
    ]:
        msg = f"Required overview phrase {phrase!r} not found in {OVERVIEW_DOC}"
        assert phrase in content, msg


def test_docs_state_later_phase_boundaries() -> None:
    combined = "\n".join(normalized(path) for path in REQUIRED_DOCS)
    for phrase in REQUIRED_NOT_IMPLEMENTED_STATEMENTS:
        assert phrase in combined
    msg = "Required phase boundary statement 'automatic skill patching' not found in combined docs"
    assert "automatic skill patching" in combined, msg


def test_docs_do_not_overclaim_future_systems() -> None:
    for path in markdown_files():
        content = normalized(path)
        for claim in FORBIDDEN_OVERCLAIMS:
            assert claim not in content, f"{claim!r} found in {path}"


def test_skill_tdd_docs_do_not_contain_real_looking_secrets_or_local_paths() -> None:
    for path in markdown_files():
        content = read(path)
        for pattern in SECRET_PATTERNS:
            match = pattern.search(content)
            assert match is None, f"Secret-like value {match.group(0)!r} found in {path}"
        match = LOCAL_USER_PATH_PATTERN.search(content)
        assert match is None, f"Local user path {match.group(0)!r} found in {path}"


def test_skill_tdd_docs_use_current_project_name() -> None:
    stale_name = "agent" + "-skillops"
    for path in markdown_files():
        msg = f"Stale project name {stale_name!r} found in {path}"
        assert stale_name not in normalized(path), msg
