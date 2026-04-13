---
name: mobile-input
paths: [Assets/Scripts/UI/**, Assets/Scripts/Gameplay/Input/**]
description: Touch-first input rules for mobile.
---

# Mobile Input Rules

## Touch patterns
- Primary input = touch; all mechanics must be playable with touch alone
- Use Unity `InputSystem` Touch API, not legacy `Input.touches`
- Never depend on multi-touch for core mechanic unless ergonomic (e.g., virtual joystick + button)

## Gesture support
- Tap, long-press, swipe, pinch (zoom) — standard
- Custom gestures require accessibility alternative

## UI
- Tap targets ≥44pt / 48dp
- Avoid precise drag on small elements
- Hover/rollover states don't exist — design for press/release only

## Virtual controls (if any)
- On-screen stick + buttons: opacity adjustable, position customizable
- Hide during cutscenes
- Haptic feedback on press (short, <20ms)
