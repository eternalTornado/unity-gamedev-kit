---
name: dev-story
description: Implements a single Story end-to-end — plan, code, test, review. Delegates to specialized agents (planner, gameplay-programmer, tester, code-reviewer) and enforces the priority hierarchy (Quality → Modern C# → Architecture → Performance).
---

# /dev-story — Implement a Story

## Usage

```
/dev-story <story-id>
/dev-story ORBIT-001
```

## Process

1. **Read the story** at `Production/stories/<story-id>.md`. If missing, stop and ask user.
2. **Read linked GDD section** referenced by the story.
3. **Planner phase** — delegate to `planner` agent to produce a TODO list in `Production/plans/<story-id>.md`.
4. **Implementation phase** — delegate to the right specialist based on file path:
   - `Assets/Scripts/Gameplay/` → `gameplay-programmer`
   - `Assets/Scripts/AI/` → `ai-programmer`
   - `Assets/Scripts/UI/` → `ui-programmer`
   - `Assets/Scripts/Networking/` → `network-programmer`
   - `Assets/Scripts/Core/` → `engine-programmer`
5. **Test phase** — delegate to `tester` agent to write unit tests in `Tests/Unit/<system>/`.
6. **Compile check** — run Unity's command-line compile (or ask user to open Unity Editor) and surface errors.
7. **Code review phase** — delegate to `code-reviewer` agent enforcing the 4-priority hierarchy:
   - 🔴 Quality: nullable, no warnings, throw not log, `nameof`, `readonly`
   - 🟡 Modern C#: LINQ, expression bodies, pattern matching
   - 🟢 Architecture: VContainer DI, SignalBus, Data Controllers, UniTask
   - 🔵 Performance: no LINQ in Update, zero-alloc hot paths, pooling
8. **Close the story** — delegate to `docs-manager` if new public APIs were added. Ask user if ready for `/story-done`.

## Collaboration protocol

- Before each phase, summarize to the user what the next agent will do and ask for approval.
- Never commit code during `/dev-story` — commits require explicit user instruction.
- If compile fails or tests fail, fix them; do not mark the story done with broken tests.
- If the story's acceptance criteria cannot be met with available infrastructure, stop and escalate (may need an ADR first).
