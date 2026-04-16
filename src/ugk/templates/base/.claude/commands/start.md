---
name: start
description: Guided onboarding -- detects project state by scanning Design/GDD/, Assets/Scripts/, and config files. Routes to the right phase of the 5-phase workflow.
---

# /start -- Guided Onboarding

## What this command does

Scans the project to understand its current state, then routes the user to the correct next step in the **5-phase workflow** (Concept → Systems Design → Architecture → Implementation → Polish).

## Step 1: Scan the project (MANDATORY -- do this FIRST, before saying anything)

You MUST actually read files and directories. Do not guess or assume.

### 1a. Scan Design/GDD/

List ALL `.md` files in `Design/GDD/`. For EACH file found:
- Read the file
- Note: filename, title/topic, which of the 7 required GDD sections are present
- Check if it's a concept doc, a system GDD, or a raw design doc

If the directory doesn't exist or is empty, note "No GDD files found."

### 1b. Check engine configuration

Read `.claude/docs/technical-preferences.md`. Check if engine/language/naming/performance fields are filled in (not `[TO BE CONFIGURED]`).

### 1c. Check for code

List `Assets/Scripts/` subdirectories. Count `.cs` files (excluding `.gitkeep`). Note if there's real implementation code or just scaffolding.

### 1d. Check architecture docs

List `.md` files in `Docs/architecture/`. Note overview.md, per-system docs, ADR count.

### 1e. Check implementation specs

List subdirectories in `Docs/specs/`. Per module, check if `plan.md` and `tasks.md` exist and count how many tasks are marked `[X]`.

### 1f. Check production state

- Check `Production/session-state/active.md` for paused session
- Check `Production/stage.txt` for last gate passed

## Step 2: Present assessment

Summarize what you found. Be specific -- list the actual files you found, not just "GDDs exist". Example:

```
=== Project Assessment ===

Design/GDD/ (3 files found):
  - game-concept.md -- game concept with pillars, core loop (complete)
  - combat.md -- combat system design, 5/7 sections present (missing: Formulas, Acceptance Criteria)
  - progression.md -- raw design notes, not in 7-section format

Engine: Unity 6 configured (URP, mobile target)
Code: 0 .cs files in Assets/Scripts/
Architecture: No docs yet
Specs: No Docs/specs/ — Phase 4 not started
Production: No active session state, Production/stage.txt missing

Assessment: Phase 1 complete. Phase 2 partially complete — GDDs exist but not all in 7-section format.
```

## Step 3: Route to next action

Based on what you found, suggest one or more paths from this table:

| What you found | Current phase | Suggested command |
|---|---|---|
| Active session state in `active.md` | varies | Resume from where you left off |
| No GDD files at all, no concept | Phase 1 | `/brainstorm` — start from scratch |
| GDD files exist but not in 7-section format | Phase 1-2 | `/adopt` — retrofit to kit format |
| GDDs in 7-section format, engine not configured | Phase 1 | `/setup-engine` — configure tech stack |
| GDDs complete, engine configured, no architecture | Phase 2→3 | `/gate-check systems` then `/create-architecture` |
| Architecture docs exist, no specs | Phase 3→4 | `/gate-check architecture` then `/implement <module>` |
| Specs exist, some `tasks.md` complete | Phase 4 | `/implement <next-module>` or `/gate-check implementation` |
| All MVP modules complete | Phase 4→5 | `/gate-check implementation` then `/perf-profile` / `/playtest-report` |
| Code exists but few/no design docs | varies | `/project-stage-detect` — full assessment |

Present the matching paths to the user. If more than one path fits, use the `AskUserQuestion` tool to let the user pick. Do NOT generate the question free-form in chat.

## CRITICAL RULES

- **ALWAYS scan `Design/GDD/` first.** Never skip this step. Never say "no GDDs found" without actually listing the directory.
- **Read every `.md` file** in Design/GDD/. They may have any filename — not just `game-concept.md`.
- **Be specific** about what you found. List filenames. Count sections. Note what's missing.
- **Don't guess the project state.** If you can't read a directory, say so and ask the user.
- **Use `AskUserQuestion`** for routing decisions with 2-4 concrete options. Do NOT free-form ask "what do you want to do next?" in chat.

## Suggested next step

End with a "Suggested next step" block listing the 1-3 commands most likely to move the project forward, given the current phase. If the user still needs to pick (multiple viable paths), that pick is the next step.

## Collaboration protocol

Follow the kit-wide Q → O → D → Draft → Approval protocol. Always ask before writing files.
