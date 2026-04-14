---
name: design-system
description: Authors a single-system GDD (combat, orbit, economy, etc.) with the 8 mandatory sections + Game Feel. Section-by-section with user approval; writes each section to file immediately.
---

# /design-system — Single System GDD Authoring

## Required sections (enforced by validate-commit hook)

1. **Overview** — one paragraph.
2. **Player Fantasy** — what the player imagines feeling.
3. **Detailed Rules** — unambiguous mechanical rules.
4. **Formulas** — every calculation with variable definitions, ranges, examples.
5. **Edge Cases** — explicit resolution (not "handle gracefully").
6. **Dependencies** — bidirectional (A refs B → B must ref A).
7. **Tuning Knobs** — designer-safe ranges per knob.
8. **Acceptance Criteria** — QA-testable pass/fail.

Plus **Game Feel** section: input responsiveness (ms/frames), animation timing (startup/active/recovery), impact moments, weight profile.

## Process

1. Read ALL `.md` files in `Design/GDD/` to understand the full design context (concept, existing systems, dependencies). Look for a concept doc and systems index regardless of filename.
2. Read any upstream/downstream system GDDs to catch dependencies.
3. **Technical Feasibility Pre-Check** — flag if the system requires research or tech spike before design proceeds.
4. For each section (in order):
   a. Present context
   b. Ask questions
   c. Present options
   d. User decides
   e. Draft section
   f. User approves
   g. Write to file immediately
5. After all sections: suggest `/design-review Design/GDD/<system>.md`.

## File path convention

`Design/GDD/<kebab-case-system-name>.md`

## Collaboration protocol

One section at a time. Never batch multiple sections without approval. Write immediately after approval — don't hold sections in conversation.
