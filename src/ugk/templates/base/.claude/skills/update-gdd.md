---
name: update-gdd
description: Apply clarifications or decisions back into an existing GDD. Use after /clarify-gaps returns answers, or when GD decides a value mid-sprint.
model: sonnet
---

# /update-gdd — Write decisions back to the GDD

## Inputs

- `<gdd-file>` — target GDD
- `<decisions>` — list of decisions (from `/clarify-gaps` output or inline)

## Workflow

1. **Read current GDD** + **8-section structure**.
2. For each decision:
   - Locate correct section
   - Draft the edit (addition, replacement, or removal)
   - Preserve section ordering and heading levels
3. **Show diff** → approve → apply edits via Edit tool.
4. **Append changelog entry** at bottom of GDD:
   ```
   ## Changelog
   - 2026-04-13 — Parry window set to 8 frames (Q2 decision) — GD: Minh
   ```
5. **Suggest next**: `/design-review` if changes are substantial, or straight to `/create-stories`.

## Rules

- Every update must carry a rationale + author
- Never silently rewrite — always surface diff
- Preserve any `[TBD]` markers the user didn't explicitly resolve
- If decision conflicts with existing GDD content, flag the conflict and ask before choosing
