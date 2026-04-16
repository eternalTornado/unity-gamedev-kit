# Changelog

All notable changes to `unity-gamedev-kit` are documented here.

Format follows [Keep a Changelog](https://keepachangelog.com/). Versioning follows [SemVer](https://semver.org/).

## [1.2.0] — 2026-04-16

### Changed — Quality Standards Backport from CCGS (MINOR — changes behavior of existing commands)

**B1: GDD language fix** — Corrected "GDD is the feature spec" → "After retrofit and gate-check PASS, the completed GDD serves as the feature spec." Raw GDDs are not specs until they pass retrofit + cross-review + gate. Updated in: `rules/design-docs.md`, `commands/adopt.md`, `commands/implement.md`, `commands/design-system.md`, template `CLAUDE.md`.

**B2: Acceptance Criteria quality rubric** — AC must now use Given-When-Then format. Minimum coverage: 1 AC per core rule + 1 AC per player-facing formula (internal formulas exempt). Every criterion must be independently verifiable by QA without reading the GDD. Performance budget criterion required. Updated in: `rules/design-docs.md`, `commands/adopt.md`, `commands/review-all-gdds.md`, new `commands/design-system-rubrics.md`.

**B3: Formulas completion steering** — Formulas must follow a structured format: formula expression, variable table (Variable | Type | Range | Description), output range, worked example. Prose-only formulas are no longer accepted. Updated in: `rules/design-docs.md`, `commands/design-system-rubrics.md`.

**B4: Edge Cases format** — Edge cases must use "If [exact condition]: [exact outcome]" format. "Handle gracefully" / "handle appropriately" is never acceptable. Updated in: `rules/design-docs.md`, `commands/design-system-rubrics.md`.

**B5: `/adopt` severity classification** — Gap report now classifies gaps as BLOCKING / HIGH / MEDIUM / LOW with severity summary. BLOCKING gaps (missing AC or Detailed Rules) prevent the GDD from serving as implementation spec. Gap report table includes a Severity column and ➖ marker for valid N/A sections.

**B6: Section N/A mechanism** — Formulas, Edge Cases, and Tuning Knobs may now be marked "N/A — [justification]" if the system genuinely has no content for them. Justification is required. Overview, Detailed Rules, Dependencies, and AC cannot be N/A. N/A requires user confirmation. Updated in: `rules/design-docs.md`, `commands/adopt.md`, `commands/design-system.md`, `commands/gate-check.md`.

**B8: `/start` bug fix** — Fixed "8 GDD sections" → "7 required GDD sections" (residual from v1.1.1 cleanup).

### Added

- **`commands/design-system-rubrics.md`** (NEW) — Quality rubrics for AC (Given-When-Then format, coverage rules, agent delegation to qa-lead), Formulas (variable table template, completion steering), and Edge Cases (format + examples). Extracted from `design-system.md` to keep the flow file lean.
- **Context 70% warning** on all long-running commands: `design-system.md`, `adopt.md`, `review-all-gdds.md`, `implement.md`, `create-architecture.md`. When context exceeds 70%, agent writes in-progress work to file and suggests `/compact`.

### Changed

- **`commands/design-system.md` split** — Flow-only file (~70 lines) now references `design-system-rubrics.md` for quality guidance. Removed Game Feel from required sections list (was already optional). Added N/A flow for eligible sections.

### Migration notes

- Existing GDDs written before v1.2.0 may not meet the stricter AC/Formulas/Edge Cases format. Run `/adopt` to get a severity-classified gap report showing what needs updating.
- N/A sections are a new capability — systems without formulas (e.g., Save System, Event Bus) can now explicitly mark "N/A — [reason]" instead of leaving sections empty or filling with placeholder content.

### NOT backported (and why)

- GDD template file (B7 REJECTED — GD sends any format, `/adopt` converts)
- Game Feel section (user decision: dropped entirely)
- Entity registry, agent routing table, director gates, recovery protocol, Visual/Audio/UI sections, Player Fantasy section — out of scope or previously removed

## [1.1.3] — 2026-04-15

### Added — `/create-architecture` output template (cherry-picked from external TDS template review)
- **Metadata header** is now a required first section in every `Docs/architecture/<system>.md`: System, Domain, GDD source, Primary architect, Unity version, Key dependencies. Gives downstream `/implement` + `programmer` agents unambiguous context in one block instead of scattered across the doc.
- **Unity Integration** is no longer a single prose paragraph. It splits into four required sub-fields so nothing silently drops: `MonoBehaviour vs plain C#`, `Execution Order`, `Asset Workflow`, `Optimization`. Previous wording collapsed these into "MonoBehaviour vs plain C#, scene structure, prefab strategy" and agents were skipping execution-order and optimization concerns.
- **Agent Directive callouts** — a one-line `> **Agent Directive:** …` is pinned at the top of each section of the output template. These are read-time instructions for downstream implementation agents so they stop "creatively re-interpreting" architecture docs.
- `commands/create-architecture.md` now embeds the full per-system output template as a fenced block so the structure is prescribed, not just described.

### Note
- This is additive — existing `Docs/architecture/<system>.md` files remain valid. New docs generated by `/create-architecture` after upgrade will follow the expanded template.
- Decision trade-offs still go in ADRs via `/architecture-decision`; the architecture doc itself stays prescriptive, not exploratory.

## [1.1.2] — 2026-04-15

### Fixed — Player Fantasy fully excised from runtime surface
- Agents were still proposing a `Player Fantasy` section during `/adopt` retrofits. Root cause: residual "player fantasy" phrasing in `creative-director` description, `design-docs` rule, and the `/adopt` note block nudged the model to re-introduce the 8th section. All runtime-facing mentions have been scrubbed.
- `creative-director` agent description: now owns "game pillars and tone" (no `player fantasy`).
- `rules/design-docs.md`: concept-doc hint rewritten without the word "fantasy".
- `/adopt`: legacy-section note replaced with a hard rule — never invent or re-add non-implementation-actionable sections; retrofit is strictly 7-section.
- `/brainstorm`, `/design-system`, `docs/TUTORIAL.md`, `docs/SKILLS.md`, `docs/AGENTS.md`: "fantasy" language replaced with "experience" / "creative framing" / "pillars" so nothing in the package re-suggests the removed section.

### Changed — `/adopt` gap report must use full section names
- The gap matrix table now **MUST** use full column headers (`Overview`, `Detailed Rules`, `Formulas`, `Edge Cases`, `Dependencies`, `Tuning Knobs`, `Acceptance Criteria`) — abbreviated codes like `1-Ov`, `4-Fo` are prohibited.

## [1.1.1] — 2026-04-15

### Changed — GDD format (7 sections, was 8)
- **Removed** `Player Fantasy` from mandatory GDD sections. The GDD is now the **feature spec** consumed by speckit in Phase 4, so sections must be implementation-actionable. Mood, tone, and player fantasy content belongs in `Design/GDD/game-concept.md`, not per-system GDDs.
- New mandatory 7 sections: Overview, Detailed Rules, Formulas, Edge Cases, Dependencies, Tuning Knobs, Acceptance Criteria (+ optional Game Feel).
- Updated files: `.claude/rules/design-docs.md` (source of truth), `.claude/commands/{adopt,design-system,design-review,review-all-gdds,diff-design,code-audit,update-gdd,quick-design,project-stage-detect,gate-check,implement,start}.md`, `.claude/hooks/validate-commit.sh`, `.github/workflows/unity-ci.yml`, template `CLAUDE.md`.
- `/adopt` now flags legacy `Player Fantasy` sections and offers to relocate their content into the concept doc.
- `creative-director` agent still owns player fantasy (now scoped to the concept doc).

### Migration notes
- Existing GDDs with a `Player Fantasy` section remain valid; run `/adopt` to relocate the content to `Design/GDD/game-concept.md` and drop the section.
- CI grep loop no longer warns on missing `Player Fantasy`.

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
