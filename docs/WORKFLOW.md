# Workflow Guide — GDD to Ship

This guide maps the full day-to-day flow for teams using `unity-gamedev-kit`.

Compared with spec-kit's `specify → clarify → plan → tasks → implement`, ugk has **two interacting layers** (Design + Dev) and a **reconciliation loop** for GD+Dev teams where the GDD and code can drift.

## Core loop

```
/scope-check → (branch by scope) → /design-system or /create-stories →
    /story-readiness → /dev-story → /verify-against-doc →
    /story-done → /gate-check
```

## Task types

### 1. Existing GDD section → implement a story

```
/sprint-status
/story-readiness <story>
/dev-story <story>
/code-review           (optional)
/verify-against-doc <story>
/story-done <story>
```

### 2. New feature, no GDD yet

```
/brainstorm "topic"               (optional — when concept is vague)
/design-system <system>
/design-review design/gdd/<system>.md
/propagate-design-change <system>
/create-stories design/gdd/<system>.md
→ continue with flow #1
```

### 3. Bug

```
/triage-bug "description"
/dev-story <bug-id>
/regression-check
/story-done <bug-id>
```

### 4. Balance tweak (data only)

```
/scope-check "tweak"
/balance-tune <system>
/regression-check
/story-done
```

### 5. GD updated the GDD — reconcile with code

This is the **doc-code-sync loop** for GD+Dev teams with no Producer.

```
/diff-design design/gdd/<system>.md
/code-audit design/gdd/<system>.md
/gap-report                        (aggregate if multiple files)
/clarify-gaps <gap-report>         → send to GD, wait for answers
/update-gdd                        (lock GD's decisions into doc)
/scope-check
/create-stories <gap-report>
→ continue with flow #1
→ at end: /code-audit again → /design-lock
```

## Sprint cadence

| When | Skill | Who |
|------|-------|-----|
| Sprint start | `/sprint-plan`, `/create-stories`, `/story-readiness` | Producer (or dev with producer-lite agent) |
| Daily | `/sprint-status` → `/dev-story` → `/story-done` | Dev |
| Mid-sprint | `/design-review`, `/code-review` | Leads |
| Sprint end | `/sprint-close`, `/patch-notes` | Producer |
| Phase end | `/gate-check <phase>` | Opus — verdict PASS/CONCERNS/FAIL |

## Scope decision tree

```
Task arrives → /scope-check
  ├─ XS (data only)         → /balance-tune
  ├─ S  (feature, GDD OK)   → /create-stories
  ├─ M  (feature, no GDD)   → /quick-design → /create-stories
  ├─ L  (multi-system)      → /design-system + /propagate-design-change
  └─ XL (new pillar)        → /brainstorm → /design-system
```

## For small teams (GD + Dev, no Producer)

- Spawn `producer-lite` agent when you need coordination without a real producer
- Run daily `/sprint-status` via `/schedule` to get automatic reminders
- Use the doc-code-sync loop (#5) after every GDD update — don't batch
- Default to async: `/clarify-gaps` produces question lists GD can answer offline

## Anti-patterns

- ❌ Skipping `/story-readiness` — you'll find missing info after coding starts
- ❌ Skipping `/verify-against-doc` — code that "compiles" isn't code that implements the design
- ❌ Skipping `/design-lock` after a reconcile cycle — drift will return within weeks
- ❌ Running `/balance-tune` without `/scope-check` first — hidden logic changes will slip in
