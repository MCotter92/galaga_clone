import math


def figure_eight(amplitude_x, amplitude_y):
    # Gerono curve
    def curve(t):
        x = amplitude_x * math.sin(t)
        y = amplitude_y * math.sin(2 * t)
        return (x, y)

    return curve
