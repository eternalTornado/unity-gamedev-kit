---
name: adopt
description: Retrofit existing GDD documents into the ugk 7-section format. Use when a project has design docs that predate ugk installation.
---

# /adopt -- Retrofit Existing GDDs to Kit Format

## What this command does

Scans `Design/GDD/` for existing markdown documents and helps convert them into the ugk 7-section GDD format, preserving all existing content while adding missing sections.

The 7-section GDD is the implementation spec consumed by speckit in Phase 4. Any mood, tone, or creative-framing content found in existing docs does NOT belong in per-system GDDs — relocate it to the concept doc (`Design/GDD/game-concept.md`) and drop it from the GDD. Never invent or re-add non-implementation-actionable sections during retrofit.

## Process

1. **Scan** `Design/GDD/` for all `.md` files.
2. **For each document**, analyze which of the 7 required sections are present:
   1. Overview
   2. Detailed Rules
   3. Formulas
   4. Edge Cases
   5. Dependencies
   6. Tuning Knobs
   7. Acceptance Criteria
3. **Present a gap report** -- a markdown table with one row per doc and one column per section. **Column headers MUST use the full section names** (`Overview`, `Detailed Rules`, `Formulas`, `Edge Cases`, `Dependencies`, `Tuning Knobs`, `Acceptance Criteria`) — do NOT abbreviate to codes like `1-Ov`, `4-Fo`, etc. Use ✅ for present, 🟡 for partial, ❌ for missing. Flag any non-implementation content (e.g. mood/tone/creative framing) as candidates to relocate to the concept doc.
4. **For each document with gaps** (user chooses order):
   a. Show existing content mapped to the closest section
   b. Draft missing sections based on context from existing content
   c. User reviews and approves each section
   d. Write the reformatted document back to the same file
5. **After all docs are processed**: suggest `/review-all-gdds` for cross-document consistency check, or `/gate-check systems` to validate the Systems Design phase.

## Output

Reformatted GDD files in `Design/GDD/` with all 7 sections populated.

## Collaboration protocol

Never overwrite existing content without showing the diff first. Present section-by-section for approval. Preserve the author's voice and intent -- only add structure, don't rewrite.

## Suggested next step

End with a "Suggested next step" block. Typical options:

- `/review-all-gdds` — cross-check consistency once all docs are retrofitted
- `/design-system <missing-system>` — author any system listed in `systems-index.md` but not yet in `Design/GDD/`
- `/gate-check systems` — once every MVP system has a complete 7-section GDD
