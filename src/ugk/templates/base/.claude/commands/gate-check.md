---
name: gate-check
description: Formal phase gate. Verifies all required artifacts exist and pass quality bars before allowing the project to advance to the next phase. Returns verdict PASS / CONCERNS / FAIL.
---

# /gate-check — Phase Gate Verification

## Usage

```
/gate-check <phase>
```

Where `<phase>` is one of: `concept`, `systems`, `tech`, `preprod`, `prod`, `polish`, `release`.

## Verdicts

- **PASS** — all requirements met. Project may advance.
- **CONCERNS** — requirements met but with noted risks. User acknowledges risks, project may advance.
- **FAIL** — requirements missing. Project cannot advance until fixed.

## Requirements per phase

### `concept`
- [ ] Engine configured in `.claude/docs/technical-preferences.md` (not "[TO BE CONFIGURED]")
- [ ] `Design/GDD/game-concept.md` exists with all 9 sections
- [ ] `Design/GDD/systems-index.md` exists with dependency ordering
- [ ] At least 3 game pillars + 1 anti-pillar defined

### `systems`
- [ ] All MVP systems in `systems-index.md` have `Status: Approved`
- [ ] Each MVP system has its own `Design/GDD/<name>.md` with all 8 sections
- [ ] `Design/GDD/gdd-cross-review-*.md` exists with verdict PASS or CONCERNS

### `tech`
- [ ] `Docs/architecture/architecture.md` exists
- [ ] At least 3 Foundation-layer ADRs in `Docs/architecture/adr-*.md`
- [ ] `Docs/architecture/control-manifest.md` exists
- [ ] UX doc exists for primary screens

### `preprod`
- [ ] Vertical slice working on target platform
- [ ] Epics + Stories created in `Production/epics/`, `Production/stories/`
- [ ] Sprint plan covers at least the next 2 sprints
- [ ] Risk register in `Production/risks.md`

### `prod`
- [ ] All MVP stories closed (`Status: Done`)
- [ ] Unit test pass rate ≥ 95%
- [ ] No P0 or P1 bugs open
- [ ] Profiling passes target framerate on target device

### `polish`
- [ ] Playtest report exists
- [ ] Balance pass complete
- [ ] All accessibility requirements met
- [ ] Localization in place for launch languages

### `release`
- [ ] Version bumped, changelog written
- [ ] Store metadata ready (screenshots, icon, description)
- [ ] Privacy policy + ToS linked
- [ ] Crash reporter installed + tested
- [ ] Analytics events firing and verified in dashboard

## Process

1. Read the relevant files, check each requirement.
2. Print a checklist with ✅ / ⚠️ / ❌ per item.
3. Compute the verdict.
4. If FAIL: list missing artifacts and suggest skills to produce them.
5. If CONCERNS: list risks and ask user to explicitly acknowledge before proceeding.
6. If PASS: congratulate and suggest the next phase's first skill.
7. Update `Production/stage.txt` with the current phase.
