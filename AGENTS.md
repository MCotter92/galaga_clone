# AGENTS.md

## Goal
The goal of this project is for the user to learn how to steer coding agents and find a workflow that works for him.

## File structure
- `assets/` — game entity classes (player, enemy, bullet, healthbar, route), shared sprite groups and colors, path constants, a spritesheet registry, plus `assets/images/` holding the background PNG, two sound effects, and the `tiny-spaceships/` sprite set (tinyShip1–20.png + readme).
- `collisions/` — `collisions.py`: pure collision detection between bullets/enemies and players/enemies.
- `game_math/` — small pure math helpers: `curves.py` (figure-eight) and `distance.py`.
- `renderers/` — `renderers.py`: the draw call that paints the window/sprites.
- `utils/` — `utils.py`: asset loading and other odds and ends.
- `changelog` — a single extensionless file at the top level (not a directory) tracking changes.

Top-level files: `main.py` (game loop and tuning constants), `logging_config.py` (logger setup; writes `game.log`), `pyproject.toml`, `requirements.txt`, `README.md`.

## Coding style

Design philosophy: Unix-style small, composable units with high cohesion and low coupling. Each function or module does one thing and has one reason to change.

- Keep functions short and single-purpose. If you need "and" to describe what one does, split it.
- Separate pure logic (computation, transformation) from side effects (I/O, network, filesystem, state). Side effects live at the edges.
- Modules communicate through small, explicit interfaces. Don't reach into another module's internals.
- Prefer composing existing small units over adding flags or options to an existing one.
- Don't add abstractions speculatively. Extract a new unit when there's a concrete second use or a clear separate responsibility.
- When touching existing code, don't refactor unrelated parts. Mention what you noticed instead.

## Running
 Manage with `uv` only. Add packages with `uv add`, never `pip`.
- Python `>=3.13` (`.python-version` pins 3.13).
- Direct dependency: `pygame-ce>=2.5.7`.

## Commit and PR policy
Never run `git commit`, `git push`, or create PRs or commit/PR messages. The user handles all of that.
