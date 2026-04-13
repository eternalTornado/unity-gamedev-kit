---
name: pc-perf
paths: [Assets/Scripts/**]
description: Performance and scalability for desktop PC builds.
---

# PC Performance Rules

## Scalability
- Target: 60fps at 1080p on GTX 1060-equivalent (medium preset)
- Reach: 144fps at 1440p on RTX 3070 (high preset)
- Low: 30fps at 1080p on integrated GPU (low preset)

## Quality presets (required)
- Low / Medium / High / Ultra
- Each preset toggles: shadow resolution, texture quality, LOD bias, anti-aliasing, post-processing
- Auto-detect on first run via SystemInfo; allow user override

## Input
- KB/M primary; full gamepad support required (XInput + generic HID)
- Rebindable controls
- Handle alt-tab, minimize, resolution change gracefully

## Settings
- Resolution, windowed/fullscreen/borderless, v-sync, FPS cap
- Persist settings in `Application.persistentDataPath`

## Steam specifics (if applicable)
- Steamworks SDK integration documented
- Achievements defined in Steam backend AND mirrored in code
- Cloud saves path: `Application.persistentDataPath` + steamworks cloud config

## Crash reporting
- Enable Unity Cloud Diagnostics or Sentry
- Capture stack trace + system info on unhandled exceptions
