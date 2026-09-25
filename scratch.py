# Pseudocode reference for the route/formation plan. NOT runnable — this is notes.
#
# Decisions locked in:
#   - Each enemy owns its own route (no shared formation route object).
#   - A route reports `finished` after ONE lap. The caller decides what that means.
#   - Curve math goes in game_math/curves.py (pure, no pygame). Route objects go in assets/.
#   - `t` must be settable. It is the lever for respawn phase-match (S4) and for the
#     director to keep N independent routes in sync (S5). Do not skip this.
#
# Read top to bottom as the order of work. S1->S2 are headless-testable with no
# display; S3 is the first slice that touches the game.


# --------------------------------------------------------------------------------------
# S1 — the figure-8 curve. game_math/curves.py
# Pure math. Plain tuples, matching game_math/distance.py's existing style. No pygame.
# --------------------------------------------------------------------------------------

# FUNCTION figure8(t, amplitude_x, amplitude_y):
    # Gerono curve. amplitude_x = width of the 8, amplitude_y = height.
    # y uses sin(2t) so it reverses direction — this is the whole reason the old
    # x = f(y) path classes cannot express a closed loop.
    # x = amplitude_x * sin(t)
    # y = amplitude_y * sin(2 * t)
    # RETURN (x, y)


# Verify by hand, no game running:
#   t = 0        -> (0, 0)          <- the crossing point
#   t = pi/2     -> (ax, 0)         <- right lobe, y back at 0
#   t = pi       -> (0, 0)          <- back to the crossing
#   t = 3pi/2    -> (-ax, 0)        <- left lobe
#   t = 2pi      -> (0, 0)          <- EQUALS t=0. This equality is the closure test.
#
# Also check y is POSITIVE at pi/4 and NEGATIVE at 3pi/4. If it never changes
# sign you wrote a circle or an ellipse, not a figure 8.
#
# Known and accepted for now: advancing t at a constant rate does NOT give constant
# pixel speed. The ship whips through the crossing and crawls around the lobes.
# Fix is arc-length reparameterization. Do not open it until the rest works.


# --------------------------------------------------------------------------------------
# S2 — the route object. assets/
# Wraps a curve, owns progress. No pygame sprite, no image, no enemy knowledge.
# --------------------------------------------------------------------------------------
#
# CLASS Route:
#     FUNCTION __init__(curve, rate, start_t=0):
#         self.curve    = curve           # e.g. a partial of figure8
#         self.rate     = rate            # RADIANS PER SECOND, not pixels
#         self.t        = start_t         # settable ctor arg — see note above
#         self.lap_t    = 2 * pi          # the terminal value for this curve
#         self.finished = FALSE
#
#     FUNCTION advance(dt) -> position:
#         self.t += self.rate * dt
#         IF self.t >= self.lap_t:
#             self.finished = TRUE
#             # do NOT clamp or wrap here. Whether it loops, holds, or is torn down
#             # is the caller's decision. Clamping here bakes in the policy.
#         RETURN self.curve(self.t)
#
#     FUNCTION reset():
#         self.t        = 0               # or `start_t`, decided by the caller
#         self.finished = FALSE

# Note: `finished` stays TRUE once set. The caller is expected to consume it and
# call reset() if it wants another lap. Alternatively it self-clears on read.
# Pick one and be consistent — ambiguity here is what makes loops feel haunted.


# Headless verify:
#   route = Route(figure8_partial, rate=2*pi)      # 1 lap per second
#   FOR 600 iterations: route.advance(1/60)
#   EXPECT t ~= 2*pi after ~60 frames
#   EXPECT `finished` flipped exactly once over 600 frames
#   route.reset() -> finished is FALSE again
#
# This needs no display, no player, no enemies. Run it straight in a REPL.


# --------------------------------------------------------------------------------------
# S3 — one enemy on a route. assets/enemy.py + main.py
# First slice that touches the game. One enemy, hand-constructed in main. No director.
# --------------------------------------------------------------------------------------

# --- Enemy.__init__: delete this apparatus entirely, it is all x = f(y) scaffolding ---
#   - param `path`          (replaced by `route`)
#   - param `step`          (the spawn-frame-frozen speed — see below)
#   - self.x_intercept      (same number as start_x, two names)
#   - self.start_x
#   - self.start_y          (assigned at line 58, discards the y it was passed)
#   - self.speed            (frozen at construction: was `velo * dt` where dt was the
#                            SPAWN frame's dt. A hitching frame birthed a slow enemy
#                            forever. The route reads dt per frame, so this dies here.)
#   - self.angel            (typo, never read)
#
# --- Enemy.update: signature becomes update(self, dt, window_height) ---
#   OLD: coords[0] = self.sprite_path.path(x_intercept, coords[1])
#        coords[1] += self.speed
#        rect.topleft = coords
#   NEW: self.rect.topleft = self.route.advance(dt)
#
#   Position has THREE sources of truth today — rect, coords, healthbar — and they
#   disagree until the first update(). Collapse to one: the route's return value is
#   the single source, rect is derived from it, and `coords` either goes away or
#   becomes a property. Healthbar derives from rect as it already does.
#
# --- main.py ---
#   enemies_group.update(WINDOW_HEIGHT)  ->  enemies_group.update(dt, WINDOW_HEIGHT)
#
#   The call site is where the "caller decides" policy lives, and it is currently
#   the simplest possible version of it:
#       IF enemy.route.finished: enemy.route.reset()   # loops forever
#
#   Nothing changes with the off-screen cull at enemy.py:88. A centered figure-8
#   never trips it. It is still latent for dives — a diver that leaves the bottom
#   and curves back gets killed by it. Deal with that at the dive slice, not now.

# Verify: one visible 8, `finished` flips once per lap, speed looks right, no
# drift or judder. Kill it and confirm the cull behaviour is what you expect.


# --------------------------------------------------------------------------------------
# S4 — replacement on death. assets/enemy_director.py
# First slice with real state ("is slot N occupied?"). This is where a class beats a
# free function — a director with only `dt` as a parameter has nowhere to keep that.
# --------------------------------------------------------------------------------------

# CLASS EnemyDirector:
#     FUNCTION __init__(enemy_group, route_config):
#         self.enemy_group  = enemy_group
#         self.route_config = route_config  # amp_x, amp_y, rate — shared spawn config
#
#     FUNCTION update(dt):
#         # Death detection: before/after len(enemy_group) across the collision pass.
#         # Fine at this scale. Revisit only if double-spawns or misses show up.
#         before = len(self.enemy_group)
#         ...collisions happen in main between the two reads...
#         after = len(self.enemy_group)
#
#         IF after < before:
#             FOR each enemy that disappeared:
#                 phase = the t value it had when it died
#                 self.spawn_enemy(t=phase)   # SAME phase, or it teleports into the
#                                            # middle of the 8. This is why t is settable.
#
#     FUNCTION spawn_enemy(start_t=0):
#         enemy = Enemy(..., route=Route(curve, rate, start_t=start_t))
#         self.enemy_group.add(enemy)
#         RETURN enemy

# Also fold in here: delete all_sprites_group. Two writers (main for bullets, the
# director for enemies) and zero readers — nothing in the repo iterates it. The
# director is the last thing that would add a writer, so this is the cheap moment.

# Verify: shoot one, a replacement appears at the same phase of the 8, no
# double-spawn, nothing leaks when the player quits mid-frame.


# --------------------------------------------------------------------------------------
# S5 — formation. assets/
# N enemies, each with its own route, kept in sync by the director. Not a rigid
# Galaga formation — that is a later decision and this does not block it.
# --------------------------------------------------------------------------------------

# The cost of per-enemy routes, paid here: if every route self-advances its own t,
# they drift apart over time. So the director becomes the clock.

CLASS EnemyDirector:
    FUNCTION update(dt):
        self.clock += dt
        FOR each enemy in self.enemy_group:
            enemy.route.t = self.clock + enemy.phase_offset   # director DRIVES t
            # the route still owns curve evaluation; the director owns the clock
        ...repopulate any slot empty for longer than X seconds...

    FUNCTION spawn_enemy(slot_index):
        phase_offset = self.formation.phase_for_slot(slot_index)
        spawn_enemy(t = self.clock + phase_offset)

CLASS Formation:
    FUNCTION phase_for_slot(i) -> radians:
        # Vary by slot. Zero offset everywhere = a single stacked column that
        # reads as one ship, not a formation. Spread the offsets.
        # Deliberately coarse for the first look.

# Keep `Formation` this dumb. Slot occupancy, phase math, nothing else. It gets
# smarter at the dive slice, not before.


# --------------------------------------------------------------------------------------
# NOT YET — parked, do not open early
# --------------------------------------------------------------------------------------
#
# Entrance fly-in: enemies arrive from off-screen and come to REST on a slot. Needs a
#   finite route (this one is a closed loop and never arrives) plus a real arrival
#   concept. Also: the route ends at a fixed point, but a moving formation makes
#   that point stale. Settle live-seek-vs-stale-endpoint when you build it.
#
# Dive: a diver needs its own route for the duration, and the off-screen cull at
#   enemy.py:88 will kill it. A diver is also the moment "enemy left the group"
#   stops meaning "enemy died" — a director keyed on group length will start
#   restocking slots that divers are still using. Needs the state machine.
#
# Dive selection: round-robin over who peels off, and what pattern they use.
#
# Arc-length reparameterization: constant pixel speed along the curve. Fixes the
#   whip-through-the-crossing. Cosmetic until it isn't.
