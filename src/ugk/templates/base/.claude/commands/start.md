---
name: start
description: Guided onboarding -- detects project state by scanning Design/GDD/, Assets/Scripts/, and config files. Routes to the right phase. Use whenever a new team member joins or you don't know where to begin.
---

# /start -- Guided Onboarding

## What this command does

Scans the project to understand its current state, then routes the user to the correct next step in the 7-phase workflow.

## Step 1: Scan the project (MANDATORY -- do this FIRST, before saying anything)

You MUST actually read files and directories. Do not guess or assume.

### 1a. Scan Design/GDD/

List ALL `.md` files in `Design/GDD/`. For EACH file found:
- Read the file
- Note: filename, title/topic, which of the 8 GDD sections are present
- Check if it's a concept doc, a system GDD, or a raw design doc

If the directory doesn't exist or is empty, note "No GDD files found."

### 1b. Check engine configuration

Read `.claude/docs/technical-preferences.md`. Check if engine/language/naming/performance fields are filled in (not `[TO BE CONFIGURED]`).

### 1c. Check for code

List `Assets/Scripts/` subdirectories. Count `.cs` files (excluding `.gitkeep`). Note if there's real implementation code or just scaffolding.

### 1d. Check architecture docs

Check if `Docs/architecture/` has any `.md` files.

### 1e. Check production state

- Check `Production/session-state/active.md` for paused session
- Check `Production/epics/` for epic files
- Check `Production/sprints/` for sprint files

## Step 2: Present assessment

Summarize what you found. Be specific -- list the actual files you found, not just "GDDs exist". Example:

```
=== Project Assessment ===

Design/GDD/ (3 files found):
  - game-concept.md -- game concept with pillars, core loop (complete)
  - combat.md -- combat system design, 6/8 sections present (missing: Formulas, Acceptance Criteria)
  - progression.md -- raw design notes, not in 8-section format

Engine: Unity 6 configured (URP, mobile target)
Code: 0 .cs files in Assets/Scripts/
Architecture: No docs yet
Production: No sprints or epics

Assessment: Phases 1-2 partially complete. GDDs exist but need standardization.
```

## Step 3: Route to next action

Based on what you found, suggest paths from this table:

| What you found | Suggested path |
|---|---|
| Active session state in active.md | Resume from where you left off |
| No GDD files at all, no concept | `/brainstorm` -- start from scratch |
| GDD files exist but not in 8-section format | `/adopt` -- retrofit to kit format |
| GDDs in 8-section format, engine not configured | `/setup-engine` -- configure tech stack |
| GDDs complete, engine configured, no architecture | `/create-architecture` or `/gate-check 2` |
| Code exists but few/no design docs | `/project-stage-detect` -- full assessment |
| Everything looks complete for current phase | `/gate-check <phase>` -- validate and advance |

Present the paths that fit as a table. Let the user choose.

## CRITICAL RULES

- **ALWAYS scan Design/GDD/ first.** Never skip this step. Never say "no GDDs found" without actually listing the directory.
- **Read every .md file** in Design/GDD/. They may have any filename -- not just `game-concept.md`.
- **Be specific** about what you found. List filenames. Count sections. Note what's missing.
- **Don't guess the project state.** If you can't read a directory, say so and ask the user.

## Collaboration protocol

Follow the kit-wide Q -> O -> D -> Draft -> Approval protocol. Always ask before writing files.
