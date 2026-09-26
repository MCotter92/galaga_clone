import math


class Route:
    # TODO: `curve` is expected to be a plain callable taking a single argument `t`
    # (radians) and returning a `(x, y)` pair, e.g. the closure produced by
    # `game_math.curves.figure_eight`. Nothing enforces this shape. If a caller ever
    # passes an already-evaluated tuple instead of the callable, the failure will
    # surface deep inside `update` as an unhelpful "tuple is not callable" rather than
    # at construction time, which is where the mistake is made. Consider validating the
    # callable on construction so the error points at the real culprit.
    #
    # TODO: The unit and frame of reference of the returned `(x, y)` pair are currently
    # undefined and this is the source of the "enemy sits in the top left" bug. The
    # curve currently returns offsets around the origin, but `Enemy.update` assigns the
    # result directly to `self.rect.topleft`, which interprets those offsets as absolute
    # screen coordinates and throws away the enemy's `start_x` / `start_y`. Pick one and
    # state it: either routes return offsets relative to a spawn anchor that the Route
    # owns, or routes return absolute screen positions and the curve should be built
    # around the spawn point. Whichever is chosen, the anchor belongs in the signature or
    # a docstring so the contract is readable at both ends.
    def __init__(self, curve, rads_per_sec, start_t=0):
        self.curve = curve
        self.rads_per_sec = rads_per_sec
        # f(x(t), y(t))
        self.t = start_t
        # TODO: `finished` is written but never read by any module, and `reset()` is
        # never called. Looping right now is an accidental side effect of `sin` being
        # periodic, not a deliberate state transition. Decide what should actually happen
        # when a route completes a lap: loop indefinitely (in which case `lap_t` and
        # `finished` are redundant, since `t` can just keep growing and the curve wraps
        # on its own), exit the screen, fire a callback, or hand control to a different
        # path. That decision determines whether `Route` stays a pure clock or grows into
        # something that owns an enemy's lifecycle, and it will be much harder to change
        # once multiple routes per enemy exist.
        self.lap_t = 2 * math.pi
        self.finished = False

    def update(self, dt) -> tuple[float, float]:
        # TODO: Nothing here clamps or validates `dt`. If a caller passes a bad value,
        # such as the window height instead of the frame delta, `t` jumps by thousands of
        # radians in a single frame and the path becomes noise. A guard that rejects
        # implausibly large deltas would turn a confusing visual glitch into an obvious
        # error, but decide carefully: a legitimate hitch or a debug time-scale
        # multiplier may need large deltas to survive, so a hard clamp is not obviously
        # the right answer.
        self.t += self.rads_per_sec * dt

        if self.t >= self.lap_t:
            self.finished = True

        return self.curve(self.t)

    def reset(self):
        self.t = 0
        self.finished = False
