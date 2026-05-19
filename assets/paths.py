import math


class StraightPath:
    def path(self, x_intercept, y):
        return x_intercept


class SinePath(StraightPath):
    """
    x_intercept + amplitude * sin(period(x+phase_shift)) +D
    """

    def __init__(self, amplitude, frequency, phase):
        self.amplitude = amplitude
        self.frequency = frequency
        self.phase = phase

    def path(self, x_intercept, y):
        return x_intercept + self.amplitude * math.sin(self.frequency * y + self.phase)


class CosinePath(StraightPath):
    """
    x_intercept + amplitude * sin(period(x+phase_shift)) +D
    """

    def __init__(self, amplitude, frequency, phase):
        self.amplitude = amplitude
        self.frequency = frequency
        self.phase = phase

    def path(self, x_intercept, y):
        return x_intercept + self.amplitude * math.cos(self.frequency * y + self.phase)


class ZigZagPath(StraightPath):
    """
    zig zags right then left.
    """

    def __init__(self, amplitude, frequency):
        self.amplitude = amplitude
        self.frequency = frequency

    def path(self, x_intercept, y):
        t = (y * self.frequency) % (2 * math.pi)
        triangle = (2 / math.pi) * math.asin(math.sin(t))
        return x_intercept + self.amplitude * triangle


class ReverseZigZagPath(StraightPath):
    """
    zig zags left then right.
    """

    def __init__(self, amplitude, frequency):
        self.amplitude = amplitude
        self.frequency = frequency

    def path(self, x_intercept, y):
        t = (y * self.frequency) % (2 * math.pi)
        triangle = (2 / math.pi) * math.acos(math.sin(t))
        return x_intercept + self.amplitude * triangle
