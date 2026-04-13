---
name: multiplayer-arch
paths: [Assets/Scripts/Networking/**, Assets/Scripts/Gameplay/**]
description: Architecture rules for networked multiplayer — authority, replication, anti-cheat.
---

# Multiplayer Architecture Rules

## Authority model
- Server-authoritative for all gameplay state (never trust client)
- Client-side prediction + server reconciliation for movement
- Lag compensation for hit registration (rewind server state to client's RTT)

## Replication
- Every networked variable annotated with ownership + update frequency
- Quantize floats (position, rotation) to reduce bandwidth
- Snapshot interpolation for remote players

## Bandwidth budget
- <20 KB/s per player on LAN-like connection
- <10 KB/s on 3G fallback
- Profile with Network Profiler every milestone

## Anti-cheat
- Server validates every damage, pickup, purchase
- Never send secrets to client (item drop tables, boss patterns)
- Rate-limit messages per client (prevent spam)
- Detect impossible state deltas (speed hack, teleport)

## Connection lifecycle
- Handle connect / disconnect / reconnect gracefully
- Timeout + retry policy documented
- Pause game on host migration (if supported) or boot to menu

## Testing
- Unit tests for serialization of every networked message
- Integration tests with simulated latency (100ms, 250ms, 500ms, 1s)
- Packet loss tests (5%, 10%, 25%)

## Constraints
- ❌ No gameplay code in client-only branch paths
- ❌ No `Random.Range` on server without seed (or use deterministic RNG)
- ❌ No file I/O on server hot path
- ✅ All RPC calls have validation on receive side
