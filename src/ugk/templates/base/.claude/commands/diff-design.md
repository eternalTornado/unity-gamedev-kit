---
name: diff-design
description: Diff two versions of a GDD (git-based) to extract what was added, changed, or removed. First step when GD updates a design doc and Dev needs to reconcile with code.
model: opus
---

# /diff-design — What changed in the GDD?

## When to use

- GD just updated `design/gdd/<system>.md` and notified Dev
- Before `/code-audit` — you need to know WHAT changed before comparing to code
- Before planning a Task: scope depends on delta size

## Inputs

- `<gdd-file>` — path to the GDD file (required)
- `<since>` — git ref to diff against (optional, default: previous commit touching this file)

## Collaboration Protocol

Ask BEFORE writing any output file: "May I write the diff report to `production/diff-reports/<system>-<date>.md`?"

## Workflow

1. **Locate baseline**. Run `git log --oneline -- <gdd-file>` to find last commit. If `<since>` provided, use it.
2. **Compute diff**. Run `git diff <since> HEAD -- <gdd-file>`.
3. **Classify changes** by GDD section (8 sections: Overview, Player Fantasy, Detailed Rules, Formulas, Edge Cases, Dependencies, Tuning Knobs, Acceptance Criteria + Game Feel):
   - **ADDED** — new section or new content
   - **MODIFIED** — changed rule/formula/value
   - **REMOVED** — deleted content
   - **RENAMED/REFACTORED** — content moved or restructured
4. **Flag high-risk changes**:
   - Formula changes (impact balance/gameplay)
   - Dependency additions (cross-system impact)
   - Acceptance criteria changes (test coverage impact)
5. **Draft report** → show user → ask approval → write to `production/diff-reports/<system>-<date>.md`.

## Report format

```markdown
# GDD Diff Report: <system>
**Baseline:** <git-sha-short> (<date>)
**Current:** HEAD (<date>)
**Summary:** +X added, ~Y modified, -Z removed

## Changes by section
### §3 Detailed Rules
- **ADDED** (line 42): "Dash has 8-frame i-frames..."
- **MODIFIED** (line 51): Block reduction 50% → 70%

### §4 Formulas
- **MODIFIED** (line 68): damage = atk * 1.5 → atk * base_mult (moved to Tuning)

## High-risk flags
- ⚠️ Formula change §4 → re-run balance tests
- ⚠️ Dependency added (Inventory) → check cross-system gap

## Next steps
Run `/code-audit <gdd-file>` to find gaps between new doc and code.
```

## Edge cases

- **GDD file is new** (no baseline): report as "all new" + suggest running `/code-audit` directly.
- **Outside git repo**: degrade gracefully — ask user to provide old version manually.
- **Binary or malformed diff**: bail out with clear error.

## Output

1 file: `production/diff-reports/<system>-<date>.md`. Summarize in chat with counts + flags.
