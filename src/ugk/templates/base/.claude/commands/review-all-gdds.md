---
name: review-all-gdds
description: Holistic cross-document review of all GDDs for consistency, dependency correctness, and design theory. Use before gate-check 2.
model: opus
---

# /review-all-gdds -- Cross-Document GDD Review

## What this command does

Reads every GDD spec and performs two independent review passes, then synthesizes findings into an actionable report. Specs may be in two locations:
- `Docs/Retrofit/retrofit-<name>.md` — retrofit output from `/adopt` (preferred if exists)
- `Design/GDD/<name>.md` — agent-authored GDDs already in 7-section format

## Process

### Phase 0: Scan (MANDATORY)

List ALL `.md` files in `Design/GDD/` AND `Docs/Retrofit/`. For each system, use the retrofit file if it exists, otherwise use the raw GDD. Read every file. Do not skip any. Report how many specs were found (and how many are retrofits vs raw) before proceeding.

### Phase 1: Consistency Check (can run in parallel with Phase 2)

For every pair of GDDs that share a dependency:
- Verify bidirectional references (A refs B and B refs A)
- Check formula variable names match across documents
- Check tuning knob ranges don't conflict
- Verify shared terminology is used consistently

### Phase 2: Design Theory Review (can run in parallel with Phase 1)

For each GDD individually:
- Do the Rules align with the pillars in `Design/GDD/game-concept.md`?
- Are formulas complete (no undefined variables, no magic numbers)? Do they follow the variable table format (see `design-system-rubrics.md`)?
- Are edge cases truly edge cases (not normal gameplay)? Do they use "If [condition]: [outcome]" format?
- **AC quality check**:
  - Are acceptance criteria in Given-When-Then format?
  - Does each core rule have at least one AC?
  - Does each player-facing formula have at least one AC?
  - Are criteria verifiable without reading the rest of the GDD?
  - Is there a performance budget criterion (frame time, memory, or "N/A — no runtime cost")?
- Does the system create interesting player decisions (not just busywork)?
- Are N/A sections (if any) properly justified? Do they have a one-sentence explanation?

### Phase 3: Synthesis

- Combine findings from Phase 1 and Phase 2
- Categorize issues: BLOCKING (must fix before Phase 3) vs ADVISORY (can fix later)
- Present findings as a numbered list with file paths and specific line references
- Suggest concrete fixes for each issue

## Output

Report printed to conversation. No file written unless user requests it.

## Collaboration protocol

Present the full report, then ask which issues the user wants to address. Offer to run `/update-gdd` for each document that needs changes.

## Context awareness

This command can consume significant context window space. If context usage exceeds 70%:
1. Write any in-progress section to file immediately
2. Summarize remaining work
3. Suggest the user run `/compact` then resume
