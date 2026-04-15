# Skills Reference

All skills shipped with unity-gamedev-kit. Run `ugk list skills` to see them in the CLI.

## Onboarding
| Skill | Model | Purpose |
|-------|-------|---------|
| `/start` | sonnet | Guided onboarding, detects project stage, recommends first skill |
| `/brainstorm` | sonnet | 6-phase ideation for new game concepts |

## Design
| Skill | Model | Purpose |
|-------|-------|---------|
| `/design-system` | opus | Author full 7-section GDD (incremental write) |
| `/quick-design` | opus | GDD-lite for small features (3 sections) |
| `/design-review` | opus | Peer-review a GDD for completeness + consistency |
| `/update-gdd` | opus | Apply clarifications/decisions back into GDD |
| `/propagate-design-change` | opus | Cross-system impact analysis |

## Doc ↔ Code Sync (for GD+Dev teams)
| Skill | Model | Purpose |
|-------|-------|---------|
| `/diff-design` | opus | Git-diff a GDD to extract what changed |
| `/code-audit` | opus | Scan code vs GDD, list gaps |
| `/gap-report` | opus | Consolidate diff + audit into one report |
| `/clarify-gaps` | opus | Generate question list for GD |
| `/verify-against-doc` | opus | Verify code matches GDD §8 criteria |
| `/design-lock` | opus | Tag "doc == code" baseline |

## Sprint / story
| Skill | Model | Purpose |
|-------|-------|---------|
| `/sprint-status` | sonnet | Daily sprint snapshot |
| `/story-readiness` | sonnet | Gate before `/dev-story` |
| `/create-stories` | sonnet | Break GDD/gap-report into stories |
| `/scope-check` | sonnet | Classify task scope (XS/S/M/L/XL) |
| `/dev-story` | sonnet | Chain: planner → specialist → tester → reviewer |
| `/code-review` | sonnet | Deep code review, GDD alignment |
| `/story-done` | sonnet | Close story, move to done folder |

## QA / bugs / balance
| Skill | Model | Purpose |
|-------|-------|---------|
| `/triage-bug` | opus | Classify severity + produce bug story |
| `/regression-check` | opus | Verify tests pass after change |
| `/balance-tune` | opus | Data-only numeric tunes with rationale |

## Release
| Skill | Model | Purpose |
|-------|-------|---------|
| `/gate-check` | opus | Phase gate verdict (PASS/CONCERNS/FAIL) |
| `/patch-notes` | sonnet | Generate player-facing release notes |

## Model tier rationale

- **Sonnet**: default for sprint/story operations and narrative-only tasks — fast, cheap, good enough for well-scoped execution
- **Opus**: design authoring, doc↔code reconciliation, QA triage, balance tuning, and phase-gate verdicts — anything that requires multi-document synthesis or high-stakes judgement where a wrong call ships bugs or breaks the player experience
- **Haiku**: reserved; no skills currently use it (kept for future read-only formatters)

Rule of thumb: if the skill changes player-facing behaviour, an acceptance criterion, or a design invariant, pick **opus**. If it only reports, classifies, or routes, **sonnet** is enough.

## Adding your own skill

```bash
ugk list skills             # See available catalog
# or write a new skill file:
echo '---' > .claude/commands/my-skill.md
echo 'name: my-skill' >> .claude/commands/my-skill.md
# ...
```

Path: `.claude/commands/<name>.md` with YAML frontmatter (`name`, `description`, `model`).
