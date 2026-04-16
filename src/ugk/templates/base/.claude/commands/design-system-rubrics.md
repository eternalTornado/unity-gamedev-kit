# Design System — Quality Rubrics

Referenced by `/design-system` and `/adopt` for section-level quality requirements. These rubrics define the minimum bar for each GDD section to be considered "complete."

---

## Acceptance Criteria Rubric

### Format
Every AC MUST use Given-When-Then:
```
GIVEN [initial state], WHEN [action or trigger], THEN [measurable outcome]
```

### Coverage
- At least 1 AC per core rule (from Detailed Rules section)
- At least 1 AC per player-facing formula (from Formulas section)
- Internal-only formulas (no direct player impact) are exempt from mandatory AC coverage
- Cross-system interaction criteria required for systems with dependencies
- Performance budget criterion required: frame time, memory, or "N/A — no runtime cost"

### Quality checks
- Every criterion must be independently verifiable by a QA tester WITHOUT reading the GDD
- "The system works as designed" is NOT a valid acceptance criterion
- AC that reference other sections ("as described in Overview") must be rewritten to be self-contained

### Agent delegation
When `qa-lead` agent is available, spawn for AC validation. The qa-lead checks coverage, format, and testability independently.

---

## Formulas Rubric

### Format
Every formula MUST follow this structure — prose-only formulas are not accepted:

1. **Formula expression**: `formula_name = expression`
2. **Variable table**:

   | Variable | Type | Range | Description |
   |----------|------|-------|-------------|
   | var_name | float | 0.0–1.0 | What this variable represents |

3. **Output range**: min to max under normal play
4. **Example**: worked example with real numbers

### Completion steering
- Do NOT write `[Formula TBD]` or describe a formula in prose without the variable table
- Do NOT use magic numbers — every constant must appear in the variable table with rationale
- Cross-reference rule: if a dependency GDD defines a formula whose output feeds into this system, reference it explicitly: "Uses `damage_output` from `combat.md` Formulas section"

---

## Edge Cases Rubric

### Format
Every edge case MUST use:
```
If [exact condition]: [exact outcome]. [rationale if non-obvious]
```

### Examples
- ✅ `If player health drops below 0 during damage calculation: clamp to 0, trigger death sequence, cancel pending heal effects.`
- ✅ `If two players trigger the same pickup on the same frame: server awards to the player whose request arrived first; second player sees pickup despawn. (Server-authoritative conflict resolution.)`
- ❌ `Handle edge cases appropriately.`
- ❌ `The system should handle overflow gracefully.`

### Quality checks
- An edge case without a resolution is an open design question, not a specification — flag it
- "Handle gracefully" / "handle appropriately" is never acceptable
- Each edge case must name both the exact condition AND the exact resolution
