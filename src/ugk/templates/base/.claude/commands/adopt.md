---
name: adopt
description: Retrofit existing GDD documents into the ugk 8-section format. Use when a project has design docs that predate ugk installation.
---

# /adopt -- Retrofit Existing GDDs to Kit Format

## What this command does

Scans `Design/GDD/` for existing markdown documents and helps convert them into the ugk 8-section GDD format, preserving all existing content while adding missing sections.

## Process

1. **Scan** `Design/GDD/` for all `.md` files.
2. **For each document**, analyze which of the 8 required sections are present:
   1. Overview
   2. Player Fantasy
   3. Detailed Rules
   4. Formulas
   5. Edge Cases
   6. Dependencies
   7. Tuning Knobs
   8. Acceptance Criteria
3. **Present a gap report** -- table showing each doc and which sections are missing/present.
4. **For each document with gaps** (user chooses order):
   a. Show existing content mapped to the closest section
   b. Draft missing sections based on context from existing content
   c. User reviews and approves each section
   d. Write the reformatted document back to the same file
5. **After all docs are processed**: suggest `/review-all-gdds` for cross-document consistency check, or `/gate-check 2` to validate Phase 2 completion.

## Output

Reformatted GDD files in `Design/GDD/` with all 8 sections populated.

## Collaboration protocol

Never overwrite existing content without showing the diff first. Present section-by-section for approval. Preserve the author's voice and intent -- only add structure, don't rewrite.
