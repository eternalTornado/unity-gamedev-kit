---
name: story-readiness
description: Verify a story has enough information to start development — GDD reference, acceptance criteria, scope, test type. Gate before /dev-story.
model: sonnet
---

# /story-readiness — Is this story ready to code?

## When to use

Before `/dev-story`. Prevents starting work on an underspecified story.

## Checklist (all must pass)

1. **GDD reference**: story links to `design/gdd/<file>.md` section
2. **Acceptance criteria**: ≥1 testable criterion from GDD §8
3. **Scope**: story fits in a reasonable timebox (not "implement the entire combat system")
4. **Dependencies**: any blocking stories are Done or parallel-safe
5. **Test type declared**: Logic / Integration / Visual / UI / Config (per test-standards.md)
6. **No `[TBD]` or `???` in the story body**
7. **GD confirmed ambiguities** (if from a gap report)

## Output

```
Story: combat-parry-impl
Status: READY ✅

Checks:
✅ GDD ref: design/gdd/combat.md §3.5
✅ 3 acceptance criteria, all testable
✅ Scope: ~4h, fits sprint
✅ No blockers
✅ Test type: Logic (unit test required)
✅ No [TBD]
✅ GD signed off on parry window value

Next: /dev-story combat-parry-impl
```

or

```
Status: BLOCKED ❌
- Missing test type declaration
- Acceptance criterion 2 references [TBD] — run /clarify-gaps
```

## Rules

- Read-only
- Return verdict + list — do not fix anything
- If BLOCKED, suggest the specific skill to unblock (e.g. `/clarify-gaps`, `/design-system`)
