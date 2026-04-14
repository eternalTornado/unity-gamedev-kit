---
name: di-vcontainer
description: VContainer dependency injection rules and patterns for Unity
---

# VContainer DI Rules

## Setup

- Every scene must have a `LifetimeScope` as the DI root.
- Use `[Inject]` attribute or constructor injection; prefer constructor injection for non-MonoBehaviour classes.
- MonoBehaviours use method injection via `[Inject]` on a public method.

## Registration patterns

```csharp
// Preferred: interface-based registration
builder.Register<ICombatService, CombatService>(Lifetime.Scoped);

// MonoBehaviour binding
builder.RegisterComponentInHierarchy<PlayerController>();

// Factory pattern
builder.RegisterFactory<EnemyConfig, Enemy>(container =>
    config => container.Resolve<Enemy.Factory>().Create(config));
```

## Rules

- Register interfaces, not concrete types, for all services.
- Use `Lifetime.Scoped` by default; `Lifetime.Singleton` only for truly global services (AudioManager, SaveSystem).
- Never resolve from the container directly (`container.Resolve<T>()`) outside of factories -- this is the Service Locator anti-pattern.
- Keep `LifetimeScope.Configure()` methods short; group registrations by system into extension methods if > 15 lines.
- Child scopes for scene-specific services; parent scope for cross-scene services.
- Use `IStartable` and `ITickable` interfaces instead of `MonoBehaviour.Start()`/`Update()` when the class doesn't need Transform or GameObject.

## Testing

- In tests, create a test `LifetimeScope` with mock registrations.
- Override specific registrations using `builder.Register<IMock, MockImpl>()`.
- VContainer's `IObjectResolver` is the testable entry point.

## Forbidden

- Do NOT use `FindObjectOfType<T>()` to locate injected services.
- Do NOT create MonoBehaviours with `new` -- use VContainer's factory or `RegisterComponentInNewPrefab`.
- Do NOT mix Service Locator and DI in the same project -- pick one pattern.
