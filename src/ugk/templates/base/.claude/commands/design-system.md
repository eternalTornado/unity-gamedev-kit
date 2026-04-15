---
name: design-system
description: Authors a single-system GDD (combat, orbit, economy, etc.) with the 7 mandatory sections + Game Feel. Section-by-section with user approval; writes each section to file immediately.
---

# /design-system — Single System GDD Authoring

The GDD is the **feature spec** consumed by speckit in Phase 4 — it must be implementation-actionable. Mood/tone/fantasy belongs in `Design/GDD/game-concept.md`, not here.

## Required sections (enforced by validate-commit hook)

1. **Overview** — one paragraph.
2. **Detailed Rules** — unambiguous mechanical rules.
3. **Formulas** — every calculation with variable definitions, ranges, examples.
4. **Edge Cases** — explicit resolution (not "handle gracefully").
5. **Dependencies** — bidirectional (A refs B → B must ref A).
6. **Tuning Knobs** — designer-safe ranges per knob.
7. **Acceptance Criteria** — QA-testable pass/fail.

Plus **Game Feel** section: input responsiveness (ms/frames), animation timing (startup/active/recovery), impact moments, weight profile.

## Process

1. **Read all `.md` files in `Design/GDD/`** — understand full design context (concept, existing systems, dependencies). Look for a concept doc and systems index regardless of filename.

2. **Read any upstream/downstream system GDDs** to catch dependencies.

3. **Technical Feasibility Pre-Check** — flag if the system requires research or tech spike before design proceeds. If it does, suggest `/architecture-decision` or a research task first.

4. **Collect open questions in ONE batch** — if the user's ask has ambiguities (scope, scale, depth of mechanics), use the `AskUserQuestion` tool to batch them into one call (max 4 questions, 2-4 concrete options each). Do NOT ask free-form in chat unless the answer is truly open-ended (e.g., "describe the fantasy in your own words").

5. **For each of the 8 sections** (7 mandatory + Game Feel), in order:
   a. Present context (what upstream/downstream systems imply)
   b. Use `AskUserQuestion` for enumerable choices, free-form only when unavoidable
   c. Draft the section
   d. User approves
   e. **Write to file immediately**
   f. Update `Production/session-state/active.md` if relevant

6. After all sections: run `/design-review Design/GDD/<system>.md` automatically, or suggest it.

## File path convention

`Design/GDD/<kebab-case-system-name>.md`

## Collaboration protocol

- One section at a time. Never batch multiple sections without approval.
- Write immediately after approval — don't hold sections in conversation.
- Use `AskUserQuestion` for every enumerable choice; free-form only for open-ended content.

## Suggested next step

End with a "Suggested next step" block. Typical options:

- `/design-review Design/GDD/<system>.md` — validate this GDD against design theory
- `/design-system <next-system>` — draft the next system from `systems-index.md`
- `/review-all-gdds` — once 2+ system GDDs exist, cross-check consistency
- `/gate-check systems` — all MVP systems designed and cross-reviewed
