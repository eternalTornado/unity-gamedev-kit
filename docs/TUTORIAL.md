# Tutorial — Build a Demo Unity Game with `ugk`

This tutorial walks you from a blank Unity project to a shippable vertical slice using `ugk` and Claude Code. Estimated time: **2–3 hours** (most is brainstorm + design, not code).

We'll build **"Orbit Runner"** — a 1-button hyper-casual mobile game where the player orbits a planet and dodges meteors.

---

## 0. Setup

### 0.1 Prereqs

- Finished [INSTALL.md](./INSTALL.md)
- Unity Hub with Unity 6 (6000.x LTS)
- A blank Unity 3D Core project at `~/UnityProjects/OrbitRunner`
- Claude Code open, connected to that folder

### 0.2 Bootstrap the kit

```bash
cd ~/UnityProjects/OrbitRunner
ugk init . --engine unity-6 --scope mobile-casual
ugk check
```

Expected output: green checks for git, Python, and `.claude/hooks/` present.

Commit:

```bash
git add .
git commit -m "chore: bootstrap unity-gamedev-kit v0.1.0"
```

---

## Phase 1 — Concept

### 1.1 Open Claude Code and run `/start`

Claude reads `CLAUDE.md`, detects no concept exists, and routes you to brainstorm.

```
> /start
```

It will ask which path fits:

- **A** — No idea yet
- **B** — Vague idea ("something with orbits")
- **C** — Clear concept
- **D** — Existing project

Pick **B**.

### 1.2 Brainstorm

```
> /brainstorm hyper-casual orbit mechanic
```

Claude generates 10 concept seeds with MDA (Mechanics-Dynamics-Aesthetics). You pick 2-3 favorites. It does player motivation mapping, then drafts `Design/GDD/game-concept.md` with:

- Elevator pitch
- Core fantasy
- Target audience (Bartle types)
- Core loop diagram
- 3-5 game pillars
- Anti-pillars (what this game refuses to be)

**Approve** each section before Claude writes to file.

### 1.3 Pin engine + map systems

```
> /setup-engine unity-6
> /map-systems
```

`systems-index.md` lists every system: Orbit, Meteor Spawner, Score, Game Over, Main Menu, Progression, Settings. Each gets a priority tier (MVP / Vertical Slice / Alpha).

### 1.4 Gate check

```
> /gate-check concept
```

Verdict: `PASS` → move to Phase 2.

---

## Phase 2 — Systems Design

### 2.1 Design each MVP system

```
> /design-system orbit
```

Claude walks you through the **8 required sections**:

1. Overview
2. Player Fantasy
3. Detailed Rules
4. Formulas (with variables, ranges, examples)
5. Edge Cases (explicit resolution, not "handle gracefully")
6. Dependencies (bidirectional)
7. Tuning Knobs (safe ranges)
8. Acceptance Criteria (testable)

Plus a **Game Feel** section for orbit speed, input responsiveness, juice.

Each section is incremental: Question → Options → Decision → Draft → Approval → Write to file. You never lose work to a context crash.

Repeat for `meteor-spawner`, `score`, `game-over`.

### 2.2 Cross-GDD review

```
> /review-all-gdds
```

Claude reads all GDDs at once and checks:

- Bidirectional dependencies (A references B → does B reference A?)
- Rule contradictions
- Dominant strategies
- Economic loops
- Pillar alignment

Output: `Design/GDD/gdd-cross-review-<date>.md`.

### 2.3 Gate check

```
> /gate-check systems
```

---

## Phase 3 — Technical Setup

### 3.1 Master architecture

```
> /create-architecture
```

Produces `Docs/architecture/architecture.md` with system boundaries, data flow, integration points.

### 3.2 Architecture Decision Records (ADRs)

```
> /architecture-decision "DI container: VContainer vs Zenject"
> /architecture-decision "Event bus: SignalBus vs MessagePipe"
> /architecture-decision "Async lib: UniTask vs Coroutines"
```

Each ADR has: context, options, chosen option, consequences, dependencies.

Minimum 3 Foundation-layer ADRs before gate.

### 3.3 Gate check

```
> /gate-check tech
```

---

## Phase 4 — Pre-Production

```
> /create-epics
> /create-stories
> /sprint-plan
```

Claude turns systems into Epics → Stories. Each story has acceptance criteria and a test plan.

---

## Phase 5 — Production

### 5.1 Implement a story

```
> /dev-story ORBIT-001
```

Claude delegates to:
1. `planner` agent — creates TODO list in `Production/plans/ORBIT-001.md`
2. `gameplay-programmer` agent — writes C# code in `Assets/Scripts/Gameplay/Orbit/`
3. `tester` agent — writes unit tests in `Tests/Unit/`
4. `code-reviewer` agent — verifies priority hierarchy:
   - 🔴 Quality: nullable types, no warnings, throw not log
   - 🟡 Modern C#: LINQ, expression bodies
   - 🟢 Architecture: VContainer DI, Data Controllers
   - 🔵 Performance: no LINQ in Update, no alloc in hot path

Path-scoped rules fire automatically: code in `Assets/Scripts/Gameplay/` enforces data-driven values, no UI coupling.

### 5.2 Hook enforcement

Try to commit a GDD missing the "Formulas" section → `validate-commit.sh` blocks you.
Try to commit `Data/meteors.json` with broken JSON → blocked.
Try to push to `main` without a PR → `validate-push.sh` warns you.

### 5.3 Gate check

```
> /gate-check prod
```

---

## Phase 6 — Polish

```
> /perf-profile
> /balance-check
> /playtest-report
```

Profile target: 60 FPS on iPhone 12, <100MB RAM, <30MB install.

---

## Phase 7 — Release

```
> /release-checklist
```

Verifies: version bumped, changelog written, store metadata ready, privacy policy linked, crash reporter installed, analytics events firing.

```
> /gate-check release
```

`PASS` → you're ready to ship.

---

## Team workflow

When another dev joins:

```bash
git clone <your-repo>
cd OrbitRunner
ugk check              # verify their tooling
```

They open Claude Code — the `session-start.sh` hook prints:

- Current branch
- Recent commits
- Active sprint
- Open bugs
- TODO/FIXME counts
- Recovery state if previous session crashed

They type `/help` — Claude reads `Production/stage.txt` and tells them exactly what phase the team is in and what the next task is.

## Troubleshooting

See [INSTALL.md](./INSTALL.md) troubleshooting section and open an issue at the repo.
