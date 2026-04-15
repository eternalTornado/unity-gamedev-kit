---
name: project-stage-detect
description: Analyze the current project to determine which phase (1-5) of the 5-phase workflow it's in. Checks GDDs, architecture docs, specs, code, tests, and production artifacts.
model: haiku
---

# /project-stage-detect -- Workflow Phase Detection

## What this command does

Scans the project structure to determine the current workflow phase and suggest the appropriate next action.

## Detection logic (5-phase workflow)

IMPORTANT: Always scan `Design/GDD/` for ALL `.md` files. Read each one. Do not only look for specific filenames.

| Check | Indicator |
|---|---|
| Any `.md` file exists in `Design/GDD/` | Phase 1 started |
| `Design/GDD/systems-index.md` + concept doc + at least 3 game pillars | Phase 1 complete |
| Every MVP system in `systems-index.md` has its GDD with all 7 sections | Phase 2 started |
| `Design/GDD/gdd-cross-review-*.md` exists with PASS or CONCERNS | Phase 2 complete |
| `Docs/architecture/overview.md` exists | Phase 3 started |
| Per-system architecture docs + ≥3 ADRs | Phase 3 complete |
| Any `Docs/specs/<module>/plan.md` exists | Phase 4 started |
| All MVP modules have `plan.md` + `tasks.md` with all tasks `[X]` | Phase 4 complete |
| `Production/qa/` or `Docs/playtest/` has reports; performance budgets met | Phase 5 started |
| Release checklist + store metadata complete | Phase 5 complete |

## Process

1. **Scan** `Design/GDD/` and list ALL `.md` files. Read each to check section completeness.
2. **Scan** `Docs/architecture/` for overview + per-system docs + ADRs.
3. **Scan** `Docs/specs/*/` for `plan.md` + `tasks.md`. For each `tasks.md`, count completed vs total tasks.
4. **Scan** `Production/` for `stage.txt`, `session-state/active.md`, `qa/`, release artifacts.
5. **Determine** the current phase (the highest phase with incomplete indicators).
6. **Report**:
   - Current phase and sub-step
   - What's been completed
   - What's missing or incomplete
   - Suggested next command to run
7. If artifacts from multiple phases exist but are incomplete, flag the gaps.

## Output

Phase assessment printed to conversation. No files written.

## Suggested next step

End with a "Suggested next step" block listing 1-3 commands the user could run next:

- If Phase 1 incomplete → `/brainstorm`, `/setup-engine`, `/map-systems`
- If Phase 2 incomplete → `/design-system <name>`, `/review-all-gdds`, `/gate-check systems`
- If Phase 3 incomplete → `/create-architecture`, `/architecture-decision`, `/gate-check architecture`
- If Phase 4 incomplete → `/implement <module>`, `/gate-check implementation`
- If Phase 5 incomplete → `/perf-profile`, `/playtest-report`, `/release-checklist`

## Notes

This is a read-only diagnostic. It does not modify any files. Use it when rejoining a project or when unsure where you left off.
