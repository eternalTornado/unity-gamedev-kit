---
name: balance-tune
description: Safely adjust numeric balance values (HP, damage, drop rates, cooldowns) with rationale logged to GDD. Data-only changes, no code logic changes.
model: opus
---

# /balance-tune — Adjust balance values with audit trail

## When to use

- GD requests a numeric tweak ("boss HP -20%", "XP curve flatter")
- After playtest feedback on difficulty
- Never for logic changes — if formula changes, use `/design-system` instead

## Pre-check

Run `/scope-check` first. If it classifies as anything but XS (data-only), refuse and redirect.

## Workflow

1. **Locate value**:
   - Search ScriptableObjects, JSON configs, CSV data
   - NEVER touch hardcoded values in `.cs` — if hardcoded, flag as tech debt
2. **Read current value + spec §6 Tuning Knobs** (from `Docs/Retrofit/retrofit-<system>.md` or `Design/GDD/<system>.md`) — confirm in-range.
3. **Ask rationale**: "Why this change? (playtest / analytics / design intent)"
4. **Draft change set**:
   - File path
   - Before → After
   - GDD note to append
5. **Approve** → apply edit → update the spec file (`Docs/Retrofit/retrofit-<system>.md` or `Design/GDD/<system>.md`) §6 Tuning Knobs with timestamped note.
6. **Suggest regression check**: any test using old value?

## Output

```
Balance tune: boss HP
- File: Assets/Data/Balance/BossStats.asset
- maxHP: 2000 → 1600 (−20%)
- Rationale: playtest showed phase 2 too punishing
- GDD updated: design/gdd/combat.md §7 (log appended)

Regression note:
- test_boss_phase2_dps_window uses hp=2000 → needs update

Next: /regression-check combat
```

## Rules

- Each tune must have GD-approved rationale — log it
- Never tune in bulk without individual approval
- Never silently change: show diff first
- If value exceeds GDD range, warn and ask to update range before applying
