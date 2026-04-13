---
name: regression-check
description: Verify a change didn't break existing functionality. Runs test suite, compares against baseline, flags likely regressions.
model: sonnet
---

# /regression-check — Did we break anything?

## When to use

- After `/balance-tune` (numeric change could ripple)
- After bug fix (ensure fix didn't introduce new bug)
- Before merge to main
- Before `/design-lock`

## Workflow

1. **Determine scope**:
   - Changed files (`git diff`)
   - Systems touched (via path → rule mapping)
2. **Identify impacted tests**:
   - Unit tests in `tests/unit/<system>/`
   - Integration tests referencing changed symbols
   - Smoke tests for affected gameplay loops
3. **Run tests** (engine-specific):
   - Godot: `godot --headless --script tests/gdunit4_runner.gd`
   - Unity: `game-ci/unity-test-runner` or Test Runner window
4. **Compare to baseline** (last green run on main).
5. **Flag suspicious patterns**:
   - Tests that pass but warn about deprecated APIs
   - Tests that pass with wider tolerance than before
   - Tests that skip (silent failure)
6. **Write report** → `production/regression-reports/<date>.md`.

## Report format

```
Regression check: 2026-04-13
Changed: Assets/Scripts/Combat/BlockController.cs
Impacted systems: combat
Tests run: 38 (28 pass / 0 fail / 10 skipped)

⚠️ Concerns:
- test_block_reduction_at_50_percent SKIPPED — is this related to the tune?
- test_combo_chain warned about frame-time variance

✅ No regressions detected in combat.
⚠️ Verify skipped test intentional.
```

## Rules

- NEVER mark "no regression" if tests were skipped without explanation
- If tests fail, do NOT auto-fix — surface to user
- Always re-run on clean state (no uncommitted changes unrelated to the tune)
