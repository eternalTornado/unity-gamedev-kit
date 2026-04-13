# Installation

## Prerequisites

| Tool | Why | Install |
|---|---|---|
| **Python 3.10+** | Runs `ugk` | [python.org](https://www.python.org/downloads/) |
| **`uv`** | Fast Python package manager (same as spec-kit) | See below |
| **Git** | `ugk init` creates a git repo | [git-scm.com](https://git-scm.com/) |
| **Claude Code** | Actually uses the `.claude/` kit | [claude.ai/code](https://claude.ai/code) |
| **Unity 6 (6000.x)** | The engine | [unity.com/download](https://unity.com/download) |
| **`gh` CLI** *(optional)* | Create GitHub repos from terminal | [cli.github.com](https://cli.github.com/) |

## Install `uv`

### Windows (PowerShell)

```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

### macOS / Linux

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Verify:

```bash
uv --version
```

## Install `ugk`

### Option A — Persistent (recommended)

```bash
uv tool install unity-gamedev-kit --from git+https://github.com/eternalTornado/unity-gamedev-kit.git
```

Now `ugk` is available anywhere:

```bash
ugk --help
ugk version
```

### Option B — One-time without install

```bash
uvx --from git+https://github.com/eternalTornado/unity-gamedev-kit.git ugk init MyGame
```

### Option C — Pin to a version (for team consistency)

```bash
uv tool install unity-gamedev-kit --from git+https://github.com/eternalTornado/unity-gamedev-kit.git@v0.1.0
```

### Option D — Local development (contributors)

```bash
git clone https://github.com/eternalTornado/unity-gamedev-kit.git
cd unity-gamedev-kit
uv pip install -e .
```

## Upgrade

```bash
uv tool upgrade unity-gamedev-kit
```

## Uninstall

```bash
uv tool uninstall unity-gamedev-kit
```

## Verify with a Unity project

```bash
cd /path/to/your/UnityProject
ugk init .
ugk check
```

Open Claude Code in that folder. You should see the `session-start.sh` hook print context at startup.

## Troubleshooting

### `ugk: command not found` after install

`uv` installs tools to `~/.local/bin` (Linux/macOS) or `%USERPROFILE%\.local\bin` (Windows). Make sure that's on your `PATH`.

```bash
uv tool update-shell    # auto-update PATH in your shell rc
```

### Hooks don't run on Windows

Git Bash is required for `.sh` hooks. Install [Git for Windows](https://git-scm.com/download/win) (includes Git Bash). Alternatively, Windows-native `.ps1` hook variants land in v0.3.

### `claude-code` can't see the hooks

Check that `.claude/settings.json` exists in the project root and references the hook paths correctly. Run `ugk check` to verify.
