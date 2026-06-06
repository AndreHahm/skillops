"""Typer CLI for SkillOps."""

from __future__ import annotations

from pathlib import Path
from typing import Annotated

import typer
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from skillops_core.health import (
    generate_health_report,
    write_health_report_json,
    write_health_report_markdown,
)
from skillops_core.models import FindingLevel
from skillops_core.validation import load_registry, load_skill_manifest, validate_registry

app = typer.Typer(help="SkillOps control-plane CLI.")
console = Console()


def _repo_root(path: Path | None = None) -> Path:
    return (path or Path.cwd()).resolve()


def _print_findings(report) -> None:
    table = Table(title="Validation Findings")
    table.add_column("Level")
    table.add_column("Code")
    table.add_column("Skill")
    table.add_column("Path")
    table.add_column("Message")
    for finding in report.findings:
        style = {
            FindingLevel.error: "red",
            FindingLevel.warning: "yellow",
            FindingLevel.info: "cyan",
        }[finding.level]
        table.add_row(
            f"[{style}]{finding.level}[/]",
            finding.code,
            finding.skill_id or "-",
            finding.path or "-",
            finding.message,
        )
    console.print(table if report.findings else Panel("No findings.", title="Validation"))


@app.command()
def validate(repo_root: Annotated[Path | None, typer.Option("--repo-root")] = None) -> None:
    """Validate registry/skills.yaml and all registered skill manifests."""
    report = validate_registry(_repo_root(repo_root))
    _print_findings(report)
    console.print(
        f"[bold]Summary:[/] {report.error_count} errors, "
        f"{report.warning_count} warnings, {report.info_count} info"
    )
    if report.has_errors:
        raise typer.Exit(1)


@app.command()
def health(repo_root: Annotated[Path | None, typer.Option("--repo-root")] = None) -> None:
    """Generate JSON and Markdown health reports."""
    root = _repo_root(repo_root)
    report = generate_health_report(root)
    json_path = root / "reports" / "health" / "health-report.json"
    markdown_path = root / "reports" / "health" / "health-report.md"
    write_health_report_json(report, json_path)
    write_health_report_markdown(report, markdown_path)
    console.print(
        Panel(f"Generated health reports. Overall score: {report.overall_score}", title="Health")
    )
    console.print(f"JSON: {json_path}")
    console.print(f"Markdown: {markdown_path}")


@app.command(name="list")
def list_skills(repo_root: Annotated[Path | None, typer.Option("--repo-root")] = None) -> None:
    """List registered skills."""
    root = _repo_root(repo_root)
    try:
        registry = load_registry(root / "registry" / "skills.yaml")
    except Exception as exc:
        console.print(f"[red]Failed to load registry:[/] {exc}")
        raise typer.Exit(1)
    table = Table(title="Registered Skills")
    for column in ["id", "name", "version", "status", "risk_tier", "owner", "path"]:
        table.add_column(column)
    for entry in registry.skills:
        try:
            manifest = load_skill_manifest(root / entry.path)
        except Exception as exc:
            console.print(f"[red]Failed to load skill manifest for {entry.id}:[/] {exc}")
            raise typer.Exit(1)
        table.add_row(
            manifest.id,
            manifest.name,
            manifest.version,
            str(manifest.status),
            str(manifest.risk_tier),
            manifest.owner.name,
            entry.path,
        )
    console.print(table)


@app.command()
def inspect(
    skill_id: str, repo_root: Annotated[Path | None, typer.Option("--repo-root")] = None
) -> None:
    """Inspect one registered skill."""
    root = _repo_root(repo_root)
    try:
        registry = load_registry(root / "registry" / "skills.yaml")
    except Exception as exc:
        console.print(f"[red]Failed to load registry:[/] {exc}")
        raise typer.Exit(1)
    entry = next((item for item in registry.skills if item.id == skill_id), None)
    if entry is None:
        console.print(f"[red]Skill not found:[/] {skill_id}")
        raise typer.Exit(1)
    try:
        manifest = load_skill_manifest(root / entry.path)
    except Exception as exc:
        console.print(f"[red]Failed to load skill manifest for {skill_id}:[/] {exc}")
        raise typer.Exit(1)
    report = validate_registry(root)
    console.print(Panel(manifest.description, title=f"{manifest.name} ({manifest.id})"))
    table = Table(title="Manifest")
    table.add_column("Field")
    table.add_column("Value")
    table.add_row("version", manifest.version)
    table.add_row("status", str(manifest.status))
    table.add_row("risk_tier", str(manifest.risk_tier))
    table.add_row("owner", f"{manifest.owner.name} <{manifest.owner.contact}>")
    table.add_row("type", f"{manifest.type.category} / {manifest.type.execution}")
    table.add_row("dependencies", str(manifest.dependencies.model_dump()))
    table.add_row("allowed_tools", str(manifest.allowed_tools.model_dump(exclude_none=True)))
    table.add_row("evals", str(manifest.evals.model_dump()))
    table.add_row("path", entry.path)
    console.print(table)
    skill_findings = report.findings_for_skill(skill_id)
    if skill_findings:
        finding_report = type(report)(findings=skill_findings)
        _print_findings(finding_report)


if __name__ == "__main__":
    app()
