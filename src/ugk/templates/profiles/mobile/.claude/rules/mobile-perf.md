---
name: mobile-perf
paths: [Assets/Scripts/**]
description: Performance constraints specific to mobile Unity builds (iOS/Android).
---

# Mobile Performance Rules

## Frame budget
- Target 60fps on mid-tier devices (iPhone 12, Pixel 5)
- Frame budget: 16.6ms total / 8ms CPU / 8ms GPU
- Fallback: 30fps on low-tier (iPhone 8, Galaxy A-series)

## Hard rules
- ❌ No `GameObject.Find` / `FindObjectOfType` in Update/FixedUpdate
- ❌ No `Resources.Load` at runtime — use Addressables
- ❌ No LINQ in hot paths (use for-loop)
- ❌ No `string` concatenation in Update — use StringBuilder or cache
- ❌ No `Camera.main` lookups — cache in Awake
- ✅ Pool GameObjects (bullets, VFX, UI popups)
- ✅ Texture compression: ASTC 6x6 on iOS, ASTC 6x6 / ETC2 on Android
- ✅ Mesh LODs for anything beyond 5m from camera

## Memory ceiling
- Runtime heap: ≤512MB on mid-tier
- Texture memory: ≤256MB
- Audio: ≤64MB (stream music, compress SFX)

## Battery & thermal
- Profile thermal throttling every release
- Lower FPS / shader complexity under thermal warning
- No constant vibration (drains battery + hardware wear)

## Input
- Touch-first; gamepad optional
- Tap targets ≥44pt (iOS HIG) / 48dp (Material)
- No hover states — use press/release only

## Platform-specific
- iOS: respect safe area on notched devices
- Android: handle back button (Input.GetKeyDown(KeyCode.Escape))
- Both: pause audio/game on `OnApplicationPause(true)`

## Verification
- Profile with Unity Profiler + platform native tools (Xcode Instruments, Android Profiler)
- Test on lowest-spec target device before every release
