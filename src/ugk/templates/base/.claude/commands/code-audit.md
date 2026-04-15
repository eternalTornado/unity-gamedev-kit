---
name: code-audit
description: Scan Unity code against a GDD to find gaps — features in doc not in code, code not in doc, formula mismatches. Produces a gap inventory ready for clarification with GD.
model: opus
---

# /code-audit — Find gaps between GDD and code

## When to use

- After `/diff-design` (or when GDD changed but you aren't sure what code needs to change)
- Before creating stories for a new sprint — audit current state first
- As a periodic health check (weekly) to catch doc drift

## Inputs

- `<gdd-file>` — path to GDD to audit against
- `<code-scope>` — optional folder glob (default: `Assets/Scripts/**`)

## Collaboration Protocol

Do NOT fix anything. This is READ-ONLY reconnaissance. Ask before writing the gap report.

## Workflow

1. **Parse GDD** for 7 sections. Extract:
   - Named mechanics from §2 Detailed Rules
   - Formulas and constants from §3 Formulas
   - Tuning values from §6 Tuning Knobs
   - Acceptance criteria from §7
2. **Scan code** (via Grep/Read):
   - Find class/MonoBehaviour names matching mechanic names
   - Find constants, public fields, ScriptableObject references
   - Follow `GDD-ref:` comments if present
3. **Match + gap**:
   - **G-MISSING** — GDD mechanic has no code implementation
   - **G-FORMULA** — formula constant in code ≠ GDD value
   - **G-ORPHAN** — code feature not mentioned in GDD
   - **G-AMBIGUOUS** — GDD says "short", "fast", etc. — unmeasurable
   - **G-STALE** — code has `// TODO` or deprecated flag matching GDD section
4. **Evidence-first**: every gap must cite (a) GDD section + line, (b) code file + line OR absence.
5. **Draft gap report** → ask approval → write to `production/gap-reports/<system>-<date>.md`.

## Gap report format

```markdown
# Gap Report: <system>
**GDD:** design/gdd/<system>.md (audited <date>)
**Code scope:** Assets/Scripts/<system>/**
**Total gaps:** N (MISSING: X, FORMULA: Y, ORPHAN: Z, AMBIGUOUS: A)

| ID | Type | Severity | GDD evidence | Code evidence | Verdict |
|----|------|----------|--------------|---------------|---------|
| G-01 | MISSING | HIGH | §3.5 "Parry window 8 frames" | (none found) | TBD |
| G-02 | FORMULA | MED | §4 "block_reduction = 0.7" | `BlockController.cs:42` uses 0.5 | TBD |
| G-03 | ORPHAN | LOW | — | `StaggerHandler.cs` | TBD |

## Recommended next step
Run `/clarify-gaps production/gap-reports/<system>-<date>.md` to generate questions for GD.
```

## Severity rubric

- **HIGH** — feature completely missing, formula affects balance, ship-blocking
- **MED** — formula drift, partial implementation
- **LOW** — orphan code (may be intentional), cosmetic mismatch

## Edge cases

- **Code uses reflection / runtime lookup** — mark AMBIGUOUS; audit cannot verify statically
- **Generated code** (e.g., from `*.meta`, auto-gen) — skip with note
- **GDD section empty or `[TBD]`** — report as "GDD incomplete" rather than gap

## Anti-patterns

- ❌ Don't auto-fix anything. Verdict on each gap comes from GD, not AI.
- ❌ Don't assume orphan code is dead — always ask before suggesting removal.
