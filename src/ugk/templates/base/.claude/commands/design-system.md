---
name: design-system
description: Authors a single-system GDD with the 7 mandatory sections. Section-by-section with user approval; writes each section to file immediately. Quality rubrics in design-system-rubrics.md.
---

# /design-system — Single System GDD Authoring

After retrofit and `/gate-check systems` PASS, the completed GDD serves as the **feature spec** consumed by speckit in Phase 4 — it must be implementation-actionable. Mood/tone/creative framing belongs in `Design/GDD/game-concept.md`, not here.

**Quality rubrics**: See `design-system-rubrics.md` for detailed format requirements (AC, Formulas, Edge Cases).

## Required sections (7 mandatory)

1. **Overview** — one paragraph.
2. **Detailed Rules** — unambiguous mechanical rules.
3. **Formulas** — every calculation with variable table, ranges, examples. See rubrics.
4. **Edge Cases** — explicit "If [condition]: [outcome]" format. See rubrics.
5. **Dependencies** — bidirectional (A refs B → B must ref A).
6. **Tuning Knobs** — designer-safe ranges per knob.
7. **Acceptance Criteria** — Given-When-Then format, 1:1 coverage. See rubrics.

## N/A-eligible sections

Formulas, Edge Cases, and Tuning Knobs may be marked N/A if the system genuinely has no content for them. For each N/A-eligible section, the agent MUST ask:
- "Does this system have [formulas/tuning knobs/edge cases]?"
- If user says no → require a one-sentence justification → write "N/A — [justification]"
- Sections that CANNOT be N/A: Overview, Detailed Rules, Dependencies, Acceptance Criteria.

## Process

1. **Read all `.md` files in `Design/GDD/`** — understand full design context (concept, existing systems, dependencies). Look for a concept doc and systems index regardless of filename.

2. **Read any upstream/downstream system GDDs** to catch dependencies.

3. **Technical Feasibility Pre-Check** — flag if the system requires research or tech spike before design proceeds. If it does, suggest `/architecture-decision` or a research task first.

4. **Collect open questions in ONE batch** — if the user's ask has ambiguities (scope, scale, depth of mechanics), use the `AskUserQuestion` tool to batch them into one call (max 4 questions, 2-4 concrete options each). Do NOT ask free-form in chat unless the answer is truly open-ended (e.g., "describe the system's intended experience in your own words").

5. **For each of the 7 sections**, in order:
   a. Present context (what upstream/downstream systems imply)
   b. For N/A-eligible sections (Formulas, Edge Cases, Tuning Knobs): ask user if this section applies before drafting
   c. Use `AskUserQuestion` for enumerable choices, free-form only when unavoidable
   d. Draft the section (following quality rubrics from `design-system-rubrics.md`)
   e. User approves
   f. **Write to file immediately**
   g. Update `Production/session-state/active.md` if relevant

6. After all sections: run `/design-review Design/GDD/<system>.md` automatically, or suggest it.

## File path convention

`Design/GDD/<kebab-case-system-name>.md`

## Collaboration protocol

- One section at a time. Never batch multiple sections without approval.
- Write immediately after approval — don't hold sections in conversation.
- Use `AskUserQuestion` for every enumerable choice; free-form only for open-ended content.

## Context awareness

This command can consume significant context window space. If context usage exceeds 70%:
1. Write any in-progress section to file immediately
2. Summarize remaining work
3. Suggest the user run `/compact` then resume

## Suggested next step

End with a "Suggested next step" block. Typical options:

- `/design-review Design/GDD/<system>.md` — validate this GDD against design theory
- `/design-system <next-system>` — draft the next system from `systems-index.md`
- `/review-all-gdds` — once 2+ system GDDs exist, cross-check consistency
- `/gate-check systems` — all MVP systems designed and cross-reviewed
