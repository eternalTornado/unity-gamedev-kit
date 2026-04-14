---
name: architecture-decision
description: Create an Architecture Decision Record (ADR) documenting a technical trade-off. Writes to Docs/architecture/decisions/.
---

# /architecture-decision -- Architecture Decision Record

## What this command does

Creates a structured ADR (Architecture Decision Record) for a technical decision that has trade-offs worth documenting.

## When to use

- Choosing between two viable approaches (e.g., ECS vs MonoBehaviour, UniTask vs Coroutines)
- Making a decision that constrains future options
- Overriding a default convention for a good reason
- Any decision a future developer would ask "why did we do it this way?"

## Process

1. **Ask** what decision needs to be recorded (or accept argument: `/architecture-decision <topic>`).
2. **Draft ADR** with these sections:
   - **Title** -- short, descriptive (e.g., "Use UniTask for all async operations")
   - **Status** -- Proposed / Accepted / Deprecated / Superseded
   - **Context** -- what problem or constraint prompted this decision
   - **Options considered** -- at least 2, with pros/cons for each
   - **Decision** -- which option was chosen and why
   - **Consequences** -- positive, negative, and neutral outcomes
   - **References** -- links to GDDs, systems, or external docs that informed this
3. **Present** the draft for user review.
4. **Write** to `Docs/architecture/decisions/ADR-NNNN-<kebab-title>.md` (auto-increment number).

## Output

`Docs/architecture/decisions/ADR-NNNN-<title>.md`

## Collaboration protocol

Present the full ADR draft before writing. The user may adjust the decision rationale or add options not considered.
