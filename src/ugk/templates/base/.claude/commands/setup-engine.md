---
name: setup-engine
description: Configure the Unity project's technical preferences -- engine version, rendering pipeline, physics, naming conventions, performance budgets. Writes results to .claude/docs/technical-preferences.md.
---

# /setup-engine -- Technical Setup Configuration

## What this command does

Walks the user through configuring the technical foundations of their Unity project. Produces a filled-in `.claude/docs/technical-preferences.md` that all agents and rules reference.

## Process

1. **Read current state** — check `.claude/docs/technical-preferences.md` for any already-configured values. Skip categories that are already set (unless the user asks to change them).

2. **Batch ALL open questions into one `AskUserQuestion` call** (max 4 questions per call; if more are needed, issue a second call after the first batch returns). Use 2-4 concrete options per question. Do NOT ask free-form in chat. Do NOT ask one question at a time.

   Questions to ask (skip any that are already configured):

   a. **Engine + render pipeline** — options like "Unity 6 + URP", "Unity 6 + HDRP", "Unity 6 + Built-in", "Unity 2022 LTS + URP"
   b. **Target platforms** — options like "PC only", "Mobile only (iOS + Android)", "PC + Mobile", "Console + PC"
   c. **Async pattern** — options like "UniTask (recommended)", "Plain Task/async-await", "Coroutines only", "Mixed"
   d. **Event system** — options like "C# events", "UnityEvent", "ScriptableObject channels", "Mixed"

3. **Performance budgets** — second `AskUserQuestion` batch:

   a. **Target framerate** — "30 fps", "60 fps (recommended)", "120 fps", "Variable (min/target/max)"
   b. **Memory ceiling** — "256 MB (low-end mobile)", "512 MB (mid mobile)", "1 GB (high-end mobile/low-end PC)", "2 GB+ (PC/console)"
   c. **Test framework** — "Unity Test Framework (NUnit)", "NUnit + custom runner", "None — skip tests"
   d. **Minimum coverage target** — "50%", "70% (recommended)", "90%", "No target"

4. **Naming conventions** — populate from common C# defaults unless the user overrides:
   - Classes: `PascalCase`
   - Variables: `camelCase` (private with `_underscore` prefix)
   - Events/signals: `On<Thing><Happened>` (PascalCase)
   - Files: match primary class name
   - Constants: `UPPER_SNAKE_CASE` or `PascalCase`

5. **DI / Architecture** — if not already configured via the `ugk init --di` flag, ask:
   - DI framework preference: `none` (default), `VContainer`, `Zenject`, `Other`
   - If the user picks none, reinforce that ugk defaults to ScriptableObject events + Service Locator + manual injection.

6. **Write** each answered section to `.claude/docs/technical-preferences.md` immediately after approval. Use incremental writing — never buffer multiple sections.

7. **Sync constitution (optional)** — if `/memory/constitution.md` doesn't exist yet and the user plans to use Phase 4 speckit flow, offer to generate it from `CLAUDE.md` + the filled `technical-preferences.md`.

## Output

- `.claude/docs/technical-preferences.md` — fully populated
- `/memory/constitution.md` (optional, for speckit integration)

## Collaboration protocol

- Use `AskUserQuestion` — batch all open questions into one call with concrete options.
- Write each section immediately after approval.
- Do not override already-configured values without explicit user confirmation.

## Suggested next step

End with a "Suggested next step" block. Typical options:

- `/map-systems` — enumerate the systems this game will need
- `/brainstorm` — if the game concept is not yet written
- `/design-system <name>` — if you already know the first system to design
- `/gate-check concept` — verify Phase 1 is complete
