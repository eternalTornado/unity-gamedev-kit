---
name: design-lock
description: Tag a baseline where GDD and code are verified in sync. Creates a restore point for the next /diff-design cycle. Essential for doc-code-sync teams to avoid drift.
model: opus
---

# /design-lock — Lock "doc == code" as a checkpoint

## When to use

- After `/code-audit` returns 0 gaps (or only accepted advisory gaps)
- End of a sprint where all stories verified with `/verify-against-doc`
- Before a release — proves the shipped build matches documented design

## Inputs

- `<gdd-file>` or `<system>` — the system/GDD being locked
- `<tag-name>` — optional semantic tag (default: `<system>-v<N>` auto-incremented)

## Workflow

1. **Pre-flight checks** (ALL must pass, else refuse to lock):
   - `/code-audit <gdd-file>` run within last 24h with 0 HIGH/MED gaps
   - No unmerged PRs touching the system
   - Git working tree clean on the branch being locked
2. **Compute lock metadata**:
   - GDD file SHA (git hash-object)
   - Code commit SHA for the system folder (git rev-parse HEAD)
   - Test run result (latest CI status if available)
3. **Write lock record** → ask approval → append to `production/design-locks/<system>.md`.
4. **Optionally git-tag** (asks user): `<system>-v<N>` pointing at HEAD.

## Lock record format

```markdown
# Design Locks: <system>

## Lock #3 — 2026-04-13
**Tag:** combat-v2
**GDD:** design/gdd/combat.md @ sha a1b2c3d
**Code:** commit 4e5f6g7 (Assets/Scripts/Combat/**)
**Audit:** 0 gaps (production/gap-reports/combat-2026-04-13.md)
**Tests:** 42/42 pass (CI run #127)
**Locked by:** Truong (Dev) with GD sign-off from Minh

### Notable state
- Parry mechanic: implemented with 8-frame window
- Block reduction: 0.7 (new value from v2.1)
- Stagger: removed
```

## Why lock matters

Next time GD updates the GDD, `/diff-design` uses this lock as the baseline — you diff only the NEW changes, not 6 months of accumulated drift. Without locks, every audit re-audits the entire history.

## Rules

- ❌ Never lock with HIGH or MED gaps open
- ❌ Never lock unilaterally if GD is the source of truth — get GD sign-off
- ✅ Prefer git tags for major locks (release candidates)
- ✅ Keep lock records permanent (gitignored folder? NO — commit them)

## After locking

Recommend to user:
- Close the sprint's gap report and verifications
- Update `production/session-state/active.md` to remove this system from "in flux"
- If shipping: create patch notes from the diff since previous lock
