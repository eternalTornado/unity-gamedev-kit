<div align="center">

# 🎮 Unity GameDev Kit (`ugk`)

**AI-driven workflow for Unity — from GDD to Ship, with Claude Code.**

*Inspired by [github/spec-kit](https://github.com/github/spec-kit) and [Claude-Code-Game-Studios](https://github.com/Donchitos/Claude-Code-Game-Studios).*

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](./LICENSE)
[![Version](https://img.shields.io/badge/version-1.0.0-brightgreen.svg)](https://github.com/eternalTornado/unity-gamedev-kit/releases)
[![Status](https://img.shields.io/badge/status-stable-brightgreen.svg)](https://github.com/eternalTornado/unity-gamedev-kit)

</div>

---

## What is this?

A one-command scaffolder that drops an opinionated `.claude/` directory — **agents, skills, hooks, rules, and templates** — into any Unity project, so your whole team and Claude Code share the same workflow.

**Philosophy:** Game dev isn't a stream of Jira tickets. It's a 7-phase pipeline: Concept → Systems Design → Technical Setup → Pre-Production → Production → Polish → Release. Each phase has a gate. Each gate has artifacts. `ugk` gives Claude Code the rules to enforce that.

## Quick start

```bash
# Install once (persistent)
uv tool install unity-gamedev-kit --from git+https://github.com/eternalTornado/unity-gamedev-kit.git

# Or run once without installing
uvx --from git+https://github.com/eternalTornado/unity-gamedev-kit.git ugk init MyGame

# Bootstrap current Unity project
cd MyUnityProject
ugk init . --engine unity-6 --scope mobile

# Verify installation
ugk check
```

Then open **Claude Code** in the project folder and type `/start`.

> **Don't have `uv`?** Install it first: `powershell -c "irm https://astral.sh/uv/install.ps1 | iex"` on Windows, or `curl -LsSf https://astral.sh/uv/install.sh | sh` on macOS/Linux.

## What you get

```
MyUnityProject/
├── CLAUDE.md                        # Entry point — Claude reads this first
├── .claude/
│   ├── agents/                      # 13 Unity-specialized sub-agents
│   ├── skills/                      # 23 slash-commands (/start, /design-system, /code-audit, ...)
│   ├── hooks/                       # 6 shell hooks + 6 Windows .ps1 equivalents
│   ├── rules/                       # 8 path-scoped rules for Assets/Scripts/**
│   └── settings.json                # Hook + permission registrations
├── Design/GDD/                      # Game design docs — 7-section template (doubles as Phase 4 spec)
├── Docs/architecture/               # Architecture Decision Records (ADRs)
├── Production/                      # Epics, stories, sprint plans, session state
└── Assets/Scripts/{Core,Gameplay,AI,UI,Networking}/   # Path-scoped rule zones
```

## The 7-Phase Workflow

| Phase | Skill | Output | Gate |
|---|---|---|---|
| 1. Concept | `/brainstorm` → `/setup-engine` → `/map-systems` | `game-concept.md`, `systems-index.md` | `/gate-check concept` |
| 2. Systems Design | `/design-system` (×N) → `/review-all-gdds` | 7-section GDDs, cross-review | `/gate-check systems` |
| 3. Technical Setup | `/create-architecture` → `/architecture-decision` | `architecture.md`, ADRs | `/gate-check tech` |
| 4. Pre-Production | `/create-epics` → `/create-stories` → `/sprint-plan` | Epic/Story backlog | `/gate-check preprod` |
| 5. Production | `/dev-story` → `/code-review` | Code + unit/integration tests | `/gate-check prod` |
| 6. Polish | `/perf-profile` → `/balance-check` → `/playtest-report` | Tuned build | `/gate-check polish` |
| 7. Release | `/release-checklist` → `/hotfix` | Shipped build | `/gate-check release` |

Each gate returns a verdict: `PASS` / `CONCERNS` / `FAIL`. `CONCERNS` passes with acknowledged risk; `FAIL` blocks the next phase.

## Why `ugk` over copying files manually?

1. **Versioned** — pinned releases, `ugk update` migrates projects to new kit versions.
2. **One command, whole team** — every member runs `ugk init` and gets the identical `.claude/` directory; git-tracked.
3. **Scope-aware templates** — `--scope mobile` adds touch + perf + store rules, `--scope multiplayer` adds networking/authority rules, `--scope pc` adds scalability + gamepad rules.
4. **Pluggable** — `ugk add agent unity-dots-specialist` drops in an extra agent without touching the rest.

## Commands

```bash
ugk init [PATH]          # Bootstrap a Unity project
  --engine unity-6       # Engine version (default: unity-6)
  --scope mobile         # Scope profile (generic|mobile|pc|multiplayer)
  --force                # Overwrite existing files

ugk check                # Verify git, Python, Claude Code tooling
ugk list [kind]          # List installable skills/agents/rules/profiles/hooks
ugk add <kind> <name>    # Add an optional component (skill/agent/rule/hook/profile)
ugk update [--dry-run]   # Upgrade kit files; hash-aware, preserves local changes
ugk version              # Print version
```

## Core concepts

### Collaboration Protocol (from [CCGS](https://github.com/Donchitos/Claude-Code-Game-Studios))

> **User-driven collaboration, not autonomous execution.**
> Every task: **Question → Options → Decision → Draft → Approval**

Claude asks *"May I write this to `<filepath>`?"* before every `Write`/`Edit`. Multi-file changes need full-changeset approval. No commits without your instruction.

### Priority hierarchy (from [TheOne Studio](https://github.com/The1Studio/theone-training-skills))

When reviewing Unity C# code, Claude checks in order:

1. 🔴 **Code Quality** — nullable types, zero warnings, throw not log, `nameof`, `readonly`
2. 🟡 **Modern C#** — LINQ, expression bodies, pattern matching, `??`/`?.`/`??=`
3. 🟢 **Unity Architecture** — VContainer DI, SignalBus events, Data Controllers, UniTask
4. 🔵 **Performance** — no LINQ in `Update`, zero-alloc hot paths, object pooling

### Path-scoped rules

Rules attach to folder globs. Code in `Assets/Scripts/AI/` gets AI rules (2ms budget, debug visualization). Code in `Assets/Scripts/Networking/` gets network rules (server-authoritative, versioned messages). Code in `Prototypes/` gets relaxed rules (hardcode allowed). Same file type, different standards.

## Documentation

- [**INSTALL.md**](./docs/INSTALL.md) — Prerequisites, Windows/macOS/Linux install
- [**CLI.md**](./docs/CLI.md) — Complete flag reference for every `ugk` command
- [**TUTORIAL.md**](./docs/TUTORIAL.md) — Build a demo game from concept to ship using `ugk`
- [**WORKFLOW.md**](./docs/WORKFLOW.md) — Full task-type flows (GDD, bug, balance, reconcile)
- [**TEAMS.md**](./docs/TEAMS.md) — Solo / GD+Dev / small team / remote configs
- [**SKILLS.md**](./docs/SKILLS.md) — Complete skill reference
- [**AGENTS.md**](./docs/AGENTS.md) — Complete agent reference
- [**EXAMPLES.md**](./docs/EXAMPLES.md) — 5 end-to-end scenarios
- [**CONTRIBUTING.md**](./CONTRIBUTING.md) — How to add agents/skills/rules

## Project status

**v1.0.0 — stable.** All roadmap items shipped.

- [x] `ugk init` with base template + scope profiles
- [x] 23 skills (6 doc-code-sync, 12 core, 5 design/release)
- [x] 13 agents covering leadership, design, engineering, process
- [x] Scope profiles: mobile, pc, multiplayer
- [x] `ugk update` with hash-aware migration
- [x] `ugk add <kind> <name>` for selective install
- [x] `ugk list [kind]` to browse catalog
- [x] Windows-native hooks (PowerShell)
- [x] CI templates (GitHub Actions)

## Inspirations & credits

- [github/spec-kit](https://github.com/github/spec-kit) — the CLI distribution pattern
- [Claude-Code-Game-Studios](https://github.com/Donchitos/Claude-Code-Game-Studios) — 48-agent studio, 7-phase pipeline, hook patterns
- [The1Studio/theone-training-skills](https://github.com/The1Studio/theone-training-skills) — priority hierarchy, VContainer/SignalBus enforcement

## License

MIT — see [LICENSE](./LICENSE).
