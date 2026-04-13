# Contributing

Thanks for your interest! `unity-gamedev-kit` is early alpha — contributions welcome, especially:

- Additional rule profiles (scope templates)
- New skills or agents
- Windows `.ps1` variants of shell hooks
- E2E tests
- Bug reports with reproduction steps

## Dev setup

```bash
git clone https://github.com/eternalTornado/unity-gamedev-kit.git
cd unity-gamedev-kit
uv pip install -e .
ugk --help
```

## Repo layout

```
unity-gamedev-kit/
├── src/ugk/
│   ├── cli.py                 # Typer entry point
│   ├── commands/              # init, check, update, add
│   └── templates/base/        # What gets copied by `ugk init`
├── docs/
├── tests/
└── pyproject.toml
```

## Adding a rule

1. Drop the file in `src/ugk/templates/base/.claude/rules/<name>.md`.
2. Add frontmatter `paths:` with a glob.
3. Open a PR with an example showing the rule in action.

## Adding a skill

1. Drop the file in `src/ugk/templates/base/.claude/skills/<name>.md`.
2. Add frontmatter `name:` + `description:` (triggering description).
3. Document the 7-phase position: which phase is this for?
4. Open a PR.

## Adding an agent

1. Drop the file in `src/ugk/templates/base/.claude/agents/<name>.md`.
2. Frontmatter `name:` + `description:` describing when Claude should invoke it.
3. List expertise, sub-specialists to route to, anti-patterns to block, escalation path.
4. Open a PR.

## Testing your changes

```bash
cd /tmp
mkdir test-project && cd test-project
ugk init .        # should scaffold without errors
ugk check         # all green
```

## Commit style

Conventional commits:

```
feat(skills): add /sprint-status
fix(hooks): correct jq fallback in validate-commit
docs(readme): clarify install instructions
chore: bump to v0.1.1
```

No AI attribution in commit messages (per TheOne Studio convention).

## Release

1. Bump version in `pyproject.toml` and `src/ugk/__init__.py`.
2. Update `CHANGELOG.md`.
3. Tag: `git tag -a v0.1.1 -m "..."`.
4. `git push origin v0.1.1`.
5. GitHub Actions publishes the release.
