---
name: project-stage-detect
description: Analyze the current project to determine which workflow phase it's in (1-7). Checks for GDDs, architecture docs, code, tests, and production artifacts.
model: haiku
---

# /project-stage-detect -- Workflow Phase Detection

## What this command does

Scans the project structure to determine the current workflow phase and suggest the appropriate next action.

## Detection logic

IMPORTANT: Always scan `Design/GDD/` for ALL `.md` files. Read each one. Do not only look for specific filenames.

| Check | Indicator |
|---|---|
| Any `.md` file exists in `Design/GDD/` | Phase 1 started |
| `Design/GDD/systems-index.md` + 2 system GDDs exist | Phase 1 complete |
| All GDDs have 8 sections | Phase 2 complete |
| `Docs/architecture/overview.md` exists | Phase 3 started |
| Architecture docs + ADRs exist for all systems | Phase 3 complete |
| `Production/epics/` has epic files | Phase 4 started |
| Stories exist with acceptance criteria | Phase 4 complete |
| `Assets/Scripts/` has implementation code (.cs) | Phase 5 started |
| Tests exist and pass, code coverage meets target | Phase 5 complete |
| Performance audit exists in `Production/qa/` | Phase 6 started |
| Playtest reports show no BLOCKING issues | Phase 6 complete |
| `Production/releases/` has a release checklist | Phase 7 started |

## Process

1. **Scan** `Design/GDD/` and list ALL `.md` files. Read each file to check section completeness. Then scan other directories for the indicators above.
2. **Determine** the current phase (the highest phase with incomplete indicators).
3. **Report**:
   - Current phase and sub-step
   - What's been completed
   - What's missing or incomplete
   - Suggested next command to run
4. If artifacts from multiple phases exist but are incomplete, flag the gaps.

## Output

Phase assessment printed to conversation. No files written.

## Notes

This is a read-only diagnostic. It does not modify any files. Use it when rejoining a project or when unsure where you left off.
