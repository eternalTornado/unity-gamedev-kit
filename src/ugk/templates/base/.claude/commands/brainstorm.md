---
name: brainstorm
description: 6-phase ideation that produces a game-concept.md with pillars, MDA analysis, core loop, target audience, and anti-pillars. Use at project kickoff or when pivoting.
---

# /brainstorm — Game Concept Ideation

## Output

`Design/GDD/game-concept.md` with these sections:

1. **Elevator pitch** (one sentence)
2. **Core experience** (what the player imagines themselves doing)
3. **MDA breakdown** (Mechanics, Dynamics, Aesthetics)
4. **Target audience** (Bartle types + demographics)
5. **Core loop diagram** (arrows in text)
6. **Unique Selling Proposition**
7. **Comparable titles + differentiation**
8. **Game pillars** (3-5 non-negotiable design values)
9. **Anti-pillars** (what this game intentionally avoids)

## 6-phase process

1. **Gather constraints** — use the `AskUserQuestion` tool to batch ALL constraint questions into ONE call (max 4). Typical:
   - **Genre direction**: "Action/combat", "Puzzle", "RPG/narrative", "Strategy/sim"
   - **Platform**: "PC only", "Mobile only", "PC + Mobile", "Console + PC"
   - **Scope**: "Prototype (1-2 months)", "Vertical slice (3-6 months)", "Full production (12+ months)"
   - **Team size**: "Solo", "2-4 devs", "5-10 devs", "10+ devs"

   For the open-ended "what's the theme/setting?" question, ask free-form in chat (it's not enumerable). Everything else uses AskUserQuestion.

2. **Generate 10 concept seeds** — each with one-line pitch + MDA tags. Present as a numbered list.

3. **Narrow to 2-3 favorites** — use `AskUserQuestion` with the 10 seeds as options (multi-select), asking the user to pick 2-3.

4. **Deep MDA analysis** on each favorite — present side-by-side, then use `AskUserQuestion` to pick the winner.

5. **Player motivation mapping** (Bartle: Achiever/Explorer/Socializer/Killer + SDT: Autonomy/Competence/Relatedness) for the winner.

6. **Winner formalization** — draft each section incrementally, user approves one at a time, write to file immediately after each approval.

## Incremental writing

Create `Design/GDD/game-concept.md` with skeleton (all 9 section headers, empty bodies) after the winner is picked. Fill one section at a time with approval between each.

## Collaboration protocol

- Use `AskUserQuestion` for every enumerable choice.
- Only fall back to free-form chat questions when the answer cannot be enumerated (themes, descriptions, proper nouns).
- Never draft multiple sections at once — one section, one approval, one write.

## Suggested next step

End with a "Suggested next step" block. Typical options:

- `/design-review Design/GDD/game-concept.md` — validate the concept against design theory
- `/setup-engine` — configure the tech stack
- `/map-systems` — enumerate the systems this game will need
- `/gate-check concept` — verify Phase 1 is complete
