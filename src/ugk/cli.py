"""ugk CLI — entry point.

Inspired by github/spec-kit's `specify` CLI.

Commands:
    ugk init [PATH]              Bootstrap a Unity project with the AI workflow kit.
    ugk check                    Verify installation (git, hooks, claude-code).
    ugk update                   Upgrade an existing project's kit files (diff-aware).
    ugk add <kind> <id>          Add an optional skill/agent/rule/profile/hook.
    ugk list [kind]              List installable components (skills, agents, rules, profiles, hooks).
    ugk version                  Print ugk version.
"""
from __future__ import annotations

import hashlib
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Optional

import typer
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Confirm
from rich.table import Table

from . import __version__

app = typer.Typer(
    name="ugk",
    help="Unity GameDev Kit — AI-driven workflow for Unity from GDD to Ship.",
    no_args_is_help=True,
    add_completion=False,
)
console = Console()

TEMPLATES_ROOT = Path(__file__).parent / "templates"
BASE_ROOT = TEMPLATES_ROOT / "base"
PROFILES_ROOT = TEMPLATES_ROOT / "profiles"

KIND_DIRS = {
    "skill": ".claude/skills",
    "skills": ".claude/skills",
    "agent": ".claude/agents",
    "agents": ".claude/agents",
    "rule": ".claude/rules",
    "rules": ".claude/rules",
    "hook": ".claude/hooks",
    "hooks": ".claude/hooks",
}


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


def _sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def _rewrite_settings_for_windows(settings_path: Path) -> None:
    """On Windows, rewrite hook commands to run .ps1 via PowerShell."""
    import json
    if not settings_path.exists():
        return
    try:
        data = json.loads(settings_path.read_text(encoding="utf-8"))
    except Exception:
        return
    hooks = data.get("hooks", {})
    for _event, entries in hooks.items():
        for entry in entries:
            for h in entry.get("hooks", []):
                cmd = h.get("command", "")
                if cmd.endswith(".sh"):
                    ps1 = cmd[:-3] + ".ps1"
                    h["command"] = f'powershell -NoProfile -ExecutionPolicy Bypass -File "{ps1}"'
    settings_path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")


def _ensure_in_project() -> Path:
    """Return cwd if it looks like a ugk-initialized project, else exit."""
    here = Path.cwd()
    if not (here / ".claude").exists():
        console.print("[red]Not a ugk project[/red] — no `.claude/` found. Run `ugk init` first.")
        raise typer.Exit(1)
    return here


# ---------- init ----------

@app.command()
def init(
    path: str = typer.Argument(".", help="Path to Unity project (use '.' for current)"),
    engine: str = typer.Option("unity-6", "--engine", help="Engine version: unity-6, unity-2022-lts"),
    scope: str = typer.Option("generic", "--scope", help="Scope profile: generic, mobile, pc, multiplayer"),
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

    if not BASE_ROOT.exists():
        console.print("[red]ERROR:[/red] base template missing. Reinstall ugk.")
        raise typer.Exit(1)

    copied = _copy_template(BASE_ROOT, target, overwrite=force)
    console.print(f"[green]✓[/green] Copied {copied} files from base template")

    # Apply scope profile overlay if requested
    if scope != "generic":
        profile_dir = PROFILES_ROOT / scope
        if profile_dir.exists():
            p_copied = _copy_template(profile_dir, target, overwrite=force)
            console.print(f"[green]✓[/green] Applied [bold]{scope}[/bold] profile ({p_copied} files)")
        else:
            console.print(f"[yellow]![/yellow] Scope '{scope}' not found — skipped")

    # Make hooks executable on Unix
    hooks_dir = target / ".claude" / "hooks"
    if hooks_dir.exists() and sys.platform != "win32":
        for h in hooks_dir.glob("*.sh"):
            h.chmod(0o755)
        console.print("[green]✓[/green] Hooks marked executable")

    # Rewrite settings.json for Windows to use .ps1 hooks via PowerShell
    if sys.platform == "win32":
        _rewrite_settings_for_windows(target / ".claude" / "settings.json")
        console.print("[green]✓[/green] settings.json patched for Windows (.ps1 hooks)")

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


# ---------- check ----------

@app.command()
def check() -> None:
    """Verify installation: git, Claude Code, hook executability."""
    console.print(Panel.fit("[bold]ugk check[/bold]", border_style="cyan"))

    checks = []
    checks.append(("git installed", shutil.which("git") is not None))
    checks.append(("gh CLI (optional)", shutil.which("gh") is not None))
    checks.append(("python >= 3.10", sys.version_info >= (3, 10)))

    here = Path.cwd()
    hooks = here / ".claude" / "hooks"
    if hooks.exists():
        sh_files = list(hooks.glob("*.sh"))
        checks.append((f".claude/hooks/ present ({len(sh_files)} hooks)", True))
    else:
        checks.append((".claude/hooks/ (run `ugk init` first)", False))

    skills = here / ".claude" / "skills"
    if skills.exists():
        checks.append((f".claude/skills/ present ({len(list(skills.glob('*.md')))} skills)", True))

    agents = here / ".claude" / "agents"
    if agents.exists():
        checks.append((f".claude/agents/ present ({len(list(agents.glob('*.md')))} agents)", True))

    for label, ok in checks:
        icon = "[green]✓[/green]" if ok else "[red]✗[/red]"
        console.print(f"  {icon} {label}")

    if all(ok for _, ok in checks):
        console.print("\n[bold green]All checks passed.[/bold green]")
    else:
        console.print("\n[bold yellow]Some checks failed. See docs/INSTALL.md.[/bold yellow]")


# ---------- version ----------

@app.command()
def version() -> None:
    """Print ugk version."""
    console.print(f"unity-gamedev-kit {__version__}")


# ---------- list ----------

@app.command("list")
def list_cmd(
    kind: Optional[str] = typer.Argument(None, help="Filter by kind: skills, agents, rules, profiles, hooks"),
) -> None:
    """List installable components shipped with this ugk version."""
    console.print(Panel.fit(f"[bold]ugk list[/bold] — v{__version__}", border_style="cyan"))

    sources = {
        "skills": (BASE_ROOT / ".claude" / "skills", "*.md"),
        "agents": (BASE_ROOT / ".claude" / "agents", "*.md"),
        "rules": (BASE_ROOT / ".claude" / "rules", "*.md"),
        "hooks": (BASE_ROOT / ".claude" / "hooks", "*.sh"),
    }
    if kind and kind not in sources and kind != "profiles":
        console.print(f"[red]Unknown kind:[/red] {kind}. Try: {', '.join(sources)} or profiles")
        raise typer.Exit(1)

    for k, (folder, pattern) in sources.items():
        if kind and kind != k:
            continue
        if not folder.exists():
            continue
        table = Table(title=k.capitalize(), show_header=True, header_style="bold cyan")
        table.add_column("Name")
        table.add_column("Description", overflow="fold")
        for f in sorted(folder.glob(pattern)):
            if f.name == ".gitkeep":
                continue
            desc = _extract_description(f)
            table.add_row(f.stem, desc)
        console.print(table)

    if not kind or kind == "profiles":
        if PROFILES_ROOT.exists():
            table = Table(title="Profiles", show_header=True, header_style="bold cyan")
            table.add_column("Name")
            table.add_column("Description", overflow="fold")
            for p in sorted(PROFILES_ROOT.iterdir()):
                if not p.is_dir():
                    continue
                readme = p / "PROFILE.md"
                desc = readme.read_text(encoding="utf-8").splitlines()[1] if readme.exists() else ""
                table.add_row(p.name, desc)
            console.print(table)


def _extract_description(path: Path) -> str:
    """Extract 'description:' from YAML frontmatter or first non-header line."""
    try:
        text = path.read_text(encoding="utf-8")
    except Exception:
        return ""
    if text.startswith("---"):
        fm_end = text.find("---", 3)
        if fm_end > 0:
            fm = text[3:fm_end]
            for line in fm.splitlines():
                if line.strip().startswith("description:"):
                    return line.split(":", 1)[1].strip().strip('"').strip("'")
    # fallback: first non-empty non-heading line
    for line in text.splitlines():
        s = line.strip()
        if s and not s.startswith("#") and not s.startswith("---"):
            return s[:120]
    return ""


# ---------- add ----------

@app.command()
def add(
    kind: str = typer.Argument(..., help="Kind: skill, agent, rule, hook, profile"),
    name: str = typer.Argument(..., help="Name (e.g., code-review) or profile (e.g., mobile)"),
    force: bool = typer.Option(False, "--force", help="Overwrite if exists"),
) -> None:
    """Install an optional component from the ugk catalog into the current project."""
    here = _ensure_in_project()

    if kind == "profile":
        src = PROFILES_ROOT / name
        if not src.exists():
            console.print(f"[red]Profile not found:[/red] {name}")
            console.print("Available: ", ", ".join(p.name for p in PROFILES_ROOT.iterdir() if p.is_dir()))
            raise typer.Exit(1)
        copied = _copy_template(src, here, overwrite=force)
        console.print(f"[green]✓[/green] Applied profile [bold]{name}[/bold] ({copied} files)")
        return

    sub = KIND_DIRS.get(kind)
    if not sub:
        console.print(f"[red]Unknown kind:[/red] {kind}. Try: skill, agent, rule, hook, profile")
        raise typer.Exit(1)

    ext = ".sh" if kind.startswith("hook") else ".md"
    src = BASE_ROOT / sub / f"{name}{ext}"
    if not src.exists():
        console.print(f"[red]Not found in catalog:[/red] {kind}/{name}{ext}")
        console.print(f"Run `ugk list {kind}s` to see available components.")
        raise typer.Exit(1)

    dst = here / sub / f"{name}{ext}"
    dst.parent.mkdir(parents=True, exist_ok=True)
    if dst.exists() and not force:
        console.print(f"[yellow]Already exists:[/yellow] {dst.relative_to(here)} (use --force to overwrite)")
        raise typer.Exit(1)

    shutil.copy2(src, dst)
    if ext == ".sh" and sys.platform != "win32":
        dst.chmod(0o755)
    console.print(f"[green]✓[/green] Added [bold]{kind}/{name}[/bold] → {dst.relative_to(here)}")


# ---------- update ----------

@app.command()
def update(
    dry_run: bool = typer.Option(False, "--dry-run", help="Show what would change without writing"),
    only: Optional[str] = typer.Option(None, "--only", help="Limit to kind: skills, agents, rules, hooks"),
) -> None:
    """Upgrade kit files in current project to match installed ugk version.

    - Adds missing files from the catalog.
    - For existing files: only updates if unchanged from a previous ugk version (sha matches stock).
    - User-modified files are NEVER overwritten — they're reported for manual merge.
    """
    here = _ensure_in_project()
    console.print(Panel.fit(f"[bold]ugk update[/bold] — v{__version__} {'(dry-run)' if dry_run else ''}", border_style="cyan"))

    kinds = [only] if only else ["skills", "agents", "rules", "hooks"]

    added = 0
    unchanged = 0
    modified_skipped: list[str] = []
    replaced = 0

    for k in kinds:
        sub = KIND_DIRS.get(k, f".claude/{k}")
        src_dir = BASE_ROOT / sub
        dst_dir = here / sub
        if not src_dir.exists():
            continue
        dst_dir.mkdir(parents=True, exist_ok=True)

        for src in src_dir.rglob("*"):
            if src.is_dir() or src.name == ".gitkeep":
                continue
            rel = src.relative_to(src_dir)
            dst = dst_dir / rel

            if not dst.exists():
                if not dry_run:
                    dst.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copy2(src, dst)
                    if src.suffix == ".sh" and sys.platform != "win32":
                        dst.chmod(0o755)
                added += 1
                console.print(f"  [green]+ add[/green] {sub}/{rel}")
                continue

            # Exists — compare hashes
            if _sha256(src) == _sha256(dst):
                unchanged += 1
                continue

            # Differs. Could be user-modified OR old ugk version.
            # Heuristic: we don't have history, so ask user per-file in non-dry mode.
            if dry_run:
                console.print(f"  [yellow]~ differs[/yellow] {sub}/{rel} (would prompt)")
                modified_skipped.append(str(rel))
                continue
            if Confirm.ask(f"  Replace {sub}/{rel}? (user changes will be lost)", default=False):
                shutil.copy2(src, dst)
                replaced += 1
                console.print(f"    [green]✓[/green] replaced")
            else:
                modified_skipped.append(str(rel))
                console.print(f"    [yellow]kept user version[/yellow]")

    console.print(
        f"\n[bold]Summary:[/bold] +{added} added, ={unchanged} unchanged, "
        f"~{replaced} replaced, !{len(modified_skipped)} kept-user"
    )
    if modified_skipped and not dry_run:
        console.print("\nFiles with local changes (review manually):")
        for p in modified_skipped:
            console.print(f"  - {p}")


if __name__ == "__main__":
    app()
