"""Typer CLI for SkillOps."""

from __future__ import annotations

from collections.abc import Iterable
from pathlib import Path
from typing import Annotated, Any

import typer
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from skillops_core import (
    generate_health_report,
    load_skill_manifest,
    load_skills_registry,
    validate_skill_manifest,
    validate_skills_registry,
)
from skillops_core.constants import (
    DEFAULT_HEALTH_REPORT_JSON_PATH,
    DEFAULT_HEALTH_REPORT_MARKDOWN_PATH,
    DEFAULT_SKILLS_REGISTRY_PATH,
)
from skillops_core.errors import SkillOpsError
from skillops_core.health import write_health_report_json, write_health_report_markdown
from skillops_core.models import (
    RegistrySkillEntry,
    SkillManifest,
    SkillsRegistry,
    ValidationFinding,
    ValidationReport,
)

app = typer.Typer(help="SkillOps control-plane CLI.", no_args_is_help=True)
console = Console(width=160)

RepoRootOption = Annotated[
    Path,
    typer.Option(
        "--repo-root",
        help="Repository root containing registry/skills.yaml.",
        file_okay=False,
        dir_okay=True,
        resolve_path=True,
    ),
]


def _resolve_repo_root(repo_root: Path) -> Path:
    return repo_root.resolve()


def _relative_to_repo(path: Path, repo_root: Path) -> Path:
    if not path.is_absolute():
        return path
    try:
        return path.resolve().relative_to(repo_root)
    except ValueError:
        return path


def _resolve_output_path(path: Path, repo_root: Path) -> Path:
    return path if path.is_absolute() else repo_root / path


def _print_error(message: str) -> None:
    console.print(f"[red]Error:[/] {message}")


def _render_findings(
    findings: Iterable[ValidationFinding],
    title: str = "Validation Findings",
) -> None:
    findings = list(findings)
    if not findings:
        console.print(Panel("No findings.", title=title))
        return

    table = Table(title=title)
    table.add_column("Level")
    table.add_column("Code")
    table.add_column("Skill")
    table.add_column("Path")
    table.add_column("Message")

    styles = {"error": "red", "warning": "yellow", "info": "cyan"}
    for finding in findings:
        style = styles.get(finding.level, "white")
        table.add_row(
            f"[{style}]{finding.level.upper()}[/]",
            finding.code,
            finding.skill_id or "-",
            finding.path or "-",
            finding.message,
        )
    console.print(table)


def _print_validation_summary(report: ValidationReport, *, strict: bool) -> None:
    failed = report.has_errors or (strict and report.warning_count > 0)
    result = "FAIL" if failed else "PASS"
    result_style = "bold red" if failed else "bold green"
    console.print("[bold]SkillOps Validation[/]")
    console.print()
    console.print("[bold]Summary:[/]")
    console.print(f"- Errors: {report.error_count}")
    console.print(f"- Warnings: {report.warning_count}")
    console.print(f"- Info: {report.info_count}")
    console.print()
    console.print("[bold]Result:[/] ", Text(result, style=result_style), sep="")
    if strict and report.warning_count > 0 and not report.has_errors:
        console.print("[yellow]Strict mode: WARNING findings are treated as failures.[/]")


def _load_registry_or_exit(repo_root: Path) -> SkillsRegistry:
    registry_path = repo_root / DEFAULT_SKILLS_REGISTRY_PATH
    try:
        return load_skills_registry(registry_path)
    except SkillOpsError as exc:
        _print_error(f"Failed to load registry: {exc}")
        raise typer.Exit(1) from exc
    except Exception as exc:
        _print_error(f"Failed unexpectedly to load registry ({registry_path}): {exc}")
        console.print_exception()
        raise typer.Exit(1) from exc


def _load_manifest_or_exit(repo_root: Path, entry: RegistrySkillEntry) -> SkillManifest:
    manifest_path = repo_root / entry.path
    msg = "Failed to load skill manifest for"
    try:
        return load_skill_manifest(manifest_path)
    except SkillOpsError as exc:
        _print_error(f"{msg} {entry.id}: {exc}")
        raise typer.Exit(1) from exc
    except Exception as exc:
        _print_error(f"{msg} {entry.id} ({manifest_path}): {exc}")
        console.print_exception()
        raise typer.Exit(1) from exc


def _format_list(values: Iterable[str]) -> str:
    values = list(values)
    return "\n".join(values) if values else "none"


def _format_dict(data: dict[str, Any]) -> str:
    if not data:
        return "none"
    return "\n".join(f"{key}: {value}" for key, value in data.items())


def _add_section(table: Table, section: str, value: str) -> None:
    table.add_row(f"[bold]{section}[/]", value)


@app.command()
def validate(
    repo_root: RepoRootOption = Path("."),
    strict: Annotated[
        bool,
        typer.Option("--strict", help="Treat validation warnings as failures."),
    ] = False,
) -> None:
    """Validate registry/skills.yaml and all registered skill manifests."""

    root = _resolve_repo_root(repo_root)
    try:
        report = validate_skills_registry(root)
    except SkillOpsError as exc:
        _print_error(f"Validation failed: {exc}")
        raise typer.Exit(1) from exc
    except Exception as exc:
        _print_error(f"Validation failed unexpectedly: {exc}")
        raise typer.Exit(1) from exc

    _print_validation_summary(report, strict=strict)
    _render_findings(report.findings)

    if report.has_errors or (strict and report.warning_count > 0):
        raise typer.Exit(1)


@app.command()
def health(
    repo_root: RepoRootOption = Path("."),
    json_path: Annotated[
        Path,
        typer.Option(
            "--json-path",
            help="Path for the JSON health report."
        ),
    ] = Path(DEFAULT_HEALTH_REPORT_JSON_PATH),
    markdown_path: Annotated[
        Path,
        typer.Option(
            "--markdown-path",
            help="Path for the Markdown health report."
        ),
    ] = Path(DEFAULT_HEALTH_REPORT_MARKDOWN_PATH),
    no_write: Annotated[
        bool,
        typer.Option(
            "--no-write",
            help="Print the health summary without writing reports."
        ),
    ] = False,
) -> None:
    """Generate SkillOps health reports."""

    root = _resolve_repo_root(repo_root)
    try:
        report = generate_health_report(root)
        json_output_path = _resolve_output_path(json_path, root)
        markdown_output_path = _resolve_output_path(markdown_path, root)
        if not no_write:
            write_health_report_json(report, json_output_path)
            write_health_report_markdown(report, markdown_output_path)
    except SkillOpsError as exc:
        _print_error(f"Health report generation failed: {exc}")
        raise typer.Exit(1) from exc
    except Exception as exc:
        _print_error(f"Health report generation failed unexpectedly: {exc}")
        raise typer.Exit(1) from exc

    console.print("[bold]SkillOps Health[/]")
    console.print()
    console.print(f"Total Skills: {report.total_skills}")
    console.print(f"Average Health Score: {report.average_health_score}")
    console.print(f"Errors: {report.errors}")
    console.print(f"Warnings: {report.warnings}")
    console.print()
    if no_write:
        console.print("Reports written: no-write enabled")
    else:
        console.print("Reports written:")
        console.print(f"- {_relative_to_repo(json_output_path, root)}")
        console.print(f"- {_relative_to_repo(markdown_output_path, root)}")


@app.command(name="list")
def list_skills(
    repo_root: RepoRootOption = Path("."),
    status: Annotated[
        str | None,
        typer.Option("--status", help="Filter skills by manifest status."),
    ] = None,
    risk_tier: Annotated[
        str | None,
        typer.Option("--risk-tier", help="Filter skills by manifest risk tier."),
    ] = None,
) -> None:
    """List registered skills."""

    root = _resolve_repo_root(repo_root)
    registry = _load_registry_or_exit(root)

    table = Table(title="Registered Skills")
    for column in ["ID", "Name", "Version", "Status", "Risk Tier", "Owner", "Path"]:
        table.add_column(column, no_wrap=True)

    for entry in registry.skills:
        manifest = _load_manifest_or_exit(root, entry)
        if status is not None and manifest.status != status:
            continue
        if risk_tier is not None and manifest.risk_tier != risk_tier:
            continue
        table.add_row(
            manifest.id,
            manifest.name,
            manifest.version,
            manifest.status,
            manifest.risk_tier,
            manifest.owner.name,
            entry.path,
        )

    console.print(table)


@app.command()
def inspect(
    skill_id: Annotated[str, typer.Argument(help="The ID of the skill to inspect.")],
    repo_root: RepoRootOption = Path(".")
) -> None:
    """Inspect one registered skill."""

    root = _resolve_repo_root(repo_root)
    reg = _load_registry_or_exit(root)
    entry = next((item for item in reg.skills if item.id == skill_id), None)
    if entry is None:
        _print_error(f"Skill not found: {skill_id}")
        raise typer.Exit(1)

    manifest = _load_manifest_or_exit(root, entry)
    validation_report = validate_skill_manifest(
        root / entry.path, root)

    console.print(Panel(manifest.description, title=f"{manifest.name} ({manifest.id})"))

    table = Table(title="Skill Details")
    table.add_column("Section")
    table.add_column("Details")
    _add_section(
        table,
        "Identity",
        (
            f"ID: {manifest.id}\n"
            f"Name: {manifest.name}\n"
            f"Version: {manifest.version}\n"
            f"Description: {manifest.description.strip()}"
        ),
    )
    _add_section(
        table,
        "Owner",
        f"Name: {manifest.owner.name}\nContact: {manifest.owner.contact}"
    )
    _add_section(
        table,
        "Status and Risk",
        f"Status: {manifest.status}\nRisk Tier: {manifest.risk_tier}",
    )
    _add_section(
        table,
        "Type",
        f"Category: {manifest.type.category}\nExecution: {manifest.type.execution}",
    )
    _add_section(
        table,
        "Compatibility",
        (
            f"Agents:\n{_format_list(manifest.compatibility.agents)}\n"
            f"Environments:\n{_format_list(manifest.compatibility.environments)}"
        ),
    )
    _add_section(
        table,
        "Dependencies",
        (
            f"Skills:\n{_format_list(manifest.dependencies.skills)}\n"
            f"Tools:\n{_format_list(manifest.dependencies.tools)}\n"
            f"MCP Servers:\n{_format_list(manifest.dependencies.mcp_servers)}"
        ),
    )
    _add_section(
        table,
        "Allowed Tools",
        _format_dict(manifest.allowed_tools.model_dump())
    )
    _add_section(
        table,
        "Evals",
        _format_dict(manifest.evals.model_dump())
    )
    _add_section(
        table,
        "Provenance",
        _format_dict(manifest.provenance.model_dump())
    )
    _add_section(
        table,
        "Paths",
        f"Registry Path: {entry.path}\nSkill File: {manifest.paths.skill_file}",
    )
    console.print(table)
    _render_findings(validation_report.findings, title="Validation Findings")


if __name__ == "__main__":
    app()
