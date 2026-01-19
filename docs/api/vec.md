# Vector Math API Reference

2D vector mathematics for position and motion calculations.

## vec2 Class

```python
from window_art import vec2
```

### Constructor

```python
vec2(x: float = 0.0, y: float = 0.0)
```

```python
v = vec2()          # (0, 0)
v = vec2(3, 4)      # (3, 4)
v = vec2(x=1, y=2)  # (1, 2)
```

---

### Properties

| Property | Type | Description |
|----------|------|-------------|
| `x` | float | X component |
| `y` | float | Y component |
| `length` | float | Magnitude (read-only) |
| `length_squared` | float | Magnitude squared (read-only, faster) |

```python
v = vec2(3, 4)
print(v.x)              # 3.0
print(v.y)              # 4.0
print(v.length)         # 5.0
print(v.length_squared) # 25.0
```

---

### Arithmetic Operators

```python
a = vec2(1, 2)
b = vec2(3, 4)

# Addition
c = a + b        # vec2(4, 6)

# Subtraction
c = a - b        # vec2(-2, -2)

# Scalar multiplication
c = a * 2        # vec2(2, 4)
c = 2 * a        # vec2(2, 4)

# Scalar division
c = a / 2        # vec2(0.5, 1)

# Negation
c = -a           # vec2(-1, -2)
```

---

### Iteration and Indexing

```python
v = vec2(3, 4)

# Unpack
x, y = v

# Index
print(v[0])  # 3.0
print(v[1])  # 4.0

# Iterate
for component in v:
    print(component)
```

---

### Methods

#### normalized()

Return a unit vector in the same direction.

```python
v.normalized() -> vec2
```

```python
v = vec2(3, 4)
n = v.normalized()  # vec2(0.6, 0.8)
print(n.length)     # 1.0
```

---

#### dot()

Compute the dot product with another vector.

```python
v.dot(other: vec2) -> float
```

```python
a = vec2(1, 0)
b = vec2(0, 1)
print(a.dot(b))  # 0.0 (perpendicular)

c = vec2(1, 0)
print(a.dot(c))  # 1.0 (parallel)
```

---

#### distance_to()

Compute the distance to another vector.

```python
v.distance_to(other: vec2) -> float
```

```python
a = vec2(0, 0)
b = vec2(3, 4)
print(a.distance_to(b))  # 5.0
```

---

#### lerp()

Linearly interpolate towards another vector.

```python
v.lerp(other: vec2, t: float) -> vec2
```

| Parameter | Type | Description |
|-----------|------|-------------|
| `other` | vec2 | Target vector |
| `t` | float | Interpolation factor (0.0-1.0) |

```python
a = vec2(0, 0)
b = vec2(10, 10)
mid = a.lerp(b, 0.5)  # vec2(5, 5)
```

---

#### angle()

Get the angle of this vector in radians.

```python
v.angle() -> float
```

Returns angle from positive X-axis, in range [-pi, pi].

```python
import math
v = vec2(1, 0)
print(v.angle())  # 0.0

v = vec2(0, 1)
print(v.angle())  # 1.5707... (pi/2)
```

---

#### rotated()

Rotate the vector by an angle.

```python
v.rotated(angle: float) -> vec2
```

| Parameter | Type | Description |
|-----------|------|-------------|
| `angle` | float | Rotation angle in radians |

```python
import math
v = vec2(1, 0)
rotated = v.rotated(math.pi / 2)  # vec2(0, 1)
```

---

#### copy()

Create a copy of the vector.

```python
v.copy() -> vec2
```

---

#### as_tuple()

Convert to a tuple of floats.

```python
v.as_tuple() -> tuple[float, float]
```

```python
v = vec2(3.5, 4.5)
t = v.as_tuple()  # (3.5, 4.5)
```

---

#### as_int_tuple()

Convert to a tuple of integers.

```python
v.as_int_tuple() -> tuple[int, int]
```

```python
v = vec2(3.7, 4.2)
t = v.as_int_tuple()  # (3, 4)
```

---

### Class Methods

#### from_angle()

Create a vector from an angle.

```python
vec2.from_angle(angle: float, length: float = 1.0) -> vec2
```

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `angle` | float | required | Angle in radians |
| `length` | float | `1.0` | Vector magnitude |

```python
import math

# Unit vector pointing right
v = vec2.from_angle(0)  # vec2(1, 0)

# Unit vector pointing up
v = vec2.from_angle(math.pi / 2)  # vec2(0, 1)

# Vector of length 5 at 45 degrees
v = vec2.from_angle(math.pi / 4, 5)
```

---

## Example: Circular Motion

```python
import desktop_windows as dw
from window_art import vec2
import math

with wa.run():
    win = wa.window(400, 300, 50, 50, color="coral")

    center = vec2(400, 300)
    radius = 150
    angle = 0

    while wa.update():
        angle += wa.delta_time() * 2  # 2 radians per second

        # Calculate position on circle
        offset = vec2.from_angle(angle, radius)
        pos = center + offset

        win.position = pos.as_int_tuple()

        if angle > math.pi * 4:  # Two full rotations
            break
```

## Example: Smooth Following

```python
import desktop_windows as dw
from window_art import vec2

with wa.run():
    target = wa.window(500, 300, 30, 30, color="red")
    follower = wa.window(100, 300, 50, 50, color="blue")

    while wa.update():
        # Move target
        target.x += wa.delta_time() * 50

        # Follower smoothly follows target
        target_pos = vec2(target.x, target.y)
        follower_pos = vec2(follower.x, follower.y)

        # Lerp towards target (smooth following)
        new_pos = follower_pos.lerp(target_pos, wa.delta_time() * 3)
        follower.position = new_pos.as_int_tuple()

        if target.x > 800:
            break
```
