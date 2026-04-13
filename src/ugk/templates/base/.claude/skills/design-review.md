---
name: design-review
description: Peer-review a GDD for completeness, clarity, testability, and internal consistency. Use after /design-system drafts a new section.
model: sonnet
---

# /design-review — Peer review a GDD

## Inputs

- `<gdd-file>` — the GDD to review

## Workflow

1. **Read the full GDD**.
2. **Check 8-section completeness**: Overview, Player Fantasy, Detailed Rules, Formulas, Edge Cases, Dependencies, Tuning Knobs, Acceptance Criteria (+ Game Feel).
3. **Per-section quality checks**:
   - **Rules**: unambiguous? measurable? no hand-waving?
   - **Formulas**: all variables defined? units specified?
   - **Edge Cases**: ≥3 listed? boundary conditions covered?
   - **Dependencies**: named systems verified to exist?
   - **Tuning Knobs**: ranges specified? default values?
   - **Acceptance Criteria**: each one testable? tied to a formula or rule?
4. **Consistency checks**:
   - Player Fantasy aligns with Rules (doesn't promise something Rules don't deliver)
   - Formulas support the stated Rules
   - No section contradicts another
5. **Flag anti-patterns**:
   - "feels good", "fun", "polished" without measurable criteria
   - Magic numbers not linked to tuning knobs
   - Copy-paste from another GDD without adaptation
6. **Write review** → approve → `production/design-reviews/<system>-<date>.md`.

## Review report format

```markdown
# Design Review: combat.md
**Reviewer:** Claude (advisory)
**Verdict:** CONCERNS (3 must-fix, 4 nits)

## Must-fix (before implementation)
1. §4 Formula uses undefined variable `attack_base` — clarify source
2. §5 Edge Cases missing: what happens if parry input during death animation?
3. §8 Criterion 3 not testable ("parry feels tight") — replace with frame count

## Nits (optional)
- §1 Overview 2 paragraphs, should be 1
- §7 Tuning Knob `parry_window` has no range (suggest 4–12 frames)

## Cross-section consistency
✅ Fantasy aligns with Rules
⚠️ Formula §4 implies 0.5 damage floor, not stated in Rules

## Recommendation
Run `/update-gdd` to address must-fix items, then re-review.
```

## Verdict tiers

- **PASS** — ready for `/create-stories`
- **CONCERNS** — fix must-fixes, proceed after update
- **FAIL** — fundamental issues, re-design needed
