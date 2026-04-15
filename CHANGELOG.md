# Changelog

All notable changes to `unity-gamedev-kit` are documented here.

Format follows [Keep a Changelog](https://keepachangelog.com/). Versioning follows [SemVer](https://semver.org/).

## [1.1.0] — 2026-04-15

### Changed — Workflow restructure (BREAKING)
- **5-phase workflow** replaces 7-phase. New phases: Concept → Systems Design → Architecture → Implementation → Polish.
- `/gate-check` phases renamed: `tech` → `architecture`, `preprod` + `prod` merged into `implementation`, `polish` + `release` merged into `polish`.
- Phase 4 (Implementation) now delegates to [speckit](https://github.com/github/spec-kit) for `/plan` → `/tasks` → `/implement`. `/speckit.specify` is skipped because the GDD already contains the feature spec.
- Document locations for speckit outputs: `Docs/specs/<module>/plan.md`, `tasks.md` (override of speckit's default `specs/<feature>/`).

### Added — New command
- `/implement <module>` — Phase 4 entry point. Reads GDD + architecture doc, delegates to speckit (`/plan` → `/tasks` → `/implement`), finishes with `/code-review`.

### Changed — Commands
- `/dev-story` is deprecated. It redirects to `/implement`. Legacy `Production/stories/` workflow is no longer the canonical flow.
- All commands now MUST end with a **"Suggested next step"** block — a short list of 1-3 commands the user could run next.
- Commands that collect user input (`/start`, `/setup-engine`, `/brainstorm`, `/map-systems`, `/design-system`, `/create-architecture`) now use the `AskUserQuestion` tool with **batched** questions (up to 4 per call). Free-form chat questions are reserved for truly open-ended inputs only.

### Added — Constitution-like features folded into CLAUDE.md
- **Session Rules** section: precedence hierarchy (GDD > CLAUDE.md > technical-preferences > rules > drafts), document focus (max 3 per task), `/clear` and `/compact` triggers, incremental writing.
- **Governance** section: AI must not self-approve gates, gate fail → fix → re-submit (max 2 cycles), P0 hotfix exception, constitution-like-change approval flow, compliance citations.
- **Speckit integration** section: explains the Phase 4 flow and where speckit writes its documents.

## [1.0.0] — 2026-04-13

First stable release. Covers the full GDD → Ship → Maintain workflow for Unity.

### Added — CLI
- `ugk add <kind> <name>` — install optional skill/agent/rule/hook/profile from catalog
- `ugk list [kind]` — list installable components with descriptions
- `ugk update [--dry-run] [--only KIND]` — upgrade kit files (hash-aware, preserves user edits)
- `ugk init --scope <mobile|pc|multiplayer>` — apply scope profile overlays on init

### Added — Doc ↔ Code Sync skills (for GD+Dev teams)
- `/diff-design` — git-diff a GDD to extract what changed
- `/code-audit` — scan code vs GDD, list gaps (MISSING / FORMULA / ORPHAN / AMBIGUOUS)
- `/gap-report` — consolidate multiple diff/audit outputs into one report
- `/clarify-gaps` — generate question list for GD with defaults
- `/verify-against-doc` — verify new code matches GDD acceptance criteria
- `/design-lock` — tag "doc == code" baseline for next diff cycle

### Added — Core workflow skills
- `/sprint-status` (haiku) — daily sprint snapshot
- `/story-readiness` (haiku) — gate before `/dev-story`
- `/story-done` (haiku) — close story cleanly with prereq checks
- `/create-stories` — break GDD or gap-report into concrete stories
- `/scope-check` (haiku) — classify task scope XS/S/M/L/XL
- `/design-review` — peer-review a GDD
- `/code-review` — deep code review with GDD alignment checks
- `/quick-design` — GDD-lite (3 sections) for small features
- `/triage-bug` — intake + classify bug report
- `/balance-tune` — data-only numeric tunes with rationale trail
- `/propagate-design-change` — cross-system impact analysis
- `/regression-check` — verify tests pass after change
- `/update-gdd` — apply decisions back into GDD
- `/patch-notes` (haiku) — release notes generator

### Added — Agents (12 new, 13 total)
- `creative-director` (opus) — pillars, creative conflicts
- `technical-director` (opus) — ADRs, performance, architecture
- `game-designer`, `level-designer`, `narrative-designer`, `ui-designer`, `balance-designer`
- `programmer`, `tester`, `code-reviewer`, `planner`
- `producer-lite` — coordination for small teams without a real producer
- `qa-lead` — test strategy, playtest, bug triage policy

### Added — Scope profiles
- `mobile` — iOS/Android perf, touch input, store submission rules
- `pc` — desktop scalability, quality presets, Steam notes
- `multiplayer` — authority model, bandwidth, anti-cheat

### Added — Windows-native hooks
- `.ps1` versions of all 6 shell hooks (session-start, pre-compact, post-compact, validate-commit, validate-meta-files, detect-gaps)

### Added — CI templates
- `.github/workflows/unity-ci.yml` — EditMode + PlayMode tests, GDD section validation, commit-message validation on PRs
- `.github/workflows/build.yml` — multi-platform build with game-ci/unity-builder

### Added — Documentation
- `docs/WORKFLOW.md` — full task-type flows (existing GDD, new feature, bug, balance, reconcile loop)
- `docs/TEAMS.md` — solo / GD+Dev / small team / remote configurations
- `docs/SKILLS.md` — complete skill reference with model tiers
- `docs/AGENTS.md` — complete agent reference with delegation rules
- `docs/EXAMPLES.md` — 5 end-to-end scenarios

### Changed
- `ugk init` now supports `--scope` flag to apply profile overlays
- `ugk check` now counts skills and agents
- Classifiers bumped from Alpha to Production/Stable

## [0.1.0] — 2026-04-13

### Added
- Initial release — alpha
- `ugk init` bootstraps a Unity project with `.claude/` scaffold
- `ugk check` verifies tooling
- `ugk version` prints version
- 5 path-scoped rules: gameplay, UI, AI, engine, networking (Unity Assets/Scripts/** paths)
- 3 generic rules ported from CCGS: design-docs, test-standards, prototype-code
- 5 hooks: session-start, detect-gaps, validate-commit, pre-compact, post-compact
- 1 Unity-specific hook: validate-meta-files
- 5 skills: `/start`, `/brainstorm`, `/design-system`, `/dev-story`, `/gate-check`
- 1 agent: `unity-specialist`
- Base CLAUDE.md with priority hierarchy (Quality → Modern C# → Architecture → Performance)
- Collaboration Protocol (Question → Options → Decision → Draft → Approval)
- README, INSTALL guide, TUTORIAL (Orbit Runner demo), CONTRIBUTING, LICENSE
