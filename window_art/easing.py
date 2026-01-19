"""Easing functions for smooth animations."""
from __future__ import annotations

import math
from typing import Callable

EasingFunc = Callable[[float], float]


def linear(t: float) -> float:
    """Linear interpolation (no easing)."""
    return t


def ease_in_quad(t: float) -> float:
    """Quadratic ease-in."""
    return t * t


def ease_out_quad(t: float) -> float:
    """Quadratic ease-out."""
    return 1 - (1 - t) * (1 - t)


def ease_in_out_quad(t: float) -> float:
    """Quadratic ease-in-out."""
    if t < 0.5:
        return 2 * t * t
    return 1 - (-2 * t + 2) ** 2 / 2


def ease_in_cubic(t: float) -> float:
    """Cubic ease-in."""
    return t * t * t


def ease_out_cubic(t: float) -> float:
    """Cubic ease-out."""
    return 1 - (1 - t) ** 3


def ease_in_out_cubic(t: float) -> float:
    """Cubic ease-in-out."""
    if t < 0.5:
        return 4 * t * t * t
    return 1 - (-2 * t + 2) ** 3 / 2


def ease_in_quart(t: float) -> float:
    """Quartic ease-in."""
    return t * t * t * t


def ease_out_quart(t: float) -> float:
    """Quartic ease-out."""
    return 1 - (1 - t) ** 4


def ease_in_out_quart(t: float) -> float:
    """Quartic ease-in-out."""
    if t < 0.5:
        return 8 * t * t * t * t
    return 1 - (-2 * t + 2) ** 4 / 2


def ease_in_quint(t: float) -> float:
    """Quintic ease-in."""
    return t * t * t * t * t


def ease_out_quint(t: float) -> float:
    """Quintic ease-out."""
    return 1 - (1 - t) ** 5


def ease_in_out_quint(t: float) -> float:
    """Quintic ease-in-out."""
    if t < 0.5:
        return 16 * t * t * t * t * t
    return 1 - (-2 * t + 2) ** 5 / 2


def ease_in_sine(t: float) -> float:
    """Sinusoidal ease-in."""
    return 1 - math.cos(t * math.pi / 2)


def ease_out_sine(t: float) -> float:
    """Sinusoidal ease-out."""
    return math.sin(t * math.pi / 2)


def ease_in_out_sine(t: float) -> float:
    """Sinusoidal ease-in-out."""
    return -(math.cos(math.pi * t) - 1) / 2


def ease_in_expo(t: float) -> float:
    """Exponential ease-in."""
    if t == 0:
        return 0
    return 2 ** (10 * t - 10)


def ease_out_expo(t: float) -> float:
    """Exponential ease-out."""
    if t == 1:
        return 1
    return 1 - 2 ** (-10 * t)


def ease_in_out_expo(t: float) -> float:
    """Exponential ease-in-out."""
    if t == 0:
        return 0
    if t == 1:
        return 1
    if t < 0.5:
        return 2 ** (20 * t - 10) / 2
    return (2 - 2 ** (-20 * t + 10)) / 2


def ease_in_circ(t: float) -> float:
    """Circular ease-in."""
    return 1 - math.sqrt(1 - t * t)


def ease_out_circ(t: float) -> float:
    """Circular ease-out."""
    return math.sqrt(1 - (t - 1) ** 2)


def ease_in_out_circ(t: float) -> float:
    """Circular ease-in-out."""
    if t < 0.5:
        return (1 - math.sqrt(1 - (2 * t) ** 2)) / 2
    return (math.sqrt(1 - (-2 * t + 2) ** 2) + 1) / 2


def ease_in_back(t: float) -> float:
    """Back ease-in (overshoots at start)."""
    c1 = 1.70158
    c3 = c1 + 1
    return c3 * t * t * t - c1 * t * t


def ease_out_back(t: float) -> float:
    """Back ease-out (overshoots at end)."""
    c1 = 1.70158
    c3 = c1 + 1
    return 1 + c3 * (t - 1) ** 3 + c1 * (t - 1) ** 2


def ease_in_out_back(t: float) -> float:
    """Back ease-in-out (overshoots at both ends)."""
    c1 = 1.70158
    c2 = c1 * 1.525
    if t < 0.5:
        return ((2 * t) ** 2 * ((c2 + 1) * 2 * t - c2)) / 2
    return ((2 * t - 2) ** 2 * ((c2 + 1) * (t * 2 - 2) + c2) + 2) / 2


def ease_in_elastic(t: float) -> float:
    """Elastic ease-in."""
    if t == 0:
        return 0
    if t == 1:
        return 1
    c4 = (2 * math.pi) / 3
    return -(2 ** (10 * t - 10)) * math.sin((t * 10 - 10.75) * c4)


def ease_out_elastic(t: float) -> float:
    """Elastic ease-out."""
    if t == 0:
        return 0
    if t == 1:
        return 1
    c4 = (2 * math.pi) / 3
    return 2 ** (-10 * t) * math.sin((t * 10 - 0.75) * c4) + 1


def ease_in_out_elastic(t: float) -> float:
    """Elastic ease-in-out."""
    if t == 0:
        return 0
    if t == 1:
        return 1
    c5 = (2 * math.pi) / 4.5
    if t < 0.5:
        return -(2 ** (20 * t - 10) * math.sin((20 * t - 11.125) * c5)) / 2
    return (2 ** (-20 * t + 10) * math.sin((20 * t - 11.125) * c5)) / 2 + 1


def ease_out_bounce(t: float) -> float:
    """Bounce ease-out."""
    n1 = 7.5625
    d1 = 2.75
    if t < 1 / d1:
        return n1 * t * t
    elif t < 2 / d1:
        t -= 1.5 / d1
        return n1 * t * t + 0.75
    elif t < 2.5 / d1:
        t -= 2.25 / d1
        return n1 * t * t + 0.9375
    else:
        t -= 2.625 / d1
        return n1 * t * t + 0.984375


def ease_in_bounce(t: float) -> float:
    """Bounce ease-in."""
    return 1 - ease_out_bounce(1 - t)


def ease_in_out_bounce(t: float) -> float:
    """Bounce ease-in-out."""
    if t < 0.5:
        return (1 - ease_out_bounce(1 - 2 * t)) / 2
    return (1 + ease_out_bounce(2 * t - 1)) / 2


ease_in = ease_in_quad
ease_out = ease_out_quad
ease_in_out = ease_in_out_quad


EASING_FUNCTIONS: dict[str, EasingFunc] = {
    "linear": linear,
    "ease_in": ease_in,
    "ease_out": ease_out,
    "ease_in_out": ease_in_out,
    "ease_in_quad": ease_in_quad,
    "ease_out_quad": ease_out_quad,
    "ease_in_out_quad": ease_in_out_quad,
    "ease_in_cubic": ease_in_cubic,
    "ease_out_cubic": ease_out_cubic,
    "ease_in_out_cubic": ease_in_out_cubic,
    "ease_in_quart": ease_in_quart,
    "ease_out_quart": ease_out_quart,
    "ease_in_out_quart": ease_in_out_quart,
    "ease_in_quint": ease_in_quint,
    "ease_out_quint": ease_out_quint,
    "ease_in_out_quint": ease_in_out_quint,
    "ease_in_sine": ease_in_sine,
    "ease_out_sine": ease_out_sine,
    "ease_in_out_sine": ease_in_out_sine,
    "ease_in_expo": ease_in_expo,
    "ease_out_expo": ease_out_expo,
    "ease_in_out_expo": ease_in_out_expo,
    "ease_in_circ": ease_in_circ,
    "ease_out_circ": ease_out_circ,
    "ease_in_out_circ": ease_in_out_circ,
    "ease_in_back": ease_in_back,
    "ease_out_back": ease_out_back,
    "ease_in_out_back": ease_in_out_back,
    "ease_in_elastic": ease_in_elastic,
    "ease_out_elastic": ease_out_elastic,
    "ease_in_out_elastic": ease_in_out_elastic,
    "ease_in_bounce": ease_in_bounce,
    "ease_out_bounce": ease_out_bounce,
    "ease_in_out_bounce": ease_in_out_bounce,
}


def get_easing(name: str | EasingFunc) -> EasingFunc:
    """Get an easing function by name or return the function if already callable."""
    if callable(name):
        return name
    name_normalized = name.lower().replace("-", "_").replace(" ", "_")
    if name_normalized not in EASING_FUNCTIONS:
        raise ValueError(
            f"Unknown easing function: {name}. "
            f"Available: {', '.join(EASING_FUNCTIONS.keys())}"
        )
    return EASING_FUNCTIONS[name_normalized]
