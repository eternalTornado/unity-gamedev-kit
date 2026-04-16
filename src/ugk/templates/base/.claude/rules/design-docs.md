---
paths:
  - "design/gdd/**"
---

# Design Document Rules

- Every design document MUST contain these 7 sections: Overview, Detailed Rules, Formulas, Edge Cases, Dependencies, Tuning Knobs, Acceptance Criteria
- After retrofit and `/gate-check systems` PASS, the completed spec serves as the feature spec for Phase 4 implementation (speckit skips `/speckit.specify` because the spec already contains everything `spec.md` would have). Keep sections implementation-actionable — mood / tone / creative framing belongs in the concept doc, not per-system GDDs
- Retrofit output goes to `Docs/Retrofit/retrofit-<name>.md` — the original GDD in `Design/GDD/` is never modified by `/adopt`. Agent-authored GDDs (from `/design-system`) are written directly to `Design/GDD/` in 7-section format
- Formulas MUST follow this structure — prose-only formulas are not accepted:
  1. Formula expression: `formula_name = expression`
  2. Variable table: Variable | Type | Range | Description
  3. Output range: min to max under normal play
  4. Example: worked example with real numbers
- Edge cases MUST use this format:
  If [exact condition]: [exact outcome]. [rationale if non-obvious]
- Do NOT write "handle appropriately" — each must name the exact condition and the exact resolution
- An edge case without a resolution is an open design question, not a specification
- Dependencies must be bidirectional — if system A depends on B, B's doc must mention A
- Tuning knobs must specify safe ranges and what gameplay aspect they affect
- Acceptance criteria MUST use Given-When-Then format:
  GIVEN [initial state], WHEN [action or trigger], THEN [measurable outcome]
- Minimum coverage: at least 1 AC per core rule (from Detailed Rules) + 1 AC per player-facing formula (from Formulas). Internal-only formulas (no direct player impact) are exempt from mandatory AC coverage.
- Every criterion must be independently verifiable by a QA tester WITHOUT reading the GDD
- Cross-system interaction criteria required for systems with dependencies
- Performance budget criterion required: frame time, memory, or "N/A — no runtime cost"
- "The system works as designed" is NOT a valid acceptance criterion
- No hand-waving: "the system should feel good" is not a valid specification
- Balance values must link to their source formula or rationale
- A section may be marked "N/A — [one-sentence justification]" if the system genuinely does not have content for it.
  Example: "## Formulas\n\nN/A — this is a pure event-routing system with no calculations."
  The justification must explain WHY, not just state N/A.
  Sections that CANNOT be N/A: Overview, Detailed Rules, Dependencies, Acceptance Criteria.
  Sections that CAN be N/A with justification + user confirmation: Formulas, Edge Cases, Tuning Knobs.
- Design documents MUST be written incrementally: create skeleton first, then fill
  each section one at a time with user approval between sections. Write each
  approved section to the file immediately to persist decisions and manage context
