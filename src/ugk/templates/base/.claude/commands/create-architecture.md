---
name: create-architecture
description: Generate architecture documents from GDDs -- class diagrams, data flow, system boundaries. Writes to Docs/architecture/.
---

# /create-architecture -- Architecture Document Generation

## What this command does

Translates approved GDDs into technical architecture documents. Produces class diagrams (text-based), data flow descriptions, and system boundary definitions.

## Prerequisites

- At least one approved GDD in `Design/GDD/`
- `Design/GDD/systems-index.md` exists (run `/map-systems` if missing)
- `.claude/docs/technical-preferences.md` configured (run `/setup-engine` if missing)

## Process

1. **Read** all GDDs and the systems index.
2. **For each system** (in dependency order):
   a. **Interfaces** -- define public API surface (C# interfaces)
   b. **Data model** -- key classes, structs, ScriptableObjects
   c. **Data flow** -- how data moves between systems (text diagram)
   d. **Unity integration** -- MonoBehaviour vs plain C#, scene structure, prefab strategy
   e. Present to user for approval
   f. Write to `Docs/architecture/<system-name>.md`
3. **Cross-system overview** -- produce `Docs/architecture/overview.md`:
   - System boundary diagram
   - Dependency injection / wiring strategy
   - Event flow between systems
   - Shared data contracts
## Output

- `Docs/architecture/<system>.md` per system
- `Docs/architecture/overview.md` -- cross-system view

## Collaboration protocol

Present one system at a time. For each system, show the proposed architecture before writing. Flag any GDD requirements that are technically challenging. Use `AskUserQuestion` for any enumerable choice (pattern selection, data model variant, Unity integration approach) — do NOT ask free-form in chat.

## Suggested next step

End with a "Suggested next step" block. Typical options:

- `/architecture-decision <title>` — record any design trade-off as an ADR
- `/create-architecture` again — if more systems still need architecture docs
- `/gate-check architecture` — verify Phase 3 is complete
- `/implement <module>` — start Phase 4 implementation once architecture is approved
