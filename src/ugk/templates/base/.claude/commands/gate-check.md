---
name: gate-check
description: Formal phase gate. Verifies all required artifacts exist and pass quality bars before allowing the project to advance to the next phase. Returns verdict PASS / CONCERNS / FAIL.
---

# /gate-check — Phase Gate Verification

## Usage

```
/gate-check <phase>
```

Where `<phase>` is one of: `concept`, `systems`, `architecture`, `implementation`, `polish`.

These map to the 5-phase workflow:

| Gate | Between | Purpose |
|---|---|---|
| `concept` | Phase 1 → 2 | Concept locked, systems mapped |
| `systems` | Phase 2 → 3 | All MVP GDDs complete, cross-reviewed |
| `architecture` | Phase 3 → 4 | Architecture docs + ADRs in place, ready for implementation |
| `implementation` | Phase 4 → 5 | MVP features shipped, tests pass, budgets met |
| `polish` | Phase 5 → release | Build ready to ship |

## Verdicts

- **PASS** — all requirements met. Project may advance.
- **CONCERNS** — requirements met but with noted risks. User acknowledges risks, project may advance.
- **FAIL** — requirements missing. Project cannot advance until fixed.

## Requirements per phase

### `concept` (Phase 1 → 2)
- [ ] Engine configured in `.claude/docs/technical-preferences.md` (not `[TO BE CONFIGURED]`)
- [ ] A game concept document exists in `Design/GDD/` (scan ALL `.md` files — may not be named `game-concept.md`)
- [ ] Concept doc contains: elevator pitch, core loop, game pillars, target audience
- [ ] `Design/GDD/systems-index.md` exists with dependency ordering
- [ ] At least 3 game pillars + 1 anti-pillar defined

### `systems` (Phase 2 → 3)
- [ ] All MVP systems in `systems-index.md` have `Status: Approved`
- [ ] Each MVP system has its own `Design/GDD/<name>.md` with all 8 sections
- [ ] `Design/GDD/gdd-cross-review-*.md` exists with verdict PASS or CONCERNS

### `architecture` (Phase 3 → 4)
- [ ] `Docs/architecture/overview.md` exists (cross-system overview)
- [ ] Per-system architecture docs: `Docs/architecture/<system>.md` for each MVP system
- [ ] At least 3 foundation-layer ADRs in `Docs/architecture/adr-*.md`
- [ ] UX/flow doc exists for primary screens (if the game has UI-heavy flows)

### `implementation` (Phase 4 → 5)
- [ ] All MVP modules have `Docs/specs/<module>/plan.md` + `tasks.md` (speckit output)
- [ ] All tasks in each `tasks.md` are marked `[X]` (completed)
- [ ] Unit test pass rate ≥ 95%
- [ ] No P0 or P1 bugs open
- [ ] Profiling passes target framerate on target device
- [ ] `/code-review` has been run on each MVP module and issues resolved

### `polish` (Phase 5 → release)
- [ ] Playtest report exists in `Production/qa/` or `Docs/playtest/`
- [ ] Balance pass complete (balance-check output archived)
- [ ] Accessibility requirements met (color-blind, input remapping, font size)
- [ ] Localization in place for launch languages
- [ ] Version bumped, changelog written
- [ ] Store metadata ready (screenshots, icon, description)
- [ ] Privacy policy + ToS linked
- [ ] Crash reporter installed + tested
- [ ] Analytics events firing and verified in dashboard

## Process

1. Scan `Design/GDD/` for ALL `.md` files. Read each one. Then check each requirement for the requested phase.
2. Print a checklist with ✅ / ⚠️ / ❌ per item.
3. Compute the verdict.
4. If FAIL: list missing artifacts and suggest the specific commands that would produce them.
5. If CONCERNS: list risks and ask the user to explicitly acknowledge before advancing.
6. If PASS: state the next phase and first command.
7. Update `Production/stage.txt` with the current phase.

## Suggested next step

After the verdict, ALWAYS end with a "Suggested next step" block:

- On **PASS** → suggest the first command of the next phase (e.g., after `systems` pass → `/create-architecture` or `/architecture-decision`).
- On **CONCERNS** → ask the user to acknowledge risks, then suggest the next-phase command.
- On **FAIL** → list the 1-3 specific commands that would resolve the missing items (e.g., `/design-system <name>`, `/review-all-gdds`, `/setup-engine`).

## Collaboration protocol

- Never self-approve a gate — always print the verdict and let the user make the call.
- On CONCERNS, wait for explicit acknowledgement before updating `Production/stage.txt`.
