---
name: perf-profile
description: Audit code against performance budgets defined in technical-preferences.md. Checks hot paths, allocations, draw calls, and frame budget compliance.
---

# /perf-profile -- Performance Audit

## What this command does

Reviews the codebase against the performance budgets defined in `.claude/docs/technical-preferences.md` and flags violations.

## Process

1. **Read** `.claude/docs/technical-preferences.md` for target framerate, frame budget, draw call ceiling, memory ceiling.
2. **Scan** `Assets/Scripts/` for common performance anti-patterns:
   - LINQ in `Update()`, `FixedUpdate()`, `LateUpdate()`
   - `GetComponent<T>()` in hot paths (not cached)
   - String concatenation in loops
   - Boxing/unboxing in frequently called methods
   - `FindObjectOfType` or `FindObjectsOfType` at runtime
   - Allocations in per-frame code (new arrays, lists, delegates)
   - Missing object pooling for frequently instantiated objects
3. **Check** Unity-specific concerns:
   - Shader complexity vs target platform
   - Texture memory estimates
   - Audio compression settings
4. **Categorize** findings:
   - CRITICAL: Will cause frame drops on target hardware
   - WARNING: May cause issues under load
   - INFO: Optimization opportunity
5. **Present** findings with file paths, line numbers, and suggested fixes.

## Output

Report printed to conversation. Optionally write to `Production/qa/perf-audit-<date>.md`.

## Collaboration protocol

Present the full report. Offer to fix individual issues with user approval. For each fix, show the diff before applying.
