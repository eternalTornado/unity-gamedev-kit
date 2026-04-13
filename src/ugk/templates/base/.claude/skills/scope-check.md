---
name: scope-check
description: Classify a new task/change by scope and cross-system impact BEFORE committing to design or implementation. The "clarify-before-specify" gate.
model: sonnet
---

# /scope-check — How big is this, really?

## When to use

- Right when a task lands ("add dash", "tune boss HP", "new co-op mode")
- Before deciding whether to run `/quick-design` or full `/design-system`
- Before any `/balance-tune` — verify it's truly data-only

## Workflow

1. **Ask 5 clarifying questions** (if not already answered):
   - What system does this touch?
   - Does it change formulas or behavior, or just values?
   - Does it affect other systems? (combat, UI, save, network)
   - Is there an existing GDD section, or does one need to be written?
   - Is this permanent or a playtest experiment?
2. **Classify**:
   - **XS (data-only)** → `/balance-tune`
   - **S (single-system feature, GDD exists)** → `/create-stories` directly
   - **M (single-system feature, no GDD)** → `/quick-design` → `/create-stories`
   - **L (multi-system feature)** → `/design-system` + `/propagate-design-change`
   - **XL (new pillar)** → `/brainstorm` → `/design-system`
3. **Flag risk**: shipping timeline, test coverage impact, balance ripple.
4. **Recommend** the next skill.

## Output

```
Task: "daily login reward"

Classification: L (multi-system)
Touches: save system, UI main menu, inventory, anti-cheat
GDD exists: NO
Formula/data: both (reward curve + values)
Risk: MED — affects retention, needs playtest

Recommended flow:
1. /design-system daily-login-reward
2. /design-review (after GDD drafted)
3. /propagate-design-change (updates save/inventory/UI GDDs)
4. /create-stories
5. dev loop
```

## Rules

- No file writes — pure advisory
- Always bias UP one scope tier if ambiguous (under-scoping is more dangerous than over-scoping)
- If user pushes back on scope, document disagreement in output and proceed with their choice
