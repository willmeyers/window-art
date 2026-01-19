# Quick Start

This guide walks you through creating your first animated desktop windows.

## Your First Window

```python
import window_art as wa

with wa.run():
    # Create a 200x200 coral-colored window at position (100, 100)
    win = wa.window(100, 100, 200, 200, color="coral")
    wa.wait(2)  # Keep it visible for 2 seconds
```

The `run()` context manager handles initialization and cleanup automatically.

## Moving Windows

```python
import window_art as wa

with wa.run():
    win = wa.window(100, 100, 200, 200, color="dodgerblue")

    # Move to position (500, 300) over 1 second
    wa.move(win, 500, 300, duration=1.0)

    # Move by an offset (relative motion)
    wa.move_by(win, -200, 100, duration=0.5)

    wa.wait(1)
```

## Animation with Easing

Easing functions control the acceleration curve of animations:

```python
import window_art as wa

with wa.run():
    win = wa.window(100, 100, 200, 200, color="purple")

    # Smooth deceleration
    wa.move(win, 500, 100, duration=1.0, ease="ease_out_cubic")

    # Bouncy effect
    wa.move(win, 100, 100, duration=1.0, ease="ease_out_bounce")

    # Elastic overshoot
    wa.move(win, 500, 100, duration=1.0, ease="ease_out_elastic")

    wa.wait(1)
```

See the full list in [Easing Functions](../guide/easing.md).

## Fading and Opacity

```python
import window_art as wa

with wa.run():
    win = wa.window(100, 100, 200, 200, color="red")

    # Fade to 50% opacity
    wa.fade(win, 0.5, duration=0.5)

    # Fade out completely
    wa.fade_out(win, duration=0.5)

    # Fade back in
    wa.fade_in(win, duration=0.5)

    wa.wait(1)
```

## Resizing

```python
import window_art as wa

with wa.run():
    win = wa.window(100, 100, 100, 100, color="green")

    # Resize to 300x200
    wa.resize(win, 300, 200, duration=0.5)

    # Grow by 50 pixels in each dimension
    wa.resize_by(win, 50, 50, duration=0.5)

    wa.wait(1)
```

## Changing Colors

```python
import window_art as wa

with wa.run():
    win = wa.window(100, 100, 200, 200, color="blue")

    # Instant color change
    win.color = "red"
    wa.wait(0.5)

    # Animated color transition
    wa.color_to(win, "yellow", duration=1.0)

    wa.wait(1)
```

## Multiple Windows

```python
import window_art as wa

with wa.run():
    # Create multiple windows
    colors = ["red", "orange", "yellow", "green", "blue"]
    windows = []

    for i, color in enumerate(colors):
        win = wa.window(100 + i * 150, 100, 100, 100, color=color)
        windows.append(win)

    wa.wait(1)

    # Animate all at once
    wa.move_all(windows, 400, 400, duration=1.0)

    wa.wait(1)
```

## Parallel Animations

Run multiple animations simultaneously:

```python
import window_art as wa
from functools import partial

with wa.run():
    win1 = wa.window(100, 100, 100, 100, color="red")
    win2 = wa.window(100, 250, 100, 100, color="blue")

    # Run both moves at the same time
    wa.parallel(
        partial(wa.move, win1, 500, 100, duration=1.0),
        partial(wa.move, win2, 500, 250, duration=1.0),
    )

    wa.wait(1)
```

## Sequential Animations

Chain animations one after another:

```python
import window_art as wa
from functools import partial

with wa.run():
    win = wa.window(100, 100, 100, 100, color="coral")

    # Run in sequence: move, then resize, then fade
    wa.sequence(
        partial(wa.move, win, 400, 100, duration=0.5),
        partial(wa.resize, win, 200, 200, duration=0.5),
        partial(wa.fade, win, 0.5, duration=0.5),
    )

    wa.wait(1)
```

## Next Steps

- [Basic Concepts](concepts.md) - Understand the architecture
- [Animation Guide](../guide/animation.md) - Deep dive into animations
- [Grid Layout](../guide/grid.md) - Create complex layouts
- [Examples](../examples.md) - See more complete examples
