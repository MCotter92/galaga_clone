# galaga_clone
Its a galaga clone. Not 1:1. Just for fun.

## Plan
A big refactor to make enemies and levels behave like real Galaga:
**endless formation waves** (no discrete levels), enemies that fly into a formation, shoot, and dive at the player, and an open-ended high-score game that ends on death/quit and records scores to a JSON file.

**Confirmed decisions**
- Endless Galaga-style formation waves (enemies continuously swarm into an oscillating formation that reseeds itself; difficulty ramps forever).
- Player death shows a brief game-over overlay with the final score.
- Scores saved to a gitignored `scores.json` — a list of every run plus a best-score field.
- Enemy/formation config is data-driven (JSON/Python dicts).
- Enemy movement lives in reusable **path objects**, switched by an **enemy state machine**.

### [ ]  Phase 0 — Motion & timing foundation
Today enemy movement is `x = f(y)` with constant vertical speed (`assets/paths.py`, `assets/enemy.py`). That only supports "fall straight down," which is useless for Galaga flight.

- Rebuild the path system as **route objects**: parametric curves and waypoint lists that drive an enemy's velocity and report when the path is finished (so the caller can switch behavior).
- Add a lightweight **tick/timer/scheduler** helper so the game can choreograph entrance fly-ins, dive calls, and formation restocks on a schedule.

**Research pointers**
- "spline/parametric curves for game movement" (bezier, catmull-rom) — good for smooth fly-in curves.
- "waypoint path following + arrival detection".
- "cooldown/timer pattern in game loops" (frame-based vs delta-time timing).

### [ ]  Phase 1 — Enemy archetypes + state machine (data-driven)
All enemies are currently identical (`factory/factory.py`). Introduce distinct enemy types and per-enemy behavior.

- `data/enemies.json`: archetype = sprite, size, HP, speed, fire rate, score value, and which dive/path patterns it can use. (Sprite pool: the existing `tiny-spaceships/` set.)
- **Enemy FSM**: `ENTERING → IN_FORMATION → (DIVING | SHOOTING) → RETURN/EXIT → DEAD`. Each state is driven by a path object; remove the inline movement logic from `assets/enemy.py`.

**Research pointers**
- "finite state machines in game AI" (and "state pattern" OOP).
- "data-driven enemy definitions / config-driven game objects".

### [ ] Phase 2 — Formation system
- `data/formations.json`: slot-layouts (chevron/bracket grids), target positions per slot, oscillation/shimmy parameters, and rules for who dives.
- A `Formation` object owns: the filled slot registry, the whole formation's side-to-side shimmy, and a **dive scheduler** that picks slots to peel off and which pattern to use.

**Research pointers**
- "Galaga formation" / "Galaga slot grid" — the wave is a fixed 5x-gapped pattern of (~40) slots.
- "boids / formation movement" in games.
- "scheduler pattern — round-robin dive selection".

### [ ]  Phase 3 — Endless director replaces `Level`
Delete `Level` (`assets/level.py`), `level_generator`/`create_enemies` (`factory/factory.py`), and the level-regen block in `main.py`.

- New `director.py`: an **open-ended wave generator** — reseeds the formation Galaga-style (anti-camping: enemies replenish if you stall), never "completes," and ramps difficulty by wave count/time (speed, aggression, diver count).
- This also kills the dead `enemy_count` variable and the buggy `enemy_list[i]` indexing.

**Research pointers**
- "Galaga wave system / enemy restock mechanic" — waves keep refilling a stage if you camp.
- "difficulty scaling curves in arcade games".

### [ ]  Phase 4 — Enemy projectiles & collision routing
- New `enemy_bullets_group`; enemy fire behavior (aimed/spread, rate) from archetype data. Formation and divers both shoot.
- Rework `collisions/collisions.py`: route collisions per group type, award score on enemy kill, player takes damage from enemies and enemy bullets, and player death triggers the game-over path.

**Research pointers**
- "aimed shots / bullet spread" math (vector toward player).
- "pygame sprite group collision between specific groups" (`pygame.sprite.groupcollide`).

### [ ] Phase 5 — Score + JSON high score + game-over
- Score tracker (points come from archetype data).
- Player death → brief game-over overlay with final score; Q quits. Either path appends the run to `scores.json` (list of runs + best field) — make sure the file is `.gitignore`d.
- Minimal on-screen score readout (full HUD/menu stays in the "Later" todo).

**Research pointers**
- "JSON save/load in Python" (`json` module).
- "game-over screen flow in pygame".

### [ ] Phase 6 — `main.py` rewrite
Thin loop: input → player/enemy/director updates → collisions → draw → game-over/exit. The old level-regeneration loop disappears; `groups.py` globals get re-homed under the director.

**Research pointers**
- "game loop structure" (input → update → render).
- "ownership of sprite groups — why global groups become a problem" (name-spacing/tying sprites to their manager).

---

**Suggested order:** Phase 0 → 1 → 2 → 3 (along the way Phase 4's projectiles make gameplay come alive) → 5 → 6 (Phase 6 is mostly cleanup once the others land).

