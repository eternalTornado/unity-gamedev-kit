---
name: create-architecture
description: Generate architecture documents from GDDs -- class diagrams, data flow, system boundaries. Writes to Docs/architecture/.
---

# /create-architecture -- Architecture Document Generation

## What this command does

Translates approved design specs into technical architecture documents. Produces class diagrams (text-based), data flow descriptions, and system boundary definitions.

## Usage

```
/create-architecture
/create-architecture --gdd Design/GDD/combat.md
```

`--gdd <path>` — optional. Reference the original GDD alongside the retrofit spec for additional design context (mood, intent, rationale that may not have survived retrofit).

## Prerequisites

- At least one completed spec: `Docs/Retrofit/retrofit-<name>.md` (from `/adopt`) or `Design/GDD/<name>.md` (agent-authored, already 7-section)
- `Design/GDD/systems-index.md` exists (run `/map-systems` if missing)
- `.claude/docs/technical-preferences.md` configured (run `/setup-engine` if missing)

## Process

1. **Read** all specs (check `Docs/Retrofit/` first, fallback `Design/GDD/`) and the systems index. If `--gdd` provided, also read the original GDD for additional context.
2. **For each system** (in dependency order), fill in the **Per-system output template** below:
   a. **Metadata header** — name, domain, GDD source, architect, Unity version, key dependencies
   b. **Interfaces** — public API surface (C# interfaces). Access modifiers are prescriptive.
   c. **Data model** — key classes, structs, ScriptableObjects. Data and behavior stay separated; ScriptableObjects are data-only.
   d. **Data flow** — how data moves between systems (text diagram)
   e. **Unity integration** — split into four explicit sub-fields (do NOT merge):
      - **MonoBehaviour vs plain C#** — which types are MB, which are POCO
      - **Execution Order** — Update / FixedUpdate / LateUpdate / custom Script Execution Order
      - **Asset Workflow** — Addressables group, prefab loading strategy, Resources avoidance
      - **Optimization** — object pooling, `PropertyToID`, struct vs class, allocation hotspots, Burst/Jobs if any
   f. Present to user for approval
   g. Write to `Docs/architecture/<system-name>.md`
3. **Cross-system overview** — produce `Docs/architecture/overview.md`:
   - System boundary diagram
   - Dependency injection / wiring strategy
   - Event flow between systems
   - Shared data contracts

## Per-system output template

Every `Docs/architecture/<system>.md` MUST follow this structure. Pin an **Agent Directive** callout (`> **Agent Directive:** …`) at the top of each section — these are read-time instructions for downstream implementation agents (`/implement`, `programmer`). Keep them one line, imperative, and scoped to the section.

~~~markdown
# <System Name> — Architecture

> **Agent Directive:** Read this document fully before implementing. Follow the interfaces, data models, and Unity integration exactly. Deviate only via an ADR (`/architecture-decision`).

## 1. Metadata
- **System:** <name>
- **Domain:** <Gameplay | AI | UI | Networking | Core>
- **Spec source:** `Docs/Retrofit/retrofit-<system>.md` or `Design/GDD/<system>.md`
- **Primary architect:** <name>
- **Unity version:** <e.g., Unity 6 LTS>
- **Key dependencies:** <Zenject, Addressables, UniTask, Input System, …>

## 2. Interfaces
> **Agent Directive:** Public API surface. Access modifiers are prescriptive — do not widen.

```csharp
// interface definitions
```

## 3. Data Model
> **Agent Directive:** Keep data and behavior separated. ScriptableObjects are data-only.

```csharp
// classes, structs, ScriptableObjects
```

## 4. Data Flow
> **Agent Directive:** Text diagram — do not replace with ASCII art unless it improves clarity.

## 5. Unity Integration
> **Agent Directive:** Violating these rules breaks the contract with other systems.

- **MonoBehaviour vs plain C#:** <…>
- **Execution Order:** <Update | FixedUpdate | LateUpdate | custom SEO value>
- **Asset Workflow:** <Addressables group, prefab strategy, no Resources>
- **Optimization:** <pooling targets, PropertyToID, struct usage, Burst/Jobs, allocation hotspots>
~~~

## Output

- `Docs/architecture/<system>.md` per system (structure per template above)
- `Docs/architecture/overview.md` — cross-system view

## Collaboration protocol

Present one system at a time. For each system, show the proposed architecture before writing. Flag any spec requirements that are technically challenging. Use `AskUserQuestion` for any enumerable choice (pattern selection, data model variant, Unity integration approach) — do NOT ask free-form in chat.

## Context awareness

This command can consume significant context window space. If context usage exceeds 70%:
1. Write any in-progress section to file immediately
2. Summarize remaining work
3. Suggest the user run `/compact` then resume

## Suggested next step

End with a "Suggested next step" block. Typical options:

- `/architecture-decision <title>` — record any design trade-off as an ADR
- `/create-architecture` again — if more systems still need architecture docs
- `/gate-check architecture` — verify Phase 3 is complete
- `/implement <module>` — start Phase 4 implementation once architecture is approved
