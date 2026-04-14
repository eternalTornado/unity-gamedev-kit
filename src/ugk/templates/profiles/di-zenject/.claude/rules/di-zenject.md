---
name: di-zenject
description: Zenject / Extenject dependency injection rules and patterns for Unity
---

# Zenject DI Rules

## Setup

- Every scene must have a `SceneContext` with an `Installer`.
- Use `ProjectContext` for cross-scene singleton bindings.
- Prefer `MonoInstaller` for scene-specific bindings, `ScriptableObjectInstaller` for shared config.

## Registration patterns

```csharp
// Interface binding
Container.Bind<ICombatService>().To<CombatService>().AsSingle();

// MonoBehaviour binding
Container.Bind<PlayerController>().FromComponentInHierarchy().AsSingle();

// Factory
Container.BindFactory<EnemyConfig, Enemy, Enemy.Factory>();

// Signal
Container.DeclareSignal<PlayerDiedSignal>();
Container.BindSignal<PlayerDiedSignal>().ToMethod<GameManager>(x => x.OnPlayerDied).FromResolve();
```

## Rules

- Bind interfaces, not concrete types, for all services.
- Use `AsSingle()` for services, `AsTransient()` for data objects.
- Never call `Container.Resolve<T>()` outside of factories -- use `[Inject]` attribute.
- Keep Installers focused: one Installer per system/feature.
- Use Zenject Signals for cross-system events instead of C# events or delegates.
- Use `IInitializable`, `ITickable`, `IDisposable` interfaces where possible.

## Testing

- Use `ZenjectUnitTestFixture` base class.
- Install only the bindings needed for the test.
- Use `Container.Bind<T>().FromInstance(mock)` for mock injection.

## Forbidden

- Do NOT use `FindObjectOfType<T>()` to locate injected services.
- Do NOT nest more than 2 levels of sub-containers -- keep the hierarchy flat.
- Do NOT mix Service Locator and DI in the same project.
