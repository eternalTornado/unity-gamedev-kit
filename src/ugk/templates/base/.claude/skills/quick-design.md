---
name: quick-design
description: Rapid GDD-lite for small features that don't need a full 8-section doc. Overview + Rules + Tuning only. Escape hatch for tweaks.
model: sonnet
---

# /quick-design — GDD-lite for small features

## When to use

- Small polish/feel tweaks (screen shake, SFX, particle tweaks)
- Single-function features that don't ripple to other systems
- Scope-check classified as S or M with no cross-system impact

## NOT for

- Anything that changes balance formulas → `/design-system`
- Anything that adds a new player-facing mechanic → `/design-system`
- Anything scope-checked as L or XL

## Workflow

1. **Ask 3 questions**:
   - What's the player-facing change in 1 sentence?
   - What triggers it / when does it happen?
   - What values can be tuned?
2. **Draft 3-section doc**:
   - **Overview** (2–3 sentences)
   - **Rules** (trigger, behavior, duration)
   - **Tuning Knobs** (values + ranges)
3. **Show draft** → approve → write to `design/gdd-quick/<feature>.md`.
4. **Suggest next**: usually `/create-stories` directly (skip design-review for quick designs).

## Quick-design template

```markdown
---
type: quick-design
parent-gdd: design/gdd/juice.md
---

# Hit screen shake

## Overview
When the player takes damage, camera shakes briefly to reinforce impact.

## Rules
- Trigger: `PlayerHealth.OnDamage` event
- Duration: `shake_duration` seconds
- Intensity scales with damage / maxHealth
- Suppressed during cutscenes and UI modals

## Tuning Knobs
| Knob | Default | Range |
|------|---------|-------|
| shake_duration | 0.15s | 0.05–0.4s |
| shake_amplitude | 0.3 | 0.1–0.8 |
| shake_frequency | 30Hz | 20–60Hz |
```

## Rules

- Quick designs live in `design/gdd-quick/`, not `design/gdd/` — easy to upgrade to full GDD later
- Link to parent GDD in frontmatter so audits know the context
- Never use `/quick-design` for multi-file changes
