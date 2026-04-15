# Workflow Guide — GDD to Ship

This guide maps the full day-to-day flow for teams using `unity-gamedev-kit`.

> **v1.1.0 — 5-phase workflow.** The legacy 7-phase flow (Concept → Systems → Tech → Pre-prod → Production → Polish → Release) is replaced by **5 phases**: Concept → Systems Design → Architecture → Implementation → Polish. Phase 4 (Implementation) delegates to [speckit](https://github.com/github/spec-kit) via the new `/implement <module>` command. See `CHANGELOG.md` for migration notes.

## 5-phase workflow at a glance

| Phase | Commands | Artifacts |
|---|---|---|
| 1. Concept | `/brainstorm`, `/setup-engine`, `/map-systems` | `Design/GDD/game-concept.md`, `systems-index.md` |
| 2. Systems Design | `/design-system`, `/review-all-gdds`, `/update-gdd` | 8-section GDDs per system |
| 3. Architecture | `/create-architecture`, `/architecture-decision` | `Docs/architecture/` + ADRs |
| 4. Implementation | `/implement <module>` → speckit `/plan` → `/tasks` → `/implement` → `/code-review` | `Docs/specs/<module>/`, source code, tests |
| 5. Polish | `/perf-profile`, `/balance-check`, `/playtest-report`, `/release-checklist`, `/hotfix` | Tuned build + shipped release |

Between phases: `/gate-check <phase>` with `<phase>` ∈ `concept | systems | architecture | implementation | polish`.

## Speckit integration (Phase 4)

Phase 4 uses speckit's spec-driven development flow but **skips `/speckit.specify`** because the GDD already contains Detailed Rules, Edge Cases, Acceptance Criteria, and Formulas — everything `spec.md` would have. The `/implement` wrapper:

1. Reads `Design/GDD/<module>.md` (feature spec) + `Docs/architecture/<module>.md` (tech context)
2. Invokes `/speckit.plan` → outputs `Docs/specs/<module>/plan.md` + `data-model.md` + `contracts/`
3. Invokes `/speckit.tasks` → outputs `Docs/specs/<module>/tasks.md`
4. Invokes `/speckit.implement` → generates code + tests, marks tasks `[X]`
5. Runs `/code-review` to enforce the priority hierarchy

Speckit reads `/memory/constitution.md` for gate checks. ugk populates it from `CLAUDE.md` + `.claude/docs/technical-preferences.md` during `/setup-engine`.

---

## Legacy 7-phase flow (below) — being retired

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
