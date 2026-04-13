# Changelog

All notable changes to `unity-gamedev-kit` are documented here.

Format follows [Keep a Changelog](https://keepachangelog.com/). Versioning follows [SemVer](https://semver.org/).

## [Unreleased]

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
