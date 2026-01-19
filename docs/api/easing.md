# Easing API Reference

Easing functions for animation timing curves.

## Usage

### By Name

Pass as a string to animation functions:

```python
wa.move(win, 500, 100, duration=1.0, ease="ease_out_cubic")
```

### By Function

Import and pass directly:

```python
from window_art import ease_out_cubic

wa.move(win, 500, 100, duration=1.0, ease=ease_out_cubic)
```

### Get by Name

```python
from window_art import get_easing

ease_func = get_easing("ease_out_bounce")
```

---

## Function Signature

All easing functions have the same signature:

```python
def easing_func(t: float) -> float:
    """
    Args:
        t: Progress value from 0.0 to 1.0

    Returns:
        Eased value (typically 0.0 to 1.0, may exceed for elastic/back)
    """
```

---

## Available Functions

### Linear

| Function | Description |
|----------|-------------|
| `linear` | No easing, constant speed |

---

### Quadratic

| Function | Alias | Description |
|----------|-------|-------------|
| `ease_in_quad` | `ease_in` | Accelerating from zero |
| `ease_out_quad` | `ease_out` | Decelerating to zero |
| `ease_in_out_quad` | `ease_in_out` | Accelerate then decelerate |

---

### Cubic

| Function | Description |
|----------|-------------|
| `ease_in_cubic` | Stronger acceleration |
| `ease_out_cubic` | Stronger deceleration |
| `ease_in_out_cubic` | Smooth S-curve |

---

### Quartic

| Function | Description |
|----------|-------------|
| `ease_in_quart` | Even stronger acceleration |
| `ease_out_quart` | Even stronger deceleration |
| `ease_in_out_quart` | Pronounced S-curve |

---

### Quintic

| Function | Description |
|----------|-------------|
| `ease_in_quint` | Very strong acceleration |
| `ease_out_quint` | Very strong deceleration |
| `ease_in_out_quint` | Strong S-curve |

---

### Sine

| Function | Description |
|----------|-------------|
| `ease_in_sine` | Gentle sinusoidal acceleration |
| `ease_out_sine` | Gentle sinusoidal deceleration |
| `ease_in_out_sine` | Gentle S-curve |

---

### Exponential

| Function | Description |
|----------|-------------|
| `ease_in_expo` | Exponential acceleration |
| `ease_out_expo` | Exponential deceleration |
| `ease_in_out_expo` | Exponential S-curve |

---

### Circular

| Function | Description |
|----------|-------------|
| `ease_in_circ` | Circular curve acceleration |
| `ease_out_circ` | Circular curve deceleration |
| `ease_in_out_circ` | Circular S-curve |

---

### Back (Overshoot)

| Function | Description |
|----------|-------------|
| `ease_in_back` | Pulls back before accelerating |
| `ease_out_back` | Overshoots then settles |
| `ease_in_out_back` | Both effects combined |

!!! note
    Back easing can return values outside 0.0-1.0 range.

---

### Elastic

| Function | Description |
|----------|-------------|
| `ease_in_elastic` | Elastic wind-up |
| `ease_out_elastic` | Elastic snap and wobble |
| `ease_in_out_elastic` | Both effects combined |

!!! note
    Elastic easing can return values outside 0.0-1.0 range.

---

### Bounce

| Function | Description |
|----------|-------------|
| `ease_in_bounce` | Reverse bounce at start |
| `ease_out_bounce` | Bounces at the end |
| `ease_in_out_bounce` | Both effects combined |

---

## Lookup Table

```python
from window_art.easing import EASING_FUNCTIONS

# Dictionary mapping names to functions
for name, func in EASING_FUNCTIONS.items():
    print(name)
```

---

## get_easing()

Get an easing function by name or pass through a function.

```python
from window_art import get_easing

get_easing(name: str | EasingFunc) -> EasingFunc
```

| Input | Return |
|-------|--------|
| `str` | Corresponding function from lookup table |
| `EasingFunc` | Input unchanged |

Raises `ValueError` if string name is not recognized.

---

## Type Alias

```python
EasingFunc = Callable[[float], float]
```

---

## Custom Easing

Create your own easing function:

```python
def my_ease(t: float) -> float:
    # Custom curve
    return t * t * t

wa.move(win, 500, 100, duration=1.0, ease=my_ease)
```

Requirements:
- Take single float argument `t` in range [0, 1]
- Return float (typically in range [0, 1], may exceed for special effects)
- `my_ease(0)` should return approximately 0
- `my_ease(1)` should return approximately 1

---

## Example

```python
import window_art as wa
from window_art import ease_out_bounce, get_easing

with wa.run():
    win = wa.window(100, 100, 100, 100, color="coral")

    # By name
    wa.move(win, 500, 100, duration=1.0, ease="ease_out_cubic")

    # By function
    wa.move(win, 100, 100, duration=1.0, ease=ease_out_bounce)

    # Via get_easing
    ease = get_easing("ease_out_elastic")
    wa.move(win, 500, 100, duration=1.0, ease=ease)

    # Custom
    def slow_start(t):
        return t ** 4

    wa.move(win, 100, 100, duration=1.0, ease=slow_start)

    wa.wait(1)
```
