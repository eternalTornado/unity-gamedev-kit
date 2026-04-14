---
name: patch-notes
description: Generate player-facing patch notes from closed stories, resolved bugs, and balance tunes since last release.
model: sonnet
---

# /patch-notes — Build release notes

## Inputs

- `<since>` — git ref (tag/commit) for "last release"
- `<audience>` — `player` (default) | `internal` | `press`

## Workflow

1. Read `production/sprints/*/done/` stories since baseline.
2. Read `production/bugs/closed/` entries since baseline.
3. Read `design-locks` changelogs since baseline.
4. Group by category: New / Improved / Fixed / Balance / Known issues.
5. Rewrite per audience (player = excited + non-technical).
6. Draft → approve → write to `production/releases/<version>-notes.md`.

## Template

```markdown
# v0.9.1 — April 13, 2026

## ✨ New
- Parry! Time your defense for massive counter-attacks.

## 🛠️ Improved
- Boss fight pacing refined based on your feedback.

## 🐛 Fixed
- No more falling through the floor on Level 3.
- Save file corruption on mid-air quit.

## ⚖️ Balance
- Boss HP reduced 20% for phase 2.

## Known issues
- Occasional audio hitch on level load — fix in next patch.
```

## Rules

- Never quote internal story IDs in player-facing output
- Never leak in-progress features
- Internal audience: include story IDs + commit SHAs
