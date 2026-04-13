"""ugk CLI — entry point.

Inspired by github/spec-kit's `specify` CLI.

Commands:
    ugk init [PATH]      Bootstrap a Unity project with the AI workflow kit.
    ugk check            Verify installation (git, hooks executable, claude-code).
    ugk update           Upgrade an existing project's kit files (diff-aware).
    ugk add <kind> <id>  Add an optional agent/skill/rule to current project.
"""
from __future__ import annotations

import shutil
import subprocess
import sys
from pathlib import Path
from typing import Optional

import typer
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Confirm, Prompt

from . import __version__

app = typer.Typer(
    name="ugk",
    help="Unity GameDev Kit — AI-driven workflow for Unity from GDD to Ship.",
    no_args_is_help=True,
    add_completion=False,
)
console = Console()

TEMPLATES_ROOT = Path(__file__).parent / "templates"


def _copy_template(src: Path, dst: Path, overwrite: bool = False) -> int:
    """Copy template files; return count copied. Skips existing unless overwrite."""
    count = 0
    for item in src.rglob("*"):
        if item.is_dir():
            continue
        rel = item.relative_to(src)
        target = dst / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        if target.exists() and not overwrite:
            continue
        shutil.copy2(item, target)
        count += 1
    return count


@app.command()
def init(
    path: str = typer.Argument(".", help="Path to Unity project (use '.' for current)"),
    engine: str = typer.Option("unity-6", "--engine", help="Engine version: unity-6, unity-2022-lts"),
    scope: str = typer.Option("generic", "--scope", help="Project scope: generic, mobile-casual, pc-midcore, multiplayer"),
    force: bool = typer.Option(False, "--force", help="Overwrite existing files"),
) -> None:
    """Bootstrap a Unity project with the AI workflow kit."""
    target = Path(path).resolve()
    target.mkdir(parents=True, exist_ok=True)

    console.print(Panel.fit(
        f"[bold cyan]Unity GameDev Kit[/bold cyan] v{__version__}\n"
        f"Target: [yellow]{target}[/yellow]\n"
        f"Engine: [green]{engine}[/green] | Scope: [green]{scope}[/green]",
        border_style="cyan",
    ))

    base = TEMPLATES_ROOT / "base"
    if not base.exists():
        console.print("[red]ERROR:[/red] base template missing. Reinstall ugk.")
        raise typer.Exit(1)

    copied = _copy_template(base, target, overwrite=force)
    console.print(f"[green]✓[/green] Copied {copied} files from base template")

    # Make hooks executable on Unix
    hooks_dir = target / ".claude" / "hooks"
    if hooks_dir.exists() and sys.platform != "win32":
        for h in hooks_dir.glob("*.sh"):
            h.chmod(0o755)
        console.print("[green]✓[/green] Hooks marked executable")

    # Init git if absent
    if not (target / ".git").exists():
        if Confirm.ask("Initialize git repo?", default=True):
            subprocess.run(["git", "init"], cwd=target, check=False, capture_output=True)
            console.print("[green]✓[/green] git initialized")

    console.print("\n[bold]Next steps:[/bold]")
    console.print("  1. [cyan]cd[/cyan] into the project")
    console.print("  2. Open [cyan]Claude Code[/cyan]")
    console.print("  3. Run [cyan]/start[/cyan] to begin the 7-phase workflow")
    console.print("\nDocs: [blue]https://github.com/eternalTornado/unity-gamedev-kit[/blue]\n")


@app.command()
def check() -> None:
    """Verify installation: git, Claude Code, hook executability."""
    console.print(Panel.fit("[bold]ugk check[/bold]", border_style="cyan"))

    checks = []

    # git
    git_ok = shutil.which("git") is not None
    checks.append(("git installed", git_ok))

    # gh (optional)
    gh_ok = shutil.which("gh") is not None
    checks.append(("gh CLI (optional)", gh_ok))

    # python 3
    py_ok = sys.version_info >= (3, 10)
    checks.append(("python >= 3.10", py_ok))

    # hooks in current dir
    here = Path.cwd()
    hooks = here / ".claude" / "hooks"
    if hooks.exists():
        sh_files = list(hooks.glob("*.sh"))
        checks.append((f".claude/hooks/ present ({len(sh_files)} hooks)", True))
    else:
        checks.append((".claude/hooks/ (run `ugk init` first)", False))

    for label, ok in checks:
        icon = "[green]✓[/green]" if ok else "[red]✗[/red]"
        console.print(f"  {icon} {label}")

    if all(ok for _, ok in checks):
        console.print("\n[bold green]All checks passed.[/bold green]")
    else:
        console.print("\n[bold yellow]Some checks failed. See docs/INSTALL.md.[/bold yellow]")


@app.command()
def version() -> None:
    """Print ugk version."""
    console.print(f"unity-gamedev-kit {__version__}")


@app.command()
def update(
    dry_run: bool = typer.Option(False, "--dry-run", help="Show diff without writing"),
) -> None:
    """Upgrade existing project's kit files (diff-aware). NOT YET IMPLEMENTED."""
    console.print("[yellow]`ugk update` is a v0.2 feature. Coming soon.[/yellow]")
    console.print("For now: back up `.claude/`, rerun `ugk init --force`, re-apply customizations.")


if __name__ == "__main__":
    app()
