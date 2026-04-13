---
name: triage-bug
description: Intake a bug report, classify severity, capture reproduction steps, produce a bug story ready for /dev-story.
model: sonnet
---

# /triage-bug — Bug intake

## Inputs

- `<description>` — free-text bug report from user/tester
- `<severity-hint>` — optional (user's guess)

## Workflow

1. **Clarify** (if missing):
   - Steps to reproduce
   - Expected vs actual behavior
   - Platform / build / Unity version
   - Frequency (always / intermittent / once)
   - Regression? (worked before, broken now — link commit if known)
2. **Classify severity**:
   - **CRIT** — crash, data loss, soft-lock, ship-blocker
   - **HIGH** — mechanic broken, major visual glitch
   - **MED** — edge-case bug, workaround exists
   - **LOW** — cosmetic, rare
3. **Classify type**: logic / visual / audio / performance / platform / networking
4. **Suggest specialist** to assign (gameplay-code, ui-code, etc.)
5. **Draft bug story** → approve → write to `production/bugs/<bug-id>.md` and promote into sprint if CRIT/HIGH.

## Bug story template

```markdown
---
id: bug-2026-0042
severity: HIGH
type: logic
specialist: gameplay-code
reported: 2026-04-13
reporter: QA
---

# Player falls through floor on Level 3

## Repro
1. Start Level 3
2. Sprint toward the northwest cliff
3. Jump at the marked spot

Expected: Player lands on cliff edge.
Actual: Player clips through floor into void.

## Environment
- Build: 0.8.2-rc
- Unity: 6000.0.28f1
- Platform: Windows editor + Standalone

## Frequency
Always reproducible at exact spot.

## Suspected cause
Collider gap at chunk boundary (Level3.unity lines around cliff prefab).

## Acceptance
- Player cannot clip through floor at the specified location
- Regression test covering chunk boundary colliders
```

## Rules

- CRIT bugs: refuse to accept without repro steps (too costly to guess)
- Always propose a regression test scenario
- Don't start fixing — that's `/dev-story`'s job
