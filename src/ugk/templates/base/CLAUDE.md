# CLAUDE.md — Unity GameDev Kit

This project was bootstrapped with [`unity-gamedev-kit`](https://github.com/eternalTornado/unity-gamedev-kit).

## Role

You are Claude Code working inside a Unity game project. You follow a 7-phase workflow (Concept → Systems Design → Technical Setup → Pre-Production → Production → Polish → Release), with formal gates between phases.

## Collaboration Protocol

**User-driven collaboration, not autonomous execution.**

Every task: **Question → Options → Decision → Draft → Approval**.

- Ask *"May I write this to `<filepath>`?"* before every `Write` or `Edit`.
- Show drafts or summaries before requesting approval.
- Multi-file changes require explicit approval for the full changeset.
- **No git commits without user instruction.**

## Priority Hierarchy (for every code review)

1. 🔴 **Code Quality** — nullable types ON, zero warnings, throw not log, `nameof`, `readonly`/`const`, no inline comments.
2. 🟡 **Modern C#** — LINQ over loops, expression bodies, pattern matching, `??`/`?.`/`??=`, records.
3. 🟢 **Unity Architecture** — VContainer DI, SignalBus events, Data Controllers (never direct data access), UniTask async.
4. 🔵 **Performance** — no LINQ in `Update`, zero-alloc hot paths, object pooling, frame budget.

## 7-Phase Workflow

| Phase | Key skills | Artifacts |
|---|---|---|
| 1. Concept | `/brainstorm`, `/setup-engine`, `/map-systems` | `Design/GDD/game-concept.md`, `systems-index.md` |
| 2. Systems | `/design-system`, `/review-all-gdds` | 8-section GDDs |
| 3. Tech | `/create-architecture`, `/architecture-decision` | `Docs/architecture/` |
| 4. Pre-prod | `/create-epics`, `/create-stories`, `/sprint-plan` | `Production/epics/`, stories |
| 5. Production | `/dev-story`, `/code-review` | Code + tests |
| 6. Polish | `/perf-profile`, `/balance-check`, `/playtest-report` | Tuned build |
| 7. Release | `/release-checklist`, `/hotfix` | Shipped build |

Between phases: `/gate-check <phase>` → verdict `PASS` / `CONCERNS` / `FAIL`.

## Technology Stack

- **Engine**: Unity 6 (6000.x)
- **Language**: C# 9 (Unity 6 constraint — no C# 10+ features)
- **DI**: VContainer (preferred) or TheOne.DI
- **Events**: SignalBus or Publisher/Subscriber
- **Async**: UniTask
- **Version Control**: Git, trunk-based
- **Test**: Unity Test Framework (NUnit)

## Folder Conventions (path-scoped rules)

| Path | Rule file | Key constraint |
|---|---|---|
| `Assets/Scripts/Core/**` | `.claude/rules/engine-code.md` | Zero-alloc hot paths, engine ← gameplay |
| `Assets/Scripts/Gameplay/**` | `.claude/rules/gameplay-code.md` | Data-driven, no singletons, use delta time |
| `Assets/Scripts/AI/**` | `.claude/rules/ai-code.md` | 2ms/frame budget, debug visualization |
| `Assets/Scripts/UI/**` | `.claude/rules/ui-code.md` | No game state ownership, accessibility |
| `Assets/Scripts/Networking/**` | `.claude/rules/network-code.md` | Server-authoritative, versioned messages |
| `Design/GDD/**` | `.claude/rules/design-docs.md` | 8 mandatory sections |
| `Tests/**` | `.claude/rules/test-standards.md` | AAA structure, regression tests |
| `Prototypes/**` | `.claude/rules/prototype-code.md` | Relaxed — hardcode allowed |

## Incremental Writing

For multi-section documents (GDDs, ADRs): create skeleton first, then fill sections one at a time with approval between sections. Write each approved section immediately to survive context crashes.

## Session State

Maintain `Production/session-state/active.md` as a living checkpoint. Update after each milestone. The `session-start.sh` hook auto-previews this file when a session begins.

## Important: Start Claude from the project root

Always open Claude Code from the Unity project root (where `.claude/` and `.git/` are), **not** from a subdirectory like `Assets/`. Starting from a subfolder means hooks won't run and `/slash` commands won't be found.

## First session?

Type `/start` in Claude Code to begin the guided onboarding.
