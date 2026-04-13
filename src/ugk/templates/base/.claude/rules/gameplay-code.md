---
paths:
  - "Assets/Scripts/Gameplay/**"
---

# Gameplay Code Rules (Unity)

- ALL gameplay values MUST come from external config (ScriptableObject, JSON, CSV) — NEVER hardcoded magic numbers.
- Use `Time.deltaTime` for ALL time-dependent calculations (frame-rate independence). Use `Time.fixedDeltaTime` in `FixedUpdate` only.
- NO direct references to UI code — use SignalBus/events for cross-system communication.
- Every gameplay system must expose a clear interface (`IOrbitController`, `IMeteorSpawner`) — enables DI + testing.
- State machines must have explicit transition tables with documented states (no ad-hoc if/else chains for state).
- Write unit tests for all gameplay logic — separate logic from `MonoBehaviour` presentation. Pure C# classes with DI are preferred over `MonoBehaviour` for logic.
- Document which GDD section each feature implements in code comments (e.g. `// Implements: Design/GDD/orbit.md §3 Detailed Rules`).
- No static singletons for game state — use **VContainer** (or TheOne.DI) for dependency injection.
- No `GameObject.Find`, `FindObjectOfType` in `Update`/`FixedUpdate` — cache references at startup.
- No LINQ in `Update`/`FixedUpdate` — allocations kill mobile framerate.

## Examples

**Correct** (data-driven + DI):

```csharp
public sealed class OrbitController : IOrbitController
{
    private readonly OrbitConfig config;  // ScriptableObject, injected
    private readonly SignalBus signalBus;

    public OrbitController(OrbitConfig config, SignalBus signalBus)
    {
        this.config = config;
        this.signalBus = signalBus;
    }

    public void Tick(float deltaTime)
    {
        // uses config.speed, config.radius — no magic numbers
    }
}
```

**Wrong** (hardcoded + singleton + UI coupling):

```csharp
public class OrbitController : MonoBehaviour
{
    void Update()
    {
        transform.RotateAround(Vector3.zero, Vector3.up, 90f * Time.deltaTime); // magic number
        UIManager.Instance.UpdateHUD(); // direct UI coupling
    }
}
```
