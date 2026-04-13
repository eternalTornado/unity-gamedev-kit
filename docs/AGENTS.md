# Agents Reference

All 13 agents shipped with unity-gamedev-kit. See `ugk list agents` in CLI.

## Leadership (Opus tier)
| Agent | Role |
|-------|------|
| `creative-director` | Game pillars, creative vision, design conflicts |
| `technical-director` | Architecture, performance, ADRs |

## Design (Sonnet)
| Agent | Role |
|-------|------|
| `game-designer` | Mechanic-level GDD authoring |
| `level-designer` | Scene flow, encounter pacing |
| `narrative-designer` | Story, dialog, lore |
| `ui-designer` | Screens, HUD, UX specs |
| `balance-designer` | Curves, formulas, tuning values |

## Engineering (Sonnet)
| Agent | Role |
|-------|------|
| `programmer` | Default implementer for `/dev-story` |
| `unity-specialist` | Unity engine expert + sub-specialist router |
| `tester` | Write + run tests per test-standards |
| `code-reviewer` | Code review per `/code-review` checklist |

## Process (Sonnet)
| Agent | Role |
|-------|------|
| `planner` | First step of `/dev-story` — analysis only, no writes |
| `producer-lite` | Coordination for small teams without a real producer |
| `qa-lead` | Test strategy, playtest plans, bug triage policy |

## How agents are invoked

1. **Explicit**: a skill spawns a named agent via Task tool (e.g., `/dev-story` spawns `planner` → `programmer` → `tester` → `code-reviewer`)
2. **Routing**: file path maps to specialist (via `.claude/rules/*-code.md` frontmatter)
3. **Escalation**: an agent delegates to a parent (e.g., `game-designer` → `creative-director` for pillar conflicts)

## Coordination rules (enforced)

- Vertical delegation: leadership → department → specialist (no skipping tiers)
- Horizontal consultation allowed but not binding
- Conflicts escalate to shared parent (or `creative-director` / `technical-director`)
- No unilateral cross-domain changes

See `.claude/docs/coordination-rules.md` inside an initialized project for full policy.

## Adding your own agent

Create `.claude/agents/<name>.md` with frontmatter:
```yaml
---
name: my-agent
description: What this agent does
tools: [Read, Grep, Glob, Write, Edit, Bash]
model: sonnet   # haiku | sonnet | opus
---
```
