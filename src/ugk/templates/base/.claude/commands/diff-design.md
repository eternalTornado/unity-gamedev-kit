---
name: diff-design
description: Diff a retrofit spec (git-based) to extract what changed, or compare retrofit vs original GDD. First step when design evolves and Dev needs to reconcile with code.
model: opus
---

# /diff-design — What changed in the spec?

## When to use

- After a spec update (retrofit file or GDD was revised) and Dev needs to know what changed
- Before `/code-audit` — you need to know WHAT changed before comparing to code
- Before planning a task: scope depends on delta size

## Usage

```
/diff-design combat
/diff-design combat --since abc1234
/diff-design combat --against-gdd
```

## Inputs

- `<system-name>` — system to diff (resolves to `Docs/Retrofit/retrofit-<name>.md` first, fallback `Design/GDD/<name>.md`)
- `--since <git-ref>` — git ref to diff against (optional, default: previous commit touching this file)
- `--against-gdd` — compare the retrofit file against the original GDD in `Design/GDD/<name>.md` instead of git history. Shows what was added/changed during the retrofit process.

## Modes

### Default mode: git-diff the spec over time
Tracks how the retrofit spec (or GDD) has evolved across commits. Useful when someone updated the spec and Dev needs to reconcile.

### `--against-gdd` mode: retrofit vs original GDD
Compares `Docs/Retrofit/retrofit-<name>.md` against `Design/GDD/<name>.md`. Shows what the retrofit process added, restructured, or clarified compared to the raw GDD. Useful for reviewing retrofit quality or understanding what the GD's original intent was.

## Collaboration Protocol

Ask BEFORE writing any output file: "May I write the diff report to `Production/diff-reports/<system>-<date>.md`?"

## Workflow

### Default mode (git-diff)
1. **Locate spec file** — `Docs/Retrofit/retrofit-<name>.md` or `Design/GDD/<name>.md`.
2. **Locate baseline**. Run `git log --oneline -- <spec-file>` to find last commit. If `--since` provided, use it.
3. **Compute diff**. Run `git diff <since> HEAD -- <spec-file>`.
4. **Classify changes** by section (7 sections: Overview, Detailed Rules, Formulas, Edge Cases, Dependencies, Tuning Knobs, Acceptance Criteria):
   - **ADDED** — new section or new content
   - **MODIFIED** — changed rule/formula/value
   - **REMOVED** — deleted content
   - **RENAMED/REFACTORED** — content moved or restructured
5. **Flag high-risk changes**:
   - Formula changes (impact balance/gameplay)
   - Dependency additions (cross-system impact)
   - Acceptance criteria changes (test coverage impact)
6. **Draft report** → show user → ask approval → write to `Production/diff-reports/<system>-<date>.md`.

### `--against-gdd` mode
1. **Read** `Docs/Retrofit/retrofit-<name>.md` and `Design/GDD/<name>.md`.
2. **Compare section by section**: what was added, restructured, clarified, or dropped during retrofit.
3. **Flag**: sections that exist in retrofit but not in GDD (added by `/adopt`), content relocated to concept doc, N/A sections.
4. **Draft report** → show user → ask approval → write to `Production/diff-reports/<system>-retrofit-vs-gdd-<date>.md`.

## Report format

```markdown
# Spec Diff Report: <system>
**Baseline:** <git-sha-short> (<date>) OR original GDD
**Current:** HEAD (<date>) OR retrofit file
**Summary:** +X added, ~Y modified, -Z removed

## Changes by section
### §2 Detailed Rules
- **ADDED** (line 42): "Dash has 8-frame i-frames..."
- **MODIFIED** (line 51): Block reduction 50% → 70%

### §3 Formulas
- **MODIFIED** (line 68): damage = atk * 1.5 → atk * base_mult (moved to Tuning)

## High-risk flags
- ⚠️ Formula change §3 → re-run balance tests
- ⚠️ Dependency added (Inventory) → check cross-system gap

## Next steps
Run `/code-audit <system>` to find gaps between updated spec and code.
```

## Edge cases

- **Spec file is new** (no baseline): report as "all new" + suggest running `/code-audit` directly.
- **No retrofit file exists** (only raw GDD): diff the GDD directly.
- **`--against-gdd` but no retrofit exists**: error — nothing to compare.
- **Outside git repo**: degrade gracefully — ask user to provide old version manually.

## Output

1 file: `Production/diff-reports/<system>-<date>.md`. Summarize in chat with counts + flags.
