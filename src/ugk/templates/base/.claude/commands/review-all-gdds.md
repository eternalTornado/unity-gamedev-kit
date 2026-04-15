---
name: review-all-gdds
description: Holistic cross-document review of all GDDs for consistency, dependency correctness, and design theory. Use before gate-check 2.
model: opus
---

# /review-all-gdds -- Cross-Document GDD Review

## What this command does

Reads every GDD in `Design/GDD/` and performs two independent review passes, then synthesizes findings into an actionable report.

## Process

### Phase 0: Scan (MANDATORY)

List ALL `.md` files in `Design/GDD/`. Read every file. Do not skip any. Report how many GDDs were found before proceeding.

### Phase 1: Consistency Check (can run in parallel with Phase 2)

For every pair of GDDs that share a dependency:
- Verify bidirectional references (A refs B and B refs A)
- Check formula variable names match across documents
- Check tuning knob ranges don't conflict
- Verify shared terminology is used consistently

### Phase 2: Design Theory Review (can run in parallel with Phase 1)

For each GDD individually:
- Do the Rules align with the pillars in `Design/GDD/game-concept.md`?
- Are formulas complete (no undefined variables, no magic numbers)?
- Are edge cases truly edge cases (not normal gameplay)?
- Are acceptance criteria testable by QA (not vague)?
- Does the system create interesting player decisions (not just busywork)?

### Phase 3: Synthesis

- Combine findings from Phase 1 and Phase 2
- Categorize issues: BLOCKING (must fix before Phase 3) vs ADVISORY (can fix later)
- Present findings as a numbered list with file paths and specific line references
- Suggest concrete fixes for each issue

## Output

Report printed to conversation. No file written unless user requests it.

## Collaboration protocol

Present the full report, then ask which issues the user wants to address. Offer to run `/update-gdd` for each document that needs changes.
