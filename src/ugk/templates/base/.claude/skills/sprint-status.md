---
name: sprint-status
description: Read-only snapshot of the current sprint — active stories, blockers, progress. Cheap Haiku-tier status check to run daily.
model: haiku
---

# /sprint-status

Read-only. No file writes. No questions.

## Workflow

1. Read `production/sprints/current/` (or latest sprint folder).
2. Read `production/session-state/active.md`.
3. List stories with status: Ready / In-Progress / Blocked / Done.
4. Surface: how many days left, blockers, unverified stories.
5. Print compact table + 1-line TL;DR.

## Output format (chat only)

```
Sprint: 2026-W15 (day 3/5)
┌──────────────────────┬──────────────┬──────────┐
│ Story                │ Status       │ Owner    │
├──────────────────────┼──────────────┼──────────┤
│ combat-parry-impl    │ In-Progress  │ Truong   │
│ combat-block-tune    │ Ready        │ —        │
│ ui-menu-polish       │ Blocked (GD) │ Truong   │
└──────────────────────┴──────────────┴──────────┘
TL;DR: 1 in progress, 1 blocked on GD, 1 ready. Unblock ui-menu-polish today.
```

## Rules

- Never edit files
- Never spawn subagents
- If no sprint folder found, report and suggest `/sprint-plan`
