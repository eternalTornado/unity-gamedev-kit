---
name: create-stories
description: Break a GDD or gap report into concrete stories ready for a sprint. Each story has acceptance criteria, estimate, test type, dependencies.
model: sonnet
---

# /create-stories — GDD/gap-report → stories

## Inputs

- `<source>` — path to `design/gdd/<file>.md` OR `production/gap-reports/<file>.md`
- `<sprint>` — optional target sprint (default: current)

## Workflow

1. **Read source**:
   - If GDD: use §3 Rules + §8 Acceptance Criteria as story seeds
   - If gap report: one story per gap (or cluster of related gaps)
2. **For each story, draft**:
   - ID (kebab-case, system-prefixed: `combat-parry-impl`)
   - Title (imperative, ≤10 words)
   - GDD ref (section + lines)
   - Acceptance criteria (copy from GDD §8, one per line)
   - Scope estimate: XS(<2h) / S(<4h) / M(<1d) / L(<2d) / XL(split!)
   - Test type: Logic / Integration / Visual / UI / Config
   - Dependencies (other story IDs)
   - Sub-specialist to spawn (e.g., gameplay-code, ui-code — per rules folder)
3. **Reject XL stories** — force user to split before proceeding.
4. **Order by dependency graph**. Flag parallelizable stories.
5. **Show draft list** → approve → write to `production/sprints/<sprint>/stories/<id>.md`.

## Story file template

```markdown
---
id: combat-parry-impl
title: Implement parry mechanic with 8-frame window
gdd: design/gdd/combat.md §3.5
gap-refs: [combat-G-01, combat-G-04]
scope: M
test-type: Logic
specialist: gameplay-code
dependencies: []
---

## Acceptance criteria
1. Parry window active for 8 frames (133ms @ 60fps)
2. i-frames applied during parry window
3. Successful parry triggers counter-attack state
4. SFX + VFX fire on successful parry

## Implementation notes
- Use existing InputBuffer for parry input
- Add PARRY state to PlayerStateMachine
- Config parry-frames via ScriptableObject (tuning knob)

## Test plan
- Unit: test_parry_window_active_8_frames
- Unit: test_parry_triggers_iframes
- Integration: test_parry_chains_to_counter
```

## Anti-patterns

- ❌ Monolithic "implement combat" story → split
- ❌ Story without GDD ref → reject, run `/design-system` first
- ❌ Vague acceptance ("combat feels good") → push back with question
