# CLI Reference

Complete flag reference for every `ugk` command.

## `ugk init [PATH]`

Bootstrap a Unity project with the AI workflow kit. Run this **at the Unity project root** (the folder that contains `Assets/`, `ProjectSettings/`, etc.), not inside `Assets/`.

```bash
ugk init [PATH] [--engine ENGINE] [--scope SCOPE] [--force]
```

| Flag | Type | Default | Valid values | Description |
|---|---|---|---|---|
| `PATH` | positional | `.` | any directory path | Target project root. Created if missing. Use `.` for current directory. |
| `--engine` | option | `unity-6` | `unity-6`, `unity-2022-lts` | Unity engine version. Controls which engine-reference snapshot is copied and which rules activate. |
| `--scope` | option | `generic` | `generic`, `mobile`, `pc`, `multiplayer` | Scope profile overlay. See [Scope profiles](#scope-profiles) below. |
| `--force` | flag | `false` | — | Overwrite existing files in the target directory. Without it, `ugk` skips files that already exist. |

### Scope profiles

Scope determines which extra rules, perf budgets, and store-submission checks layer on top of the base template. A file in `Assets/Scripts/UI/` gets different verdicts depending on scope.

| Scope | When to use | What it adds |
|---|---|---|
| `generic` | Prototypes, jam games, engine demos | No overlay — base rules only. |
| `mobile` | iOS / Android shipping titles | Touch input rules, strict perf budgets (draw calls, memory, thermal), store submission checklist (App Store / Play Store). |
| `pc` | Steam / Epic / standalone PC | Scalability presets (Low→Ultra), gamepad + K/M dual input, Steam notes. |
| `multiplayer` | Any networked game (co-op, PvP, MMO) | Server-authoritative rules, bandwidth budgets, versioned messages, anti-cheat notes. |

You can combine profiles after init with `ugk add profile <name>`.

### Examples

```bash
ugk init . --engine unity-6 --scope mobile
ugk init MyGame --engine unity-2022-lts --scope pc
ugk init . --scope multiplayer --force
```

---

## `ugk check`

Verify installation: git, Python, Claude Code tooling, and (if inside a ugk project) count of installed skills / agents / hooks.

```bash
ugk check
```

No flags. Safe to run anywhere — reports which checks pass/fail.

---

## `ugk version`

Print the installed ugk version.

```bash
ugk version
```

No flags.

---

## `ugk list [KIND]`

List installable components shipped with this ugk version. Without `KIND`, lists everything.

```bash
ugk list [KIND]
```

| Arg | Valid values | Description |
|---|---|---|
| `KIND` | `skills`, `agents`, `rules`, `hooks`, `profiles` | Filter to one category. Omit to list all. |

### Examples

```bash
ugk list                # all categories
ugk list skills         # only skills
ugk list profiles       # only scope profiles
```

---

## `ugk add <KIND> <NAME>`

Install a single optional component from the ugk catalog into the current project. Must be run inside a ugk-initialized project (one with a `.claude/` folder).

```bash
ugk add KIND NAME [--force]
```

| Arg / Flag | Valid values | Description |
|---|---|---|
| `KIND` | `skill`, `agent`, `rule`, `hook`, `profile` | Category of the component. |
| `NAME` | any entry listed by `ugk list KIND` | Component name, without file extension. For profiles: `mobile`, `pc`, `multiplayer`. |
| `--force` | — | Overwrite if the target file already exists. Without it, refuses to overwrite. |

### Examples

```bash
ugk add skill code-audit              # install the /code-audit skill
ugk add agent balance-designer        # install balance-designer subagent
ugk add hook validate-meta-files      # install the Unity .meta hook
ugk add profile multiplayer           # layer multiplayer rules on an existing project
ugk add rule networking --force       # overwrite existing networking rule
```

---

## `ugk update`

Upgrade kit files in the current project to match the installed ugk version. Hash-aware — it will **not** overwrite files you've modified locally without confirmation.

```bash
ugk update [--dry-run] [--only KIND]
```

| Flag | Valid values | Description |
|---|---|---|
| `--dry-run` | — | Show what would change (add / differ) without writing. Safe to run anytime. |
| `--only` | `skills`, `agents`, `rules`, `hooks` | Limit the update to one category. Omit to update all four. |

### Behaviour

- **Missing files** are added silently.
- **Unchanged files** (hash matches catalog) are skipped as up-to-date.
- **Differing files** prompt per-file: replace (lose local edits) or keep user version. In `--dry-run`, they are listed but never modified.

### Examples

```bash
ugk update --dry-run                  # preview all changes
ugk update --only skills              # upgrade only .claude/skills/
ugk update                            # interactive upgrade of everything
```

---

## Exit codes

| Code | Meaning |
|---|---|
| `0` | Success |
| `1` | Invalid argument, missing catalog entry, or not inside a ugk project (for `add` / `update`) |

## Environment

- `uv tool install unity-gamedev-kit --from git+...` installs `ugk` persistently on `PATH`.
- `uvx --from git+... ugk <cmd>` runs without installing.
- No environment variables are read by ugk itself.

## See also

- [INSTALL.md](./INSTALL.md) — prerequisites and installation per OS
- [TUTORIAL.md](./TUTORIAL.md) — end-to-end walkthrough (Orbit Runner demo)
- [WORKFLOW.md](./WORKFLOW.md) — how commands chain into full task flows
