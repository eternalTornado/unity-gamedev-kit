---
paths:
  - "Assets/Scripts/AI/**"
---

# AI Code Rules (Unity)

- **AI update budget: 2ms per frame maximum** — profile with Unity Profiler + Deep Profile to verify.
- All AI parameters must be tunable from ScriptableObject (behaviour tree weights, perception ranges, timers).
- AI must be debuggable: implement `OnDrawGizmos`/`OnDrawGizmosSelected` for all AI state (paths, perception cones, target lines, decision state).
- AI should **telegraph** intentions — players need 200-400ms to read and react.
- Prefer utility-based or behaviour tree approaches (e.g. NodeCanvas, Behavior Designer) over hardcoded if/else chains.
- Group AI must support formation, flanking, and role assignment from data.
- All AI state machines must log transitions when debug flag is on.
- Never trust AI-relevant input from the network without validation (multiplayer).
- Use `NavMeshAgent` thoughtfully — pathfinding is expensive, batch requests where possible.
- Sensor checks (vision, hearing) must run on a timer, not every frame.
