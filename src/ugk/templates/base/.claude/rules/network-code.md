---
paths:
  - "Assets/Scripts/Networking/**"
---

# Network Code Rules (Unity)

- Server is AUTHORITATIVE for all gameplay-critical state — never trust the client.
- All network messages must be versioned for forward/backward compatibility.
- Client predicts locally, reconciles with server — implement rollback for mispredictions.
- Handle disconnection, reconnection, and host migration gracefully.
- Rate-limit all network logging to prevent log flooding.
- All networked values specify replication strategy: reliable/unreliable, frequency, interpolation.
- Bandwidth budget: define and track per-message-type bandwidth usage.
- Security: validate all incoming packet sizes and field ranges — reject malformed packets.
- Use Mirror, Netcode for GameObjects, or Fishnet consistently — no mixing.
- Document RTT budget and acceptable jitter in each netcode feature's ADR.
