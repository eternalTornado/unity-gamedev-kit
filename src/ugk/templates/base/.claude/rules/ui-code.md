---
paths:
  - "Assets/Scripts/UI/**"
---

# UI Code Rules (Unity)

- UI must NEVER own or directly modify game state — display only. Use commands/signals to request changes.
- All UI text goes through a localization system (TMP + i18n asset) — no hardcoded user-facing strings.
- Support BOTH keyboard/mouse AND gamepad input for all interactive elements (Unity Input System, not legacy).
- All animations must be skippable and respect user motion/accessibility preferences.
- UI sounds trigger via the audio event bus, not `AudioSource.PlayOneShot` directly.
- UI must never block the main thread — heavy work on background threads via UniTask.
- Scalable text and colorblind modes are **mandatory**, not optional.
- Test all screens at minimum (1280×720) and maximum (4K) supported resolutions.
- Prefer UI Toolkit over UGUI for new screens (Unity 6). Document exceptions.
- Every `Button.onClick` handler must be ≤ 10 lines — delegate to a presenter/controller.
