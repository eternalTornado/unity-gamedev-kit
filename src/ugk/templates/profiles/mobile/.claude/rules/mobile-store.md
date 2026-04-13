---
name: mobile-store
paths: [Production/releases/**]
description: App Store / Play Store submission requirements.
---

# Mobile Store Submission Rules

## iOS (App Store)
- Privacy manifest (PrivacyInfo.xcprivacy) required
- App Tracking Transparency prompt if tracking users
- Icons: all required sizes
- Screenshots: all required device sizes
- Age rating via App Store Connect

## Android (Play Store)
- Target API level = current requirement (2026: API 34+)
- Data safety form complete
- 64-bit native libraries
- Adaptive icon (foreground + background)
- Feature graphic + screenshots

## Both
- Privacy policy URL (public)
- Terms of service URL
- Content rating accurate
- No placeholder strings in any localized language
- Crash reporting enabled (Sentry/Firebase/etc.)

## Pre-submission checklist
- [ ] Test on minimum supported OS version
- [ ] Test on slowest supported device
- [ ] Verify IAP (if any) with test accounts
- [ ] Verify ads (if any) with test IDs
- [ ] Run `/regression-check` on release build
