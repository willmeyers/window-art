# Easing Functions

Easing functions control the acceleration curve of animations, making them feel more natural and dynamic.

## What is Easing?

An easing function takes a progress value `t` (0.0 to 1.0) and returns a modified value. This controls how the animation progresses over time:

- **Linear**: Constant speed (no easing)
- **Ease-in**: Starts slow, accelerates
- **Ease-out**: Starts fast, decelerates
- **Ease-in-out**: Starts slow, speeds up, then slows down

## Using Easing Functions

### By Name

Pass the function name as a string:

```python
wa.move(win, 500, 100, duration=1.0, ease="ease_out_cubic")
wa.fade(win, 0.5, duration=0.5, ease="ease_in_out_quad")
```

### By Function

Import and pass the function directly:

```python
from window_art import ease_out_cubic

wa.move(win, 500, 100, duration=1.0, ease=ease_out_cubic)
```

### Custom Easing

Create your own easing function:

```python
def my_ease(t: float) -> float:
    # Must take t in [0, 1] and return value in approximately [0, 1]
    return t * t * t

wa.move(win, 500, 100, duration=1.0, ease=my_ease)
```

## Available Easing Functions

### Linear

| Name | Description |
|------|-------------|
| `linear` | Constant speed, no easing |

### Quadratic (Power of 2)

| Name | Description |
|------|-------------|
| `ease_in_quad` | Accelerating from zero |
| `ease_out_quad` | Decelerating to zero |
| `ease_in_out_quad` | Accelerate then decelerate |

Aliases: `ease_in`, `ease_out`, `ease_in_out`

### Cubic (Power of 3)

| Name | Description |
|------|-------------|
| `ease_in_cubic` | Stronger acceleration |
| `ease_out_cubic` | Stronger deceleration |
| `ease_in_out_cubic` | Smooth S-curve |

### Quartic (Power of 4)

| Name | Description |
|------|-------------|
| `ease_in_quart` | Even stronger acceleration |
| `ease_out_quart` | Even stronger deceleration |
| `ease_in_out_quart` | Pronounced S-curve |

### Quintic (Power of 5)

| Name | Description |
|------|-------------|
| `ease_in_quint` | Strong acceleration |
| `ease_out_quint` | Strong deceleration |
| `ease_in_out_quint` | Strong S-curve |

### Sine

| Name | Description |
|------|-------------|
| `ease_in_sine` | Gentle sinusoidal acceleration |
| `ease_out_sine` | Gentle sinusoidal deceleration |
| `ease_in_out_sine` | Gentle S-curve |

### Exponential

| Name | Description |
|------|-------------|
| `ease_in_expo` | Exponential acceleration |
| `ease_out_expo` | Exponential deceleration |
| `ease_in_out_expo` | Exponential S-curve |

### Circular

| Name | Description |
|------|-------------|
| `ease_in_circ` | Circular curve acceleration |
| `ease_out_circ` | Circular curve deceleration |
| `ease_in_out_circ` | Circular S-curve |

### Back (Overshoot)

Overshoots the target slightly, then settles.

| Name | Description |
|------|-------------|
| `ease_in_back` | Pulls back before accelerating |
| `ease_out_back` | Overshoots then settles |
| `ease_in_out_back` | Both effects combined |

### Elastic

Spring-like oscillation.

| Name | Description |
|------|-------------|
| `ease_in_elastic` | Elastic wind-up |
| `ease_out_elastic` | Elastic snap and wobble |
| `ease_in_out_elastic` | Both effects combined |

### Bounce

Ball-bouncing effect.

| Name | Description |
|------|-------------|
| `ease_in_bounce` | Reverse bounce at start |
| `ease_out_bounce` | Bounces at the end |
| `ease_in_out_bounce` | Both effects combined |

## Visual Reference

Here's how each easing family looks:

```
Linear:        ────────────────  (constant slope)

Ease-in:       ___________╱      (slow start)

Ease-out:      ╱───────────      (slow end)

Ease-in-out:   ____╱────────     (slow start and end)

Bounce:        ╱╲╱╲╱─────────    (bouncing effect)

Elastic:       ⌇⌇╱───────────    (spring oscillation)

Back:          ╲_╱───────────    (overshoot)
```

## Choosing an Easing Function

### For UI Elements

- **Appearing**: `ease_out_cubic` or `ease_out_quad`
- **Disappearing**: `ease_in_cubic` or `ease_in_quad`
- **Moving**: `ease_in_out_cubic`

### For Playful Effects

- **Bouncy**: `ease_out_bounce`
- **Springy**: `ease_out_elastic`
- **Snappy**: `ease_out_back`

### For Subtle Motion

- **Gentle**: `ease_in_out_sine`
- **Smooth**: `ease_in_out_quad`

### For Dramatic Effect

- **Explosive**: `ease_out_expo`
- **Powerful**: `ease_out_quint`

## Example: Comparing Easing Functions

```python
import window_art as wa

easings = [
    "linear",
    "ease_out_quad",
    "ease_out_cubic",
    "ease_out_bounce",
    "ease_out_elastic",
]

with wa.run():
    windows = []
    for i, ease_name in enumerate(easings):
        win = wa.window(100, 100 + i * 60, 50, 50, color="coral")
        windows.append((win, ease_name))

    wa.wait(0.5)

    # Move each window with different easing
    for win, ease_name in windows:
        wa.move(win, 600, win.y, duration=1.5, ease=ease_name)

    wa.wait(1)
```

## Programmatic Access

### Get Easing by Name

```python
from window_art import get_easing

ease_func = get_easing("ease_out_bounce")
value = ease_func(0.5)  # Get value at t=0.5
```

### List All Easing Functions

```python
from window_art.easing import EASING_FUNCTIONS

for name in EASING_FUNCTIONS:
    print(name)
```

## Mathematical Formulas

For reference, here are the formulas for the basic easing families:

### Quadratic

```python
def ease_in_quad(t):
    return t * t

def ease_out_quad(t):
    return 1 - (1 - t) * (1 - t)

def ease_in_out_quad(t):
    if t < 0.5:
        return 2 * t * t
    return 1 - (-2 * t + 2) ** 2 / 2
```

### Cubic

```python
def ease_in_cubic(t):
    return t * t * t

def ease_out_cubic(t):
    return 1 - (1 - t) ** 3

def ease_in_out_cubic(t):
    if t < 0.5:
        return 4 * t * t * t
    return 1 - (-2 * t + 2) ** 3 / 2
```
