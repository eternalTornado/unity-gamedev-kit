---
name: gap-report
description: Aggregate multiple diff/audit outputs into a single prioritized gap report ready for sprint planning. Use when /diff-design and /code-audit both ran and you need one source of truth.
model: sonnet
---

# /gap-report — Consolidate gaps into one actionable list

## When to use

- After `/diff-design` AND `/code-audit` ran — you have 2 partial reports, need 1
- When auditing multiple GDD files at once (cross-system consolidation)
- Before running `/clarify-gaps` (clarify-gaps needs 1 consolidated input)

## Inputs

- One or more report files (gap-report or diff-report) OR a folder path
- `<sprint>` — optional sprint tag for filtering

## Workflow

1. **Read all input reports**. Merge gap IDs (rename collisions: G-01 → combat-G-01).
2. **De-duplicate**. If diff-report says "Parry added" and audit says "Parry missing", collapse into 1 gap.
3. **Prioritize** by: severity → gameplay impact → ship deadline.
4. **Cluster** related gaps into candidate Tasks (e.g., all parry gaps → Task A).
5. **Draft consolidated report** → ask approval → write to `production/gap-reports/consolidated-<date>.md`.

## Consolidated report format

```markdown
# Consolidated Gap Report — <date>
**Sources:** combat-2026-04-13.md, ui-2026-04-13.md
**Total gaps:** 12 (HIGH: 3, MED: 6, LOW: 3)
**Suggested Tasks:** 4

## Priority 1 — ship-blocking
- combat-G-01 (HIGH, MISSING): Parry mechanic
- combat-G-02 (HIGH, FORMULA): Block reduction drift

## Priority 2 — this sprint
- ui-G-04 (MED, AMBIGUOUS): "main menu feels slow"

## Priority 3 — backlog / next sprint
- combat-G-08 (LOW, ORPHAN): StaggerSound

## Candidate Tasks
### Task A: Combat v2 reconcile (4 gaps)
- combat-G-01, G-02, G-03, G-05
### Task B: UI polish (3 gaps)
- ui-G-04, G-06, G-07

## Open clarifications needed
- 5 gaps still AMBIGUOUS — run `/clarify-gaps` before planning
```

## Clustering heuristic

Group gaps into the same Task when:
- Same GDD section
- Same code file or tightly-coupled files
- Dependency chain (fixing G-01 unblocks G-05)
- Reviewable together in one PR

## Next step

Always recommend at the end: either `/clarify-gaps` (if ambiguous gaps remain) or `/create-stories` (if all gaps have verdict).
