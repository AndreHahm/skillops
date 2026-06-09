"""Final Phase 2 closure guardrails."""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "reports" / "phase-2-final-review.md"
TEXT_ROOTS = [
    ROOT / ".github",
    ROOT / "docs",
    ROOT / "evals",
    ROOT / "llm-wiki",
    ROOT / "packages",
    ROOT / "registry",
    ROOT / "schemas",
    ROOT / "tests",
]
TEXT_SUFFIXES = {".json", ".md", ".py", ".toml", ".yaml", ".yml"}
REQUIRED_REPORT_HEADINGS = [
    "# Phase 2 Final Review",
    "## Summary",
    "## Reviewed Scope",
    "## Package Coverage",
    "## Acceptance Criteria Review",
    "## Consistency Findings",
    "## Drift Findings",
    "## Tests and Documentation Findings",
    "## Fixes Applied",
    "## Remaining Limitations",
    "## Recommended Follow-Up",
    "## Phase 2 Closure Recommendation",
]


def _iter_text_files() -> list[Path]:
    files = [ROOT / "README.md", ROOT / "justfile", ROOT / "pyproject.toml", ROOT / "mkdocs.yml"]
    for root in TEXT_ROOTS:
        files.extend(path for path in root.rglob("*") if path.is_file())
    return sorted(
        {path for path in files if path.suffix in TEXT_SUFFIXES or path.name == "justfile"}
    )


def test_phase2_final_review_report_exists_with_required_sections() -> None:
    assert REPORT.is_file(), "Phase 2 final review report is missing."
    content = REPORT.read_text(encoding="utf-8")
    for heading in REQUIRED_REPORT_HEADINGS:
        assert heading in content, f"Missing report heading: {heading}"


def test_phase2_text_files_do_not_reintroduce_python_312_drift() -> None:
    for path in _iter_text_files():
        content = path.read_text(encoding="utf-8")
        stale_python = "Python " + "3." + "12"
        stale_ci = "python-version: " + chr(34) + "3." + "12" + chr(34)
        assert stale_python not in content, f"Lower Python drift found in {path}"
        assert stale_ci not in content, f"Lower Python CI drift found in {path}"


def test_phase2_final_docs_reference_ci_smoke_gate_in_navigation() -> None:
    mkdocs = (ROOT / "mkdocs.yml").read_text(encoding="utf-8")
    assert "CI Smoke Gate: evaluation/ci-gate.md" in mkdocs
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    assert "skillops eval --smoke" in readme
    assert "full/live CI evaluation beyond the deterministic smoke gate" in readme
