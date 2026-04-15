---
name: map-systems
description: Extract game systems from the concept doc and produce a systems-index.md with dependency graph. Use after /brainstorm or when a game-concept.md exists.
---

# /map-systems -- System Extraction & Dependency Mapping

## What this command does

Reads the game concept document and identifies every discrete game system that needs a GDD. Produces a systems index with dependencies, priority, and complexity estimates.

## Process

1. **Read ALL `.md` files** in `Design/GDD/`. Look for a concept doc (any file describing the overall game concept, core loop, or pillars -- it may not be named `game-concept.md`). If no GDD files exist at all, suggest `/brainstorm` first.
2. **Extract systems** -- identify every mechanical system implied by the concept (e.g., combat, movement, inventory, progression, UI, economy).
3. **Present system list** to user for validation. Use the `AskUserQuestion` tool (multi-select) if there's any ambiguity about scope ("which of these are MVP?", "which should merge?"). Do NOT ask free-form in chat.
4. **Dependency mapping** -- for each system, identify:
   - Upstream dependencies (what it reads from)
   - Downstream dependents (what reads from it)
   - Present as a text-based dependency graph
5. **Priority & complexity** -- for each system, estimate:
   - Priority: Core / Important / Nice-to-have
   - Complexity: Low / Medium / High
   - Suggested design order (respecting dependencies)
6. **Write** `Design/GDD/systems-index.md` with the full map.

## Output

`Design/GDD/systems-index.md` with sections: System List, Dependency Graph, Priority Matrix, Suggested Design Order.

## Collaboration protocol

Present the full system list for approval before writing. Use `AskUserQuestion` with concrete options whenever the user needs to pick, classify, or prioritize. The user may add, remove, or re-prioritize systems.

## Suggested next step

End with a "Suggested next step" block. Typical options:

- `/design-system <first-system>` — author the highest-priority system GDD
- `/gate-check concept` — verify Phase 1 is complete before drafting system GDDs
- `/architecture-decision <title>` — if any listed system needs a tech spike before design
