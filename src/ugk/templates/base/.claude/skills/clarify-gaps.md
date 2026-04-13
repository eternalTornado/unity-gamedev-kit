---
name: clarify-gaps
description: Generate a prioritized question list for the Game Designer to resolve ambiguous gaps. Essential for GD+Dev teams with no Producer — Dev drives reconciliation by asking the right questions.
model: sonnet
---

# /clarify-gaps — Ask GD the right questions

## When to use

- After `/code-audit` or `/gap-report` — gaps exist with verdict `TBD` or `AMBIGUOUS`
- Before `/create-stories` — you need GD sign-off per gap
- Any time GD says "figure it out" — push back with a concrete question list

## Inputs

- `<gap-report-file>` — the report with TBD/AMBIGUOUS verdicts
- `<audience>` — optional (default: `GD`); can be `tech-lead`, `producer`, `all`

## Workflow

1. **Read gap report**, filter gaps where verdict is TBD / AMBIGUOUS / unresolved.
2. **For each gap, draft ONE question**:
   - Closed question preferred (yes/no, pick option A/B/C)
   - Include context: what the doc says vs what the code does
   - Offer a **default answer** so GD can "👍" if busy
3. **Group questions** by topic (combat, UI, etc.) and urgency.
4. **Format for async delivery** (copy-paste into Slack/Notion/email).
5. **Draft** → show user → approve → write to `production/clarifications/<system>-<date>.md`.

## Question list format

```markdown
# Clarifications needed — <system>
**From:** Dev  **To:** GD
**Blocking:** Sprint planning for <date>
**How to respond:** Reply inline with ✅ for default or alternative letter.

---
## Q1 (G-03 ORPHAN) — Stagger mechanic
**Context:** Doc v2.1 removed Stagger from §3. Code still has `StaggerHandler.cs` (used by 2 enemies).
**Question:** Do we remove Stagger entirely, or keep as hidden enemy-only mechanic?
- A. Remove completely (delete code + assets) ✅ **default**
- B. Keep for enemies, remove player-facing
- C. Keep as-is, update doc

## Q2 (G-04 AMBIGUOUS) — Parry window
**Context:** Doc §3.5 says "short parry window". Need exact value.
**Question:** Parry active frames?
- A. 8 frames @ 60fps = 133ms ✅ **default**
- B. 6 frames = 100ms (tighter)
- C. 10 frames = 166ms (more forgiving)

---
## Batched decisions (low-impact, respond 👍 to accept all defaults)
- Q5 SFX volume for parry → default 0.8
- Q6 VFX color → default cyan (#4FC3F7)
```

## Tone rules

- Respectful of GD's time — default answers ALWAYS
- No jargon unless GD uses it
- One question per gap — never multi-part
- Never passive-aggressive ("as mentioned in the doc you wrote...")

## After GD responds

User should update the gap report with verdicts (IMPLEMENT / UPDATE DOC / DROP) and optionally re-run `/gap-report` to produce a clean version for `/create-stories`.

## Edge cases

- **GD unavailable for days**: flag in report as "Dev-decided, pending GD confirm" — move on but log it.
- **Question has no good default**: that's fine — mark with ❓ and explain trade-off.
- **Conflict between 2 GDD sections**: elevate as separate question about doc consistency.
