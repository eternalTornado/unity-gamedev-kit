---
name: release-checklist
description: Generate a pre-release checklist covering build, QA, store submission, and go-live tasks. Writes to Production/releases/.
---

# /release-checklist -- Pre-Release Checklist

## What this command does

Generates a comprehensive checklist for shipping a build, customized to the project's target platforms and scope.

## Process

1. **Read** `.claude/docs/technical-preferences.md` for target platforms.
2. **Read** latest sprint and milestone docs for release scope.
3. **Generate checklist** covering:

   **Build**
   - Clean build succeeds (no warnings as errors)
   - All automated tests pass
   - Build size within budget
   - Version number and build number updated

   **QA**
   - All BLOCKING bugs resolved
   - Regression test pass (run `/regression-check`)
   - Performance within budgets on all target platforms
   - No placeholder art, text, or debug UI in build

   **Platform-specific** (based on scope profile)
   - Mobile: App Store / Play Store metadata, screenshots, rating questionnaire
   - PC: Steam page, achievements, cloud save
   - Console: certification requirements checklist

   **Go-live**
   - Changelog / patch notes written (run `/patch-notes`)
   - Analytics and crash reporting enabled
   - Server infrastructure ready (if multiplayer)
   - Rollback plan documented

4. **Write** to `Production/releases/release-<version>.md`.
5. Each item is a checkbox -- user checks off as completed.

## Output

`Production/releases/release-<version>.md`

## Collaboration protocol

Present the full checklist for review. User may add/remove items based on their release process.
