---
name: setup-engine
description: Configure the Unity project's technical preferences -- engine version, rendering pipeline, physics, naming conventions, performance budgets. Writes results to .claude/docs/technical-preferences.md.
---

# /setup-engine -- Technical Setup Configuration

## What this command does

Walks the user through configuring the technical foundations of their Unity project. Produces a filled-in `.claude/docs/technical-preferences.md` that all agents and rules reference.

## Process

1. **Read current state** -- check `.claude/docs/technical-preferences.md` for any already-configured values.
2. **Engine & rendering** -- ask:
   - Unity version (6, 2022 LTS, etc.)
   - Render pipeline (URP, HDRP, Built-in)
   - Target platforms (PC, Mobile, Console, Web)
3. **C# conventions** -- ask:
   - Naming: classes, variables, events, files, constants
   - Preferred patterns: async (UniTask vs coroutines), events (C# events, UnityEvent, ScriptableObject channels)
4. **Performance budgets** -- ask:
   - Target framerate (30/60/120)
   - Frame budget (ms)
   - Draw call ceiling
   - Memory ceiling
5. **Testing** -- ask:
   - Test framework (Unity Test Framework, NUnit)
   - Minimum coverage target
6. **DI / Architecture** -- if not already configured via `--di` flag, ask:
   - DI framework preference (none, VContainer, Zenject, other)
   - Event system preference
7. **Write** each answered section to `.claude/docs/technical-preferences.md` immediately after approval.
8. Suggest next step: `/map-systems` or `/design-system`.

## Output

`.claude/docs/technical-preferences.md` -- fully populated.

## Collaboration protocol

Ask one category at a time. Present sensible defaults based on the target platform. Write each section immediately after approval.
