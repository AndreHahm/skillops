"""Validation helpers for SkillOps registries and manifests."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from skillops_core.models import ModelValidationError, Registry, SkillManifest, ValidationReport

try:
    import yaml
except ModuleNotFoundError:  # pragma: no cover - used only when PyYAML is unavailable locally.
    yaml = None  # type: ignore


def _display_path(path: Path, repo_root: Path) -> str:
    try:
        return str(path.relative_to(repo_root))
    except ValueError:
        return str(path)


def _parse_scalar(value: str) -> Any:
    value = value.strip()
    if value in {"null", "~"}:
        return None
    if value == "[]":
        return []
    if value in {"true", "false"}:
        return value == "true"
    try:
        return int(value)
    except ValueError:
        return value.strip("\"'")


def _simple_yaml_load(text: str) -> dict[str, Any]:
    result: dict[str, Any] = {}
    stack: list[tuple[int, Any]] = [(-1, result)]
    lines = text.splitlines()
    index = 0
    while index < len(lines):
        raw = lines[index]
        index += 1
        if not raw.strip() or raw.lstrip().startswith("#"):
            continue
        indent = len(raw) - len(raw.lstrip(" "))
        line = raw.strip()
        while stack and indent <= stack[-1][0]:
            stack.pop()
        parent = stack[-1][1]
        if line.startswith("- "):
            item_text = line[2:]
            if not isinstance(parent, list):
                raise ValueError("Invalid list item placement")
            if ":" in item_text:
                key, value = item_text.split(":", 1)
                item: dict[str, Any] = {key.strip(): _parse_scalar(value) if value.strip() else {}}
                parent.append(item)
                stack.append((indent, item))
            else:
                parent.append(_parse_scalar(item_text))
            continue
        if ":" not in line:
            raise ValueError(f"Invalid YAML line (missing colon): {line}")
        key, value = line.split(":", 1)
        key = key.strip()
        value = value.strip()
        if value == ">":
            block: list[str] = []
            while index < len(lines):
                nxt = lines[index]
                nxt_indent = len(nxt) - len(nxt.lstrip(" "))
                if nxt.strip() and nxt_indent <= indent:
                    break
                block.append(nxt.strip())
                index += 1
            parent[key] = " ".join(part for part in block if part)
        elif value:
            parent[key] = _parse_scalar(value)
        else:
            next_container: Any = {}
            for lookahead in lines[index:]:
                stripped = lookahead.strip()
                if not stripped or stripped.startswith("#"):
                    continue
                look_indent = len(lookahead) - len(lookahead.lstrip(" "))
                if look_indent <= indent:
                    break
                if stripped.startswith("- "):
                    next_container = []
                break
            parent[key] = next_container
            stack.append((indent, next_container))
    return result


def load_yaml(path: Path) -> dict[str, Any]:
    text = path.read_text(encoding="utf-8")
    if yaml is not None:
        data = yaml.safe_load(text)
    else:
        data = _simple_yaml_load(text)
    if not isinstance(data, dict):
        raise ValueError(f"YAML document must be a mapping: {path}")
    return data


def load_skill_manifest(path: Path) -> SkillManifest:
    return SkillManifest.model_validate(load_yaml(path))


def load_registry(path: Path) -> Registry:
    return Registry.model_validate(load_yaml(path))


def validate_skill_manifest(path: Path, repo_root: Path) -> ValidationReport:
    report = ValidationReport()
    rel_path = _display_path(path, repo_root)
    if not path.exists():
        report.add("error", "missing-skill-manifest", "Skill manifest is missing.", rel_path)
        return report
    try:
        manifest_data = load_yaml(path)
    except (OSError, ValueError, Exception) as exc:
        report.add("error", "invalid-skill-yaml", f"Invalid skill YAML: {exc}", rel_path)
        return report

    for key, code in [
        ("owner", "missing-owner"),
        ("risk_tier", "missing-risk-tier"),
        ("dependencies", "missing-dependencies"),
        ("allowed_tools", "missing-allowed-tools"),
        ("evals", "missing-evals"),
    ]:
        if key not in manifest_data or manifest_data[key] in (None, ""):
            level = "error" if key in {"owner", "risk_tier"} else "warning"
            report.add(level, code, f"Required field '{key}' is missing.", rel_path)

    try:
        manifest = SkillManifest.model_validate(manifest_data)
    except ModelValidationError as exc:
        report.add("error", "invalid-skill-manifest", str(exc), rel_path, manifest_data.get("id"))
        return report

    skill_doc = path.parent / manifest.paths.skill_file
    if not skill_doc.exists():
        report.add(
            "error",
            "missing-skill-doc",
            f"Referenced skill file is missing: {manifest.paths.skill_file}",
            _display_path(skill_doc, repo_root),
            manifest.id,
        )
    if manifest.evals.suite_id is None or manifest.evals.status == "not-configured":
        report.add(
            "warning",
            "eval-suite-not-configured",
            "Evaluation suite is not configured for this skill.",
            rel_path,
            manifest.id,
        )
    if manifest.status == "draft":
        report.add("warning", "draft-status", "Skill status is draft.", rel_path, manifest.id)
    if not manifest.dependencies.skills:
        report.add(
            "info",
            "no-skill-dependencies",
            "No skill dependencies declared.",
            rel_path,
            manifest.id,
        )
    if not manifest.dependencies.mcp_servers:
        report.add(
            "info",
            "no-mcp-servers",
            "No MCP servers declared.",
            rel_path,
            manifest.id,
        )
    return report


def validate_registry(repo_root: Path) -> ValidationReport:
    repo_root = repo_root.resolve()
    report = ValidationReport()
    registry_path = repo_root / "registry" / "skills.yaml"
    if not registry_path.exists():
        report.add(
            "error",
            "missing-registry-file",
            "registry/skills.yaml does not exist.",
            "registry/skills.yaml",
        )
        return report
    try:
        registry_data = load_yaml(registry_path)
    except (OSError, ValueError, Exception) as exc:  # noqa: BLE001 - report any parse failure
        report.add(
            "error",
            "invalid-registry-yaml",
            f"Invalid registry YAML: {exc}",
            "registry/skills.yaml",
        )
        return report

    if "version" not in registry_data:
        report.add(
            "error",
            "missing-registry-version",
            "Registry version is missing.",
            "registry/skills.yaml",
        )

    raw_entries = registry_data.get("skills", [])
    seen: set[str] = set()
    for entry in raw_entries if isinstance(raw_entries, list) else []:
        if not isinstance(entry, dict):
            continue
        skill_id = entry.get("id")
        if skill_id in seen:
            report.add(
                "error",
                "duplicate-skill-id",
                f"Duplicate skill id: {skill_id}",
                "registry/skills.yaml",
                skill_id,
            )
        elif isinstance(skill_id, str):
            seen.add(skill_id)

    try:
        registry = Registry.model_validate(registry_data)
    except ModelValidationError as exc:
        report.add("error", "invalid-registry-yaml", str(exc), "registry/skills.yaml")
        return report

    for entry in registry.skills:
        manifest_path = repo_root / entry.path
        if not manifest_path.exists():
            report.add(
                "error",
                "missing-skill-manifest",
                f"Registered skill manifest is missing: {entry.path}",
                entry.path,
                entry.id,
            )
            continue
        skill_report = validate_skill_manifest(manifest_path, repo_root)
        report.findings.extend(skill_report.findings)
        try:
            manifest = load_skill_manifest(manifest_path)
        except (ModelValidationError, OSError, ValueError, Exception):  # noqa: BLE001,S112
            # Validation findings already captured; skip ID mismatch check
            continue
        if manifest.id != entry.id:
            report.add(
                "error",
                "registry-id-mismatch",
                f"Registry id '{entry.id}' does not match manifest id '{manifest.id}'.",
                entry.path,
                entry.id,
            )
    return report
