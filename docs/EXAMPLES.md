# Examples — real scenarios, step by step

## Example 1: GD updates combat.md — Dev reconciles

**Situation:** GD adds Parry mechanic, changes block reduction 50→70%, removes Stagger.

```
$ (in Claude Code)
> /diff-design design/gdd/combat.md
  → Report: +Parry, ~Block 0.5→0.7, -Stagger

> /code-audit design/gdd/combat.md
  → 5 gaps: G-01 missing Parry, G-02 formula drift, G-03 orphan Stagger, G-04 ambiguous frames, G-05 orphan SFX

> /clarify-gaps production/gap-reports/combat-2026-04-13.md
  → Question list for GD (5 questions, defaults provided)

  [ GD replies async: "defaults OK except Q4 = 8 frames" ]

> /update-gdd design/gdd/combat.md
  → Parry window = 8 frames written into §7

> /create-stories production/gap-reports/combat-2026-04-13.md
  → 4 stories created: combat-parry-impl, combat-block-tune, combat-stagger-remove, combat-doc-sync

> /story-readiness combat-parry-impl
> /dev-story combat-parry-impl
  → planner → programmer → tester → code-reviewer

> /verify-against-doc combat-parry-impl
  → PASS (5/5 criteria)

> /story-done combat-parry-impl

  [ repeat for remaining 3 stories ]

> /code-audit design/gdd/combat.md
  → 0 gaps

> /design-lock combat
  → Tag: combat-v2 (GDD sha a1b2c3, code 4e5f6g)
```

## Example 2: New feature "daily login reward" — no GDD yet

```
> /scope-check "daily login reward"
  → Classification: L (multi-system: save, inventory, UI, anti-cheat)
  → Recommended: /design-system

> /design-system daily-login-reward
  → Author 7-section GDD incrementally, approval per section

> /design-review design/gdd/daily-login-reward.md
  → CONCERNS (3 must-fix, 4 nits)

  [ fix must-fixes, re-run ]

> /design-review design/gdd/daily-login-reward.md
  → PASS

> /propagate-design-change daily-login-reward
  → Impact: save.md needs new field, inventory.md needs LoginRewardItem subtype, MainMenu.cs needs claim button

> /create-stories design/gdd/daily-login-reward.md
  → 6 stories

> /dev-story save-schema-v3
  → ... (all 6 stories) ...

> /gate-check production
  → PASS
```

## Example 3: New feature "double-jump" — GDD already exists

**Situation:** `design/gdd/movement.md` already specifies double-jump (authored last sprint, reviewed, locked). Dev picks it up from the backlog.

```
> /scope-check "implement double-jump from movement.md §3"
  → Classification: S (single system, has GDD, has acceptance criteria)
  → Recommended: /create-stories or go straight to /dev-story if story exists

> /story-readiness movement-double-jump
  → PASS: GDD §8 has 4 acceptance criteria, dependencies (input, physics) green
  → (if FAIL, falls back to /create-stories movement.md to generate one)

> /dev-story movement-double-jump
  → planner: reads movement.md, maps to PlayerController.cs + input rules
  → programmer: implements per GDD §3 formulas and §7 tuning knobs
  → tester: writes unit tests for 4 acceptance criteria from §8
  → code-reviewer: checks code-vs-GDD alignment

> /verify-against-doc movement-double-jump
  → PASS (4/4 acceptance criteria)

> /code-review movement-double-jump
  → 2 nits (naming, extract magic number) → fix inline

> /regression-check
  → No regressions in single-jump, wall-jump, fall-damage

> /story-done movement-double-jump
  → Moved to production/stories/done/
  → Sprint velocity updated
```

**Key difference vs Example 2 (no GDD):** skip `/design-system` / `/design-review` / `/propagate-design-change`. GDD is the contract; dev flow starts at `/story-readiness`. If the GDD has gaps discovered mid-implementation, pause and run `/clarify-gaps` — do **not** improvise design in code.

## Example 4: Bug fix during sprint

```
> /triage-bug "Player falls through floor on Level 3 cliff edge"
  → Severity: HIGH, Type: logic, Specialist: gameplay-code
  → Promoted to sprint as bug-2026-0042

> /dev-story bug-2026-0042
  → Fix + regression test

> /regression-check
  → No regressions in combat, movement, level loading

> /story-done bug-2026-0042
```

## Example 5: Balance tune — boss HP

```
> /scope-check "reduce boss HP by 20%"
  → Classification: XS (data-only)
  → Recommended: /balance-tune

> /balance-tune boss-hp
  → Ask rationale (playtest data)
  → Locate Assets/Data/Balance/BossStats.asset
  → 2000 → 1600
  → Append log to design/gdd/combat.md §7

> /regression-check
  → test_boss_phase2_dps_window uses old value — update expected
```

## Example 6: Solo dev starting fresh

```
$ uv tool install git+https://github.com/eternalTornado/unity-gamedev-kit.git
$ mkdir my-game && cd my-game
$ ugk init . --engine unity-6 --scope mobile
$ ugk check
$ (open in Claude Code)
> /start
  → Onboarding flow: detect stage → Concept → run /brainstorm
```
