---
paths:
  - "Assets/Scripts/Core/**"
---

# Core/Engine Code Rules (Unity)

- **ZERO allocations in hot paths** (Update, FixedUpdate, physics, rendering) — pre-allocate, pool, reuse. Use `List<T>.Clear()` + reuse over `new List<T>()`.
- Core code must NEVER depend on gameplay code (strict direction: `Core ← Gameplay`, not the other way).
- Every public API must have XML doc comments with usage examples.
- Changes to public interfaces require a deprecation period (`[Obsolete]`) and migration guide.
- Profile **before AND after** every optimization — document measured numbers in a code comment or ADR.
- Use `struct` for small immutable values, `class` for entities. Avoid boxing.
- Object pooling is mandatory for frequently spawned entities (bullets, particles, enemies).
- Prefer `Span<T>`/`ReadOnlySpan<T>` over arrays for slicing without alloc.
- All public APIs must be thread-safe OR explicitly documented as single-thread-only.
- No UnityEngine-specific types (`Vector3`, `Transform`) in pure-logic classes intended for unit testing — use wrappers.
