---
name: start
description: Guided onboarding — detects project state, routes to the right phase (brainstorm, setup-engine, design-system, or adopt existing artifacts). Use whenever a new team member joins or you don't know where to begin.
---

# /start — Guided Onboarding

## What this skill does

Analyzes the current project state and routes the user to the correct next step in the 7-phase workflow.

## Detection logic

1. Read `.claude/docs/technical-preferences.md` — is the engine configured?
2. Read `Design/GDD/game-concept.md` — does a concept doc exist?
3. Scan `Assets/Scripts/` — is there real source code (not just `.gitkeep`)?
4. Read `Production/session-state/active.md` — is there a paused session to resume?

## Routing table

| State | Route to |
|---|---|
| Active session state exists | Resume from `active.md` |
| No engine, no concept, no code | Path A — `/brainstorm` |
| Vague idea (user mentions one) | Path B — `/brainstorm <seed>` |
| Clear concept exists, no engine | Path C — `/setup-engine` |
| Brownfield — code exists, few docs | Path D1 — `/project-stage-detect` |
| Brownfield — code + GDDs exist | Path D2 — `/adopt` (retrofit to kit format) |

## Instructions

1. Detect the project state using the logic above.
2. Print a short status summary to the user (engine, concept status, code presence).
3. Ask the user which path fits (A/B/C/D1/D2) — don't guess.
4. After user confirms path, invoke the matching skill by name.
5. If resuming from `active.md`, read the file and summarize the paused work before continuing.

## Collaboration protocol

Follow the kit-wide Q→O→D→Draft→Approval protocol. Always ask before writing files.
