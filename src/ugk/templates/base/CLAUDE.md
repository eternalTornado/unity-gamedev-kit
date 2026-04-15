# CLAUDE.md — Unity GameDev Kit

This project was bootstrapped with [`unity-gamedev-kit`](https://github.com/eternalTornado/unity-gamedev-kit).

## Role

You are Claude Code working inside a Unity game project. You follow a **5-phase workflow** (Concept → Systems Design → Architecture → Implementation → Polish) with formal gates between phases. Phase 4 (Implementation) delegates to [speckit](https://github.com/github/spec-kit) for spec-driven development (`/plan` → `/tasks` → `/implement`).

## Collaboration Protocol

**User-driven collaboration, not autonomous execution.**

Every task: **Question → Options → Decision → Draft → Approval**.

- Ask *"May I write this to `<filepath>`?"* before every `Write` or `Edit`.
- Show drafts or summaries before requesting approval.
- Multi-file changes require explicit approval for the full changeset.
- **No git commits without user instruction.**

### Asking the user

When a step has ambiguities, decisions, or multiple valid options:

- Use the **`AskUserQuestion` tool** — do NOT generate free-form questions in chat.
- Batch ALL ambiguous questions into a SINGLE `AskUserQuestion` call (up to 4 questions per call). Do not ask one question at a time.
- Each question should have 2-4 concrete, mutually-exclusive options. Users can always pick "Other" to type a custom answer.
- Only fall back to free-form chat prompts if the answer truly cannot be enumerated (e.g., "describe your game concept in one paragraph").

This rule applies to every command in this kit: `/setup-engine`, `/brainstorm`, `/design-system`, `/clarify-gaps`, `/adopt`, `/architecture-decision`, and any speckit command invoked from Phase 4.

### Suggest next step after every command

Every command MUST end with a **"Suggested next step"** block — a short bullet list of 1-3 commands the user could reasonably run next given the output. Format:

```text
## Suggested next step

- `/gate-check 2` — verify Systems Design is complete
- `/design-system <name>` — draft another system GDD
- `/review-all-gdds` — cross-check existing GDDs for consistency
```

If nothing obvious comes next, say so explicitly (`No obvious next step — ask the user what they want to do.`).

## Priority Hierarchy (for every code review)

1. 🔴 **Code Quality** — nullable types ON, zero warnings, throw not log, `nameof`, `readonly`/`const`, no inline comments.
2. 🟡 **Modern C#** — LINQ over loops, expression bodies, pattern matching, `??`/`?.`/`??=`, records.
3. 🟢 **Unity Architecture** — clean separation of concerns, event-driven communication, Data Controllers (never direct data access), UniTask async.
4. 🔵 **Performance** — no LINQ in `Update`, zero-alloc hot paths, object pooling, frame budget.

## 5-Phase Workflow

| Phase | Key commands | Artifacts |
|---|---|---|
| 1. Concept | `/brainstorm`, `/setup-engine`, `/map-systems` | `Design/GDD/game-concept.md`, `systems-index.md` |
| 2. Systems Design | `/design-system`, `/review-all-gdds`, `/update-gdd` | 8-section GDDs per system |
| 3. Architecture | `/create-architecture`, `/architecture-decision` | `Docs/architecture/` + ADRs |
| 4. Implementation | `/implement <module>` → speckit `/plan` → `/tasks` → `/implement` → `/code-review` | `Docs/specs/<module>/plan.md`, `tasks.md`, source code, tests |
| 5. Polish | `/perf-profile`, `/balance-check`, `/playtest-report`, `/release-checklist`, `/hotfix` | Tuned build + shipped release |

Between phases: `/gate-check <phase>` → verdict `PASS` / `CONCERNS` / `FAIL`.

Phase gates: `concept` (1→2), `systems` (2→3), `architecture` (3→4), `implementation` (4→5), `polish` (5→ship).

## Speckit Integration (Phase 4)

Phase 4 uses [speckit](https://github.com/github/spec-kit) for spec-driven implementation — but **skips `/speckit.specify`** because the GDD already contains the feature spec (Detailed Rules, Edge Cases, Acceptance Criteria, Formulas).

**Phase 4 flow for each module/feature:**

1. User runs `/implement <module-name>` (ugk wrapper)
2. Wrapper reads the relevant GDD from `Design/GDD/<module>.md` and architecture doc from `Docs/architecture/<module>.md`
3. Delegates to `/speckit.plan` — generates per-feature tech plan at `Docs/specs/<module>/plan.md`
4. Delegates to `/speckit.tasks` — generates dependency-ordered checklist at `Docs/specs/<module>/tasks.md`
5. Delegates to `/speckit.implement` — executes tasks with TDD
6. Finishes with `/code-review` — verifies priority hierarchy (Quality → Modern C# → Architecture → Performance)

**Document locations** (override speckit defaults): speckit writes to `Docs/specs/<module>/` instead of `specs/<feature>/` to keep all design/tech docs under `Docs/`.

**Constitution**: speckit reads `/memory/constitution.md` for gate checks. ugk populates this from CLAUDE.md + `.claude/docs/technical-preferences.md` during `/setup-engine`.

## Technology Stack

- **Engine**: Unity 6 (6000.x)
- **Language**: C# 9 (Unity 6 constraint — no C# 10+ features)
- **Architecture**: No DI framework — use ScriptableObject events, Service Locator, or manual injection
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
| `Docs/specs/**` | speckit conventions | Per-module plan.md, tasks.md, data-model.md, contracts/ |
| `Tests/**` | `.claude/rules/test-standards.md` | AAA structure, regression tests |
| `Prototypes/**` | `.claude/rules/prototype-code.md` | Relaxed — hardcode allowed |

## Session Rules

- **Precedence of authority** (ties broken top-down): approved GDD > `CLAUDE.md` > `.claude/docs/technical-preferences.md` > rules in `.claude/rules/` > drafts and ad-hoc decisions.
- **Document focus**: keep the active document count ≤ 3 per task. Read `docs/_index.md` first if it exists; do not load everything.
- `/clear` when switching tasks or topics to prevent context pollution.
- `/compact` when the session is long (>60-70% context usage) or right after writing a full section to file.
- **Incremental writing**: for multi-section documents (GDDs, ADRs, plan.md), create the skeleton first, then fill sections one at a time with approval between sections. Write each approved section immediately to survive context crashes.

## Governance

- **AI MUST NOT self-approve gates.** `/gate-check` prints the verdict; only the user decides whether to advance.
- **Gate fail** → fix → re-submit (max 2 cycles). If still failing after 2 cycles, escalate to the user.
- **P0 hotfix exception**: code first, retrospective spec within 24h.
- **Constitution-like changes** (CLAUDE.md, technical-preferences.md): require explicit user approval; propagate to affected commands after the change; never edit silently.
- **Compliance**: every PR touching gameplay/architecture MUST cite the relevant GDD section or ADR ID; `/code-review` verifies this.

## Session State

Maintain `Production/session-state/active.md` as a living checkpoint. Update after each milestone (section approved, architecture decision made, implementation milestone, test results). The `session-start` hook auto-previews this file when a session begins.

## Important: Start Claude from the project root

Always open Claude Code from the Unity project root (where `.claude/` and `.git/` are), **not** from a subdirectory like `Assets/`. Starting from a subfolder means hooks won't run and `/slash` commands won't be found.

## First session?

Type `/start` in Claude Code to begin the guided onboarding.
