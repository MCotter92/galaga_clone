import math


class Route:
    def __init__(self, curve, rads_per_sec, start_t=0):
        self.curve = curve
        self.rads_per_sec = rads_per_sec
        # f(x(t), y(t))
        self.start_t = start_t
        self.t = start_t
        # One full lap from wherever the route starts.
        self.lap_t = start_t + 2 * math.pi
        self.finished = False

    def update(self, dt):
        self.t += self.rads_per_sec * dt

        if self.t >= self.lap_t:
            self.finished = True

        return self.curve(self.t)

    def reset(self):
        self.t = self.start_t
        self.finished = False
