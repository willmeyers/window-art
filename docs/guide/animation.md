# Animation

window-art provides a powerful yet simple animation system for smooth motion, fading, resizing, and color transitions.

## Animation Philosophy

Animations in window-art are **immediate-mode** by default. This means animation functions block until the animation completes:

```python
import window_art as wa

with wa.run():
    win = wa.window(100, 100, 100, 100)

    wa.move(win, 500, 100, duration=1.0)  # Blocks for 1 second
    print("Move complete!")               # Runs after animation finishes
```

This makes animations predictable and easy to sequence.

## Movement

### move()

Move a window to an absolute position.

```python
wa.move(win, x, y, duration=0.0, ease="linear")
```

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `win` | Window | required | The window to move |
| `x` | float | required | Target X position |
| `y` | float | required | Target Y position |
| `duration` | float | `0.0` | Animation duration in seconds |
| `ease` | str/func | `"linear"` | Easing function |

```python
# Instant move
wa.move(win, 500, 300)

# Animated move over 1 second
wa.move(win, 500, 300, duration=1.0)

# With easing
wa.move(win, 500, 300, duration=1.0, ease="ease_out_cubic")
```

### move_by()

Move a window by a relative offset.

```python
wa.move_by(win, dx, dy, duration=0.0, ease="linear")
```

```python
# Move 100 pixels right, 50 pixels down
wa.move_by(win, 100, 50, duration=0.5)

# Move left
wa.move_by(win, -200, 0, duration=0.5)
```

### move_all()

Move multiple windows to the same position simultaneously.

```python
wa.move_all(windows, x, y, duration=0.0, ease="linear")
```

```python
windows = [wa.window(100+i*50, 100, 50, 50) for i in range(5)]
wa.move_all(windows, 400, 400, duration=1.0)
```

## Fading

### fade()

Animate window opacity to a target value.

```python
wa.fade(win, opacity, duration=0.0, ease="linear")
```

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `win` | Window | required | The window to fade |
| `opacity` | float | required | Target opacity (0.0 to 1.0) |
| `duration` | float | `0.0` | Animation duration |
| `ease` | str/func | `"linear"` | Easing function |

```python
# Fade to 50% opacity
wa.fade(win, 0.5, duration=1.0)

# Fade to fully transparent
wa.fade(win, 0.0, duration=0.5)
```

### fade_in() / fade_out()

Convenience functions for common fade operations.

```python
wa.fade_in(win, duration=0.5, ease="linear")   # Fade to opacity 1.0
wa.fade_out(win, duration=0.5, ease="linear")  # Fade to opacity 0.0
```

```python
# Create invisible, then fade in
win = wa.window(100, 100, 200, 200, opacity=0)
wa.fade_in(win, duration=1.0)
wa.wait(1)
wa.fade_out(win, duration=1.0)
```

## Resizing

### resize()

Resize a window to target dimensions.

```python
wa.resize(win, w, h, duration=0.0, ease="linear")
```

```python
# Instant resize
wa.resize(win, 400, 300)

# Animated resize
wa.resize(win, 400, 300, duration=0.5, ease="ease_out_quad")
```

### resize_by()

Resize a window by a relative amount.

```python
wa.resize_by(win, dw, dh, duration=0.0, ease="linear")
```

```python
# Grow by 50 pixels in each dimension
wa.resize_by(win, 50, 50, duration=0.5)

# Shrink width by 100
wa.resize_by(win, -100, 0, duration=0.5)
```

## Color Transitions

### color_to()

Animate a smooth color transition.

```python
wa.color_to(win, color, duration=0.0, ease="linear")
```

```python
win = wa.window(100, 100, 200, 200, color="red")
wa.color_to(win, "blue", duration=1.0)
wa.color_to(win, "#00ff00", duration=1.0)
wa.color_to(win, (255, 165, 0), duration=1.0)  # Orange
```

## Timing

### wait()

Pause while continuing to process events.

```python
wa.wait(duration)
```

```python
win = wa.window(100, 100, 200, 200)
wa.wait(2.0)  # Keep visible for 2 seconds
```

!!! note
    `wait()` is not the same as `time.sleep()`. It continues processing SDL events, keeping windows responsive.

### Timing Functions

```python
dt = wa.delta_time()  # Time since last update() call
t = wa.get_time()     # Time since initialization
```

## Combining Animations

### parallel()

Run multiple animations simultaneously.

```python
wa.parallel(*functions)
```

Use `functools.partial` to create animation functions:

```python
from functools import partial

win1 = wa.window(100, 100, 100, 100, color="red")
win2 = wa.window(100, 250, 100, 100, color="blue")

# Both windows move at the same time
wa.parallel(
    partial(wa.move, win1, 500, 100, duration=1.0),
    partial(wa.move, win2, 500, 250, duration=1.0),
)
```

### sequence()

Run animations one after another.

```python
wa.sequence(*functions)
```

```python
from functools import partial

win = wa.window(100, 100, 100, 100, color="coral")

# Move, then resize, then fade
wa.sequence(
    partial(wa.move, win, 400, 100, duration=0.5),
    partial(wa.resize, win, 200, 200, duration=0.5),
    partial(wa.fade, win, 0.5, duration=0.5),
)
```

### Combining parallel and sequence

```python
from functools import partial

# Complex choreography
wa.sequence(
    # First: both windows move in
    partial(wa.parallel,
        partial(wa.move, win1, 300, 200, duration=1.0),
        partial(wa.move, win2, 500, 200, duration=1.0),
    ),
    # Then: both fade out
    partial(wa.parallel,
        partial(wa.fade_out, win1, duration=0.5),
        partial(wa.fade_out, win2, duration=0.5),
    ),
)
```

## Non-Blocking Animations

For advanced control, use the async variants that return generators:

```python
# Get animation generators
anim1 = wa.move_async(win1, 500, 100, duration=1.0)
anim2 = wa.fade_async(win2, 0.5, duration=1.0)

# Combine them
combined = wa.parallel_async(anim1, anim2)

# Run to completion
wa.run_animation(combined)
```

### Available Async Functions

| Function | Description |
|----------|-------------|
| `move_async()` | Non-blocking move |
| `resize_async()` | Non-blocking resize |
| `fade_async()` | Non-blocking fade |
| `color_async()` | Non-blocking color transition |
| `parallel_async()` | Combine animations in parallel |
| `sequence_async()` | Combine animations in sequence |

## Custom Animation Loop

For full control, use the update loop directly:

```python
import window_art as wa

wa.init()
win = wa.window(100, 100, 100, 100)

while wa.update():
    # Custom per-frame logic
    win.x += wa.delta_time() * 100  # Move 100 pixels per second

    if win.x > 500:
        break

wa.quit()
```

## Easing Functions

All animation functions accept an `ease` parameter. See [Easing Functions](easing.md) for the complete list.

```python
# By name
wa.move(win, 500, 100, duration=1.0, ease="ease_out_bounce")

# Or import the function directly
from window_art import ease_out_bounce
wa.move(win, 500, 100, duration=1.0, ease=ease_out_bounce)
```
