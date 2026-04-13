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
| `/design-system` | sonnet | Author full 8-section GDD (incremental write) |
| `/quick-design` | sonnet | GDD-lite for small features (3 sections) |
| `/design-review` | sonnet | Peer-review a GDD for completeness + consistency |
| `/update-gdd` | sonnet | Apply clarifications/decisions back into GDD |
| `/propagate-design-change` | sonnet | Cross-system impact analysis |

## Doc ↔ Code Sync (for GD+Dev teams)
| Skill | Model | Purpose |
|-------|-------|---------|
| `/diff-design` | sonnet | Git-diff a GDD to extract what changed |
| `/code-audit` | sonnet | Scan code vs GDD, list gaps |
| `/gap-report` | sonnet | Consolidate diff + audit into one report |
| `/clarify-gaps` | sonnet | Generate question list for GD |
| `/verify-against-doc` | sonnet | Verify code matches GDD §8 criteria |
| `/design-lock` | sonnet | Tag "doc == code" baseline |

## Sprint / story
| Skill | Model | Purpose |
|-------|-------|---------|
| `/sprint-status` | haiku | Read-only daily sprint snapshot |
| `/story-readiness` | haiku | Gate before `/dev-story` |
| `/create-stories` | sonnet | Break GDD/gap-report into stories |
| `/scope-check` | haiku | Classify task scope (XS/S/M/L/XL) |
| `/dev-story` | sonnet | Chain: planner → specialist → tester → reviewer |
| `/code-review` | sonnet | Deep code review, GDD alignment |
| `/story-done` | haiku | Close story, move to done folder |

## QA / bugs / balance
| Skill | Model | Purpose |
|-------|-------|---------|
| `/triage-bug` | sonnet | Classify severity + produce bug story |
| `/regression-check` | sonnet | Verify tests pass after change |
| `/balance-tune` | sonnet | Data-only numeric tunes with rationale |

## Release
| Skill | Model | Purpose |
|-------|-------|---------|
| `/gate-check` | opus | Phase gate verdict (PASS/CONCERNS/FAIL) |
| `/patch-notes` | haiku | Generate player-facing release notes |

## Model tier rationale

- **Haiku**: read-only status, formatting, simple lookups — cheap + fast
- **Sonnet**: default for most work (design auth, code, review)
- **Opus**: multi-document synthesis, high-stakes verdicts (e.g., phase gates)

## Adding your own skill

```bash
ugk list skills             # See available catalog
# or write a new skill file:
echo '---' > .claude/skills/my-skill.md
echo 'name: my-skill' >> .claude/skills/my-skill.md
# ...
```

Path: `.claude/skills/<name>.md` with YAML frontmatter (`name`, `description`, `model`).
