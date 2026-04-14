---
name: playtest-report
description: Structure a playtest session report with findings, bug reports, and balance observations. Writes to Production/qa/.
---

# /playtest-report -- Playtest Session Report

## What this command does

Helps the user document findings from a playtest session in a structured format that feeds into bug triage and balance tuning.

## Process

1. **Ask** session context:
   - Build version / branch
   - Playtest date and duration
   - Tester(s) -- internal, external, QA
   - Focus area (full game, specific system, specific level)
2. **Gather findings** -- ask the user to describe what they observed. Categorize each finding:
   - BUG: Something broken (crashes, incorrect behavior, visual glitches)
   - BALANCE: Something feels off (too easy, too hard, boring, unfair)
   - FEEL: Something about game feel (sluggish, unresponsive, satisfying)
   - UX: Confusion, unclear feedback, missing information
   - POSITIVE: Something that works well (important to preserve)
3. **For each BUG**, create a bug report file:
   - `Production/qa/BUG-<YYYY>-<NNNN>.md` with: description, repro steps, severity, affected system
4. **Write** playtest summary to `Production/qa/playtest-<date>.md`:
   - Session info
   - Findings by category (with links to bug reports)
   - Priority recommendations
   - Suggested next actions
5. Suggest: `/triage-bug` for critical bugs, `/balance-tune` for balance issues.

## Output

- `Production/qa/playtest-<date>.md` -- session report
- `Production/qa/BUG-<YYYY>-<NNNN>.md` -- per bug (if any)

## Collaboration protocol

Gather all findings conversationally first, then present the structured report for approval before writing files.
