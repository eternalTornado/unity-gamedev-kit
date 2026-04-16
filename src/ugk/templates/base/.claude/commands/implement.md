---
name: implement
description: Phase 4 entry point. Implements a module end-to-end by reading its GDD + architecture doc, then delegating to speckit (/plan -> /tasks -> /implement) and finishing with /code-review.
---

# /implement — Implement a Module (Phase 4)

## Usage

```
/implement <module-name>
/implement combat
/implement progression
```

`<module-name>` must match a GDD file at `Design/GDD/<module-name>.md` or a subsystem name from `Design/GDD/systems-index.md`.

## What this command does

This is the **ugk wrapper around speckit's spec-driven implementation flow**. The completed GDD (post-retrofit, post-gate) acts as the feature spec (no `/speckit.specify` needed — completed GDDs contain Detailed Rules, Edge Cases, Acceptance Criteria, and Formulas).

**Flow**:

```
Design/GDD/<module>.md     <-- feature spec (from Phase 2)
Docs/architecture/<module>.md  <-- system architecture (from Phase 3)
        |
        v
  /speckit.plan     -> Docs/specs/<module>/plan.md + data-model.md + contracts/
  /speckit.tasks    -> Docs/specs/<module>/tasks.md (dependency-ordered checklist)
  /speckit.implement -> source code + tests, tasks marked [X]
        |
        v
  /code-review      -> verify Quality -> Modern C# -> Architecture -> Performance
```

## Prerequisites

Stop and surface missing inputs if any of the following are absent:

- `Design/GDD/<module-name>.md` exists and has all 7 sections complete (see `.claude/rules/design-docs.md`)
- `Docs/architecture/<module-name>.md` OR `Docs/architecture/overview.md` exists
- `/gate-check architecture` returned PASS (check `Production/stage.txt`)
- `speckit` is installed in the project (look for `.specify/` directory — if missing, instruct the user to run `specify init` or `uvx specify-cli`)

If any prerequisite is missing, print the list and STOP. Do NOT proceed.

## Process

### Step 1: Confirm the module and collect any missing decisions

Read the GDD and architecture doc. Identify any decisions that speckit's `/plan` would need that aren't already resolved (e.g., which networking library, whether to use addressables for this module, async pattern).

If there are ambiguities, use the **`AskUserQuestion` tool** to batch ALL open questions into ONE call (max 4). Each question must have 2-4 concrete options. Do NOT ask free-form in chat. Do NOT ask questions one at a time.

### Step 2: Delegate to `/speckit.plan`

Invoke speckit's planning command with these overrides:

- **Input spec**: point speckit at `Design/GDD/<module>.md` instead of a `spec.md`
- **Output directory**: `Docs/specs/<module>/` instead of `specs/<feature>/`
- **Constitution**: speckit will auto-read `/memory/constitution.md`. If missing, generate it from `CLAUDE.md` + `.claude/docs/technical-preferences.md` before planning

Wait for speckit's plan to complete. Verify the output exists at `Docs/specs/<module>/plan.md`.

### Step 3: Delegate to `/speckit.tasks`

Break the plan into a dependency-ordered task checklist. Output goes to `Docs/specs/<module>/tasks.md`. Verify checkbox format and `[P]` parallelization markers.

### Step 4: Delegate to `/speckit.implement`

Execute tasks sequentially (respecting dependencies and parallel markers). TDD: tests before implementation. Code goes to `Assets/Scripts/<area>/<module>/`. Tests go to `Tests/<Unit|Integration>/<module>/`.

Route file-level work by path (matches ugk's folder conventions):

- `Assets/Scripts/Gameplay/` → gameplay logic
- `Assets/Scripts/AI/` → AI logic (2ms/frame budget applies)
- `Assets/Scripts/UI/` → UI (no game-state ownership)
- `Assets/Scripts/Networking/` → networking (server-authoritative)
- `Assets/Scripts/Core/` → engine-level (zero-alloc hot paths)

After each task, mark it `[X]` in `tasks.md`.

### Step 5: `/code-review`

Once all tasks are `[X]`, run `/code-review` on the new/modified files. Verify the 4-priority hierarchy:

- 🔴 Code Quality (nullable, warnings, `throw`, `nameof`, `readonly`)
- 🟡 Modern C# (LINQ outside hot paths, expression bodies, pattern matching)
- 🟢 Unity Architecture (separation of concerns, event-driven, Data Controllers)
- 🔵 Performance (no LINQ in Update, zero-alloc, pooling)

Resolve any 🔴 issues before declaring done. 🟡/🟢/🔵 issues can be logged as follow-ups.

### Step 6: Mark module done

- Update `Production/session-state/active.md` with module status
- If this is the last MVP module, suggest `/gate-check implementation`

## Collaboration protocol

- Before each speckit delegation step, summarize to the user what speckit will do and ask for approval to proceed.
- Never commit code during `/implement` — commits require explicit user instruction.
- If `/speckit.plan` surfaces constitution violations, STOP and ask the user whether to amend the constitution or adjust the plan.
- If the GDD's Acceptance Criteria cannot be met with available infrastructure, STOP and escalate (may need an ADR first — run `/architecture-decision`).

## Context awareness

This command can consume significant context window space. If context usage exceeds 70%:
1. Write any in-progress section to file immediately
2. Summarize remaining work
3. Suggest the user run `/compact` then resume

## Suggested next step

End with a "Suggested next step" block. Typical options:

- `/implement <next-module>` — implement the next module from `systems-index.md`
- `/gate-check implementation` — all MVP modules done, verify Phase 4 complete
- `/perf-profile` — run performance profiling on the new module
- `/architecture-decision <title>` — if an implementation decision needs to be recorded as an ADR

## Note on legacy `/dev-story`

`/dev-story` is deprecated in favor of `/implement`. It referenced `Production/stories/<id>.md` (Jira-style stories) and hardcoded DI framework choices. `/implement` reads from GDDs directly and uses speckit's generic implementation flow, which is tool-agnostic and more portable.
