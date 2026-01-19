"""2D vector math primitive."""
from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Iterator


@dataclass(slots=True)
class vec2:
    """A simple 2D vector class with common math operations."""

    x: float = 0.0
    y: float = 0.0

    def __add__(self, other: vec2 | tuple[float, float]) -> vec2:
        if isinstance(other, vec2):
            return vec2(self.x + other.x, self.y + other.y)
        return vec2(self.x + other[0], self.y + other[1])

    def __radd__(self, other: vec2 | tuple[float, float]) -> vec2:
        return self.__add__(other)

    def __sub__(self, other: vec2 | tuple[float, float]) -> vec2:
        if isinstance(other, vec2):
            return vec2(self.x - other.x, self.y - other.y)
        return vec2(self.x - other[0], self.y - other[1])

    def __rsub__(self, other: vec2 | tuple[float, float]) -> vec2:
        if isinstance(other, vec2):
            return vec2(other.x - self.x, other.y - self.y)
        return vec2(other[0] - self.x, other[1] - self.y)

    def __mul__(self, scalar: float) -> vec2:
        return vec2(self.x * scalar, self.y * scalar)

    def __rmul__(self, scalar: float) -> vec2:
        return self.__mul__(scalar)

    def __truediv__(self, scalar: float) -> vec2:
        return vec2(self.x / scalar, self.y / scalar)

    def __neg__(self) -> vec2:
        return vec2(-self.x, -self.y)

    def __iter__(self) -> Iterator[float]:
        yield self.x
        yield self.y

    def __getitem__(self, index: int) -> float:
        if index == 0:
            return self.x
        elif index == 1:
            return self.y
        raise IndexError(f"vec2 index out of range: {index}")

    @property
    def length(self) -> float:
        """Return the length (magnitude) of the vector."""
        return math.sqrt(self.x * self.x + self.y * self.y)

    @property
    def length_squared(self) -> float:
        """Return the squared length of the vector (faster than length)."""
        return self.x * self.x + self.y * self.y

    def normalized(self) -> vec2:
        """Return a unit vector in the same direction."""
        length = self.length
        if length == 0:
            return vec2(0, 0)
        return vec2(self.x / length, self.y / length)

    def dot(self, other: vec2) -> float:
        """Return the dot product with another vector."""
        return self.x * other.x + self.y * other.y

    def distance_to(self, other: vec2) -> float:
        """Return the distance to another vector."""
        return (self - other).length

    def lerp(self, other: vec2, t: float) -> vec2:
        """Linear interpolation to another vector."""
        return vec2(
            self.x + (other.x - self.x) * t,
            self.y + (other.y - self.y) * t,
        )

    def angle(self) -> float:
        """Return the angle of this vector in radians."""
        return math.atan2(self.y, self.x)

    def rotated(self, angle: float) -> vec2:
        """Return this vector rotated by the given angle (radians)."""
        cos_a = math.cos(angle)
        sin_a = math.sin(angle)
        return vec2(
            self.x * cos_a - self.y * sin_a,
            self.x * sin_a + self.y * cos_a,
        )

    @classmethod
    def from_angle(cls, angle: float, length: float = 1.0) -> vec2:
        """Create a vector from an angle and length."""
        return cls(math.cos(angle) * length, math.sin(angle) * length)

    def copy(self) -> vec2:
        """Return a copy of this vector."""
        return vec2(self.x, self.y)

    def as_tuple(self) -> tuple[float, float]:
        """Return as a tuple."""
        return (self.x, self.y)

    def as_int_tuple(self) -> tuple[int, int]:
        """Return as an integer tuple (for pixel coordinates)."""
        return (int(self.x), int(self.y))
