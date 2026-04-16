---
name: adopt
description: Retrofit existing GDD documents into the ugk 7-section format. Reads from Design/GDD/, writes retrofit output to Docs/Retrofit/retrofit-<name>.md — original GDD is never modified.
---

# /adopt -- Retrofit Existing GDDs to Kit Format

## What this command does

Scans `Design/GDD/` for existing markdown documents and converts them into the ugk 7-section GDD format. **The original GDD is never modified.** Retrofit output is written to `Docs/Retrofit/retrofit-<name>.md`, preserving the Game Designer's raw document as the source of truth.

After retrofit (all 7 sections complete, cross-reviewed, gate passed), the retrofit file serves as the implementation spec consumed by speckit in Phase 4. Any mood, tone, or creative-framing content found in existing docs does NOT belong in retrofit output — relocate it to the concept doc (`Design/GDD/game-concept.md`). Never invent or re-add non-implementation-actionable sections during retrofit.

## File path convention

- **Input** (read-only): `Design/GDD/<name>.md` — raw GDD from Game Designer, any format
- **Output**: `Docs/Retrofit/retrofit-<name>.md` — 7-section spec, created by `/adopt`
- Create `Docs/Retrofit/` directory if it doesn't exist

Example: `Design/GDD/combat.md` → `Docs/Retrofit/retrofit-combat.md`

## Process

1. **Scan** `Design/GDD/` for all `.md` files (excluding `game-concept.md` and `systems-index.md`).
2. **For each document**, analyze which of the 7 required sections are present:
   1. Overview
   2. Detailed Rules
   3. Formulas
   4. Edge Cases
   5. Dependencies
   6. Tuning Knobs
   7. Acceptance Criteria
3. **Present a gap report** -- a markdown table with one row per doc and one column per section. **Column headers MUST use the full section names** (`Overview`, `Detailed Rules`, `Formulas`, `Edge Cases`, `Dependencies`, `Tuning Knobs`, `Acceptance Criteria`, `Severity`) — do NOT abbreviate to codes like `1-Ov`, `4-Fo`, etc. Use these status markers:
   - ✅ = present (section exists and meets quality bar)
   - 🟡 = partial (section exists but incomplete)
   - ❌ = missing (no section at all)
   - ➖ = N/A with justification (valid, not a gap — see N/A rules below)

   Flag any non-implementation content (e.g. mood/tone/creative framing) as candidates to relocate to the concept doc.

4. **Classify gaps by severity** (after the gap report table):
   - **BLOCKING**: Missing AC or Detailed Rules — cannot generate implementation spec without these
   - **HIGH**: Missing Formulas on a system that performs calculations — stories will have wrong acceptance criteria
   - **MEDIUM**: Missing Tuning Knobs, partial Edge Cases — quality degradation but not pipeline-breaking
   - **LOW**: Missing optional sections — nice-to-have

   Present severity summary: "BLOCKING: N, HIGH: N, MEDIUM: N, LOW: N"
   If BLOCKING > 0: "⚠️ These GDDs cannot serve as implementation specs until BLOCKING gaps are resolved."

5. **For each document with gaps** (user chooses order):
   a. Show existing content mapped to the closest section
   b. **Check AC quality** during retrofit:
      - Are acceptance criteria in Given-When-Then format? If not, flag as gap.
      - Count AC vs core rules vs player-facing formulas — if coverage < 1:1, flag as gap.
      - Are criteria independently verifiable (no references to "as described in Overview")? If not, flag.
   c. **Handle N/A-eligible sections** (Formulas, Edge Cases, Tuning Knobs):
      - If a section appears genuinely not applicable, ask the user: "Does this system have [formulas/edge cases/tuning knobs]?"
      - If user confirms N/A → require a one-sentence justification → write "N/A — [justification]"
      - Sections that CANNOT be N/A: Overview, Detailed Rules, Dependencies, Acceptance Criteria
   d. Draft missing sections based on context from existing content
   e. User reviews and approves each section
   f. **Write the retrofit file** to `Docs/Retrofit/retrofit-<name>.md` — do NOT modify the original `Design/GDD/<name>.md`
   g. Add a header comment in the retrofit file: `<!-- Retrofitted from Design/GDD/<name>.md by /adopt -->`
6. **After all docs are processed**: suggest `/review-all-gdds` for cross-document consistency check, or `/gate-check systems` to validate the Systems Design phase.

## Output

Retrofit files in `Docs/Retrofit/` with all 7 sections populated (or explicitly marked N/A with justification). Original GDDs in `Design/GDD/` remain untouched.

## Collaboration protocol

Present section-by-section for approval. Preserve the author's voice and intent — only add structure, don't rewrite. The original GDD is never modified; all changes go to the retrofit file.

## Context awareness

This command can consume significant context window space. If context usage exceeds 70%:
1. Write any in-progress section to file immediately
2. Summarize remaining work
3. Suggest the user run `/compact` then resume

## Suggested next step

End with a "Suggested next step" block. Typical options:

- `/review-all-gdds` — cross-check consistency once all docs are retrofitted
- `/design-system <missing-system>` — author any system listed in `systems-index.md` but not yet in `Design/GDD/`
- `/gate-check systems` — once every MVP system has a complete 7-section GDD (or retrofit)
