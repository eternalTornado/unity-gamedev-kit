---
name: verify-against-doc
description: After a story is implemented, verify the new/modified code actually matches its GDD section. Run before /story-done as the final reconciliation check.
model: opus
---

# /verify-against-doc — Did the code actually implement the doc?

## When to use

- Right after `/dev-story` completes, BEFORE `/story-done`
- When reviewing a PR that claims to close a gap
- As a final audit before `/design-lock`

## Inputs

- `<story-id>` or `<pr-files>` — list of files changed
- `<gdd-file>` — the GDD section the story maps to

## Workflow

1. **Read the GDD section** referenced by the story.
2. **Read the changed files** (from git diff or story metadata).
3. **Extract acceptance criteria** from §8 of GDD.
4. **Verify each criterion** against code:
   - Named mechanics present? (class/method names match)
   - Formulas match? (constants, coefficients)
   - Edge cases handled? (null checks, bounds, i-frames)
   - Tuning values align?
5. **Check test coverage**: does a test exist that proves the criterion?
6. **Verdict** per criterion: ✅ PASS / ⚠️ PARTIAL / ❌ FAIL.
7. **Report** — ask approval → write to `production/verification/<story-id>.md`.

## Verdict report format

```markdown
# Verification: <story-id> vs design/gdd/<system>.md
**Date:** 2026-04-13  **Overall:** PARTIAL (4/5 pass)

## Acceptance criteria
| # | Criterion | Verdict | Evidence |
|---|-----------|---------|----------|
| 1 | Parry window = 8 frames | ✅ PASS | `PlayerParry.cs:23` const PARRY_FRAMES = 8 |
| 2 | i-frames during parry | ✅ PASS | `PlayerHealth.cs:45` IsInvincible flag + test |
| 3 | SFX plays on success | ⚠️ PARTIAL | code present, no test |
| 4 | Cooldown 1.5s | ✅ PASS | ScriptableObject config, test verifies |
| 5 | Counter-attack damage 2x | ❌ FAIL | `CounterAttack.cs` uses 1.5x — off by one? |

## Recommendation
- Fix criterion 5 before `/story-done`
- Add test for criterion 3 (SFX) or mark as ADVISORY

## Next step
Either fix and re-run, or accept PARTIAL with explicit GD sign-off.
```

## Rules

- **FAIL blocks story-done** unless user explicitly waives with written rationale
- **PARTIAL** allowed but must be logged in story metadata
- Use Read/Grep extensively — do NOT rely on conversation memory of what code "should" say
- Always cite file:line for evidence

## Edge cases

- **GDD section is `[TBD]`**: skip verify, flag as "cannot verify until GDD complete"
- **Story spans multiple GDD sections**: verify each separately, combine verdicts
- **Criterion is visual/feel**: mark as ADVISORY (see test-standards.md) — require screenshot evidence instead
