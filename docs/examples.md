# Examples

Learn by example with these working code samples.

## Basic Window

Create a simple colored window:

```python
import window_art as wa

with wa.run():
    win = wa.window(100, 100, 200, 200, color="coral")
    wa.wait(3)
```

## Animation Showcase

Demonstrate different easing functions:

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

    # Animate each with different easing
    for win, ease_name in windows:
        wa.move(win, 600, win.y, duration=1.5, ease=ease_name)

    wa.wait(1)
```

## DVD Bounce

Classic bouncing logo effect with multiple windows:

```python
import window_art as wa
from window_art import vec2
import random

NUM_WINDOWS = 20
COLORS = ["red", "orange", "yellow", "green", "cyan", "blue", "purple", "pink"]

with wa.run():
    # Create windows with random positions and velocities
    items = []
    for i in range(NUM_WINDOWS):
        x = random.randint(100, 800)
        y = random.randint(100, 600)
        color = COLORS[i % len(COLORS)]
        win = wa.window(x, y, 80, 60, color=color)

        vx = random.uniform(-200, 200)
        vy = random.uniform(-200, 200)
        items.append({"win": win, "vel": vec2(vx, vy)})

    # Animate
    while wa.update():
        dt = wa.delta_time()

        for item in items:
            win = item["win"]
            vel = item["vel"]

            # Update position
            win.x += vel.x * dt
            win.y += vel.y * dt

            # Bounce off edges
            if win.x < 0 or win.x + win.w > 1200:
                vel.x *= -1
                # Change color on bounce
                win.color = random.choice(COLORS)
            if win.y < 0 or win.y + win.h > 800:
                vel.y *= -1
                win.color = random.choice(COLORS)
```

## Color Cycling

Smoothly cycle through colors:

```python
import window_art as wa
from window_art import Color

COLORS = [
    Color.parse("red"),
    Color.parse("orange"),
    Color.parse("yellow"),
    Color.parse("green"),
    Color.parse("blue"),
    Color.parse("purple"),
]

with wa.run():
    win = wa.window(300, 200, 200, 200)

    for i in range(len(COLORS) * 2):  # Cycle twice
        current = COLORS[i % len(COLORS)]
        next_color = COLORS[(i + 1) % len(COLORS)]

        # Animate through intermediate colors
        for t in range(20):
            win.color = current.lerp(next_color, t / 20)
            wa.wait(0.05)
```

## Parallel Animations

Run multiple animations simultaneously:

```python
import window_art as wa
from functools import partial

with wa.run():
    win1 = wa.window(100, 100, 100, 100, color="red")
    win2 = wa.window(100, 300, 100, 100, color="blue")
    win3 = wa.window(100, 500, 100, 100, color="green")

    # All three move at the same time
    wa.parallel(
        partial(wa.move, win1, 600, 100, duration=1.5, ease="ease_out_cubic"),
        partial(wa.move, win2, 600, 300, duration=1.5, ease="ease_out_bounce"),
        partial(wa.move, win3, 600, 500, duration=1.5, ease="ease_out_elastic"),
    )

    wa.wait(1)

    # All three fade out
    wa.parallel(
        partial(wa.fade_out, win1, duration=0.5),
        partial(wa.fade_out, win2, duration=0.5),
        partial(wa.fade_out, win3, duration=0.5),
    )
```

## Sequential Animations

Chain animations one after another:

```python
import window_art as wa
from functools import partial

with wa.run():
    win = wa.window(100, 300, 100, 100, color="coral")

    wa.sequence(
        partial(wa.move, win, 500, 300, duration=0.5, ease="ease_out_cubic"),
        partial(wa.resize, win, 200, 200, duration=0.3, ease="ease_out_quad"),
        partial(wa.color_to, win, "dodgerblue", duration=0.3),
        partial(wa.fade, win, 0.5, duration=0.3),
        partial(wa.move, win, 300, 200, duration=0.5, ease="ease_in_out_cubic"),
        partial(wa.fade_in, win, duration=0.3),
    )

    wa.wait(1)
```

## Grid Layout

Create a grid of colored cells:

```python
import window_art as wa

with wa.run():
    grid = wa.grid(50, 50, 600, 400,
        columns="1fr 1fr 1fr",
        rows="1fr 1fr",
        gap=10
    )

    colors = ["coral", "dodgerblue", "limegreen", "gold", "hotpink", "turquoise"]
    grid.fill(colors)

    wa.wait(2)

    # Animate grid resize
    grid.animate_to(100, 100, 400, 300, duration=1.0)

    wa.wait(2)
```

## Image Display

Show an image in a window:

```python
import window_art as wa

with wa.run():
    win = wa.window(100, 100, 600, 400, image="photo.jpg")
    wa.wait(3)

    # Pan across the image
    win.image_region = (0, 0, 300, 200)
    wa.wait(1)

    win.image_region = (300, 200, 300, 200)
    wa.wait(1)

    # Show full image
    win.image_region = None
    wa.wait(1)
```

## GIF Animation

Play an animated GIF:

```python
import window_art as wa

with wa.run():
    win = wa.window(100, 100, 400, 300, gif="animation.gif")

    # Play for 3 seconds
    wa.wait(3)

    # Slow motion
    win.gif_speed = 0.5
    wa.wait(3)

    # Fast forward
    win.gif_speed = 3.0
    wa.wait(2)

    # Pause and step through frames
    win.gif_playing = False
    for i in range(win.gif_frame_count):
        win.gif_frame = i
        wa.wait(0.2)
```

## Multi-Monitor

Create windows on different screens:

```python
import window_art as wa

with wa.run():
    screens = wa.screens()

    for i, screen in enumerate(screens):
        # Center a window on each screen
        cx, cy = screen.center
        win = wa.window(
            cx - 100, cy - 100, 200, 200,
            color=["coral", "dodgerblue", "limegreen"][i % 3]
        )

    wa.wait(5)
```

## Staggered Animation

Animate windows with delays:

```python
import window_art as wa

with wa.run():
    windows = []
    for i in range(10):
        win = wa.window(100, 50 + i * 70, 50, 50, color="coral", opacity=0)
        windows.append(win)

    # Staggered fade in
    for i, win in enumerate(windows):
        wa.wait(0.1)  # Delay between each
        wa.fade_in(win, duration=0.3)

    wa.wait(1)

    # Staggered move
    for i, win in enumerate(windows):
        wa.move(win, 600, win.y, duration=0.5, ease="ease_out_cubic")
        # No wait - next one starts immediately
```

## Circular Motion

Move windows in a circle:

```python
import window_art as wa
from window_art import vec2
import math

with wa.run():
    center = vec2(400, 300)
    radius = 150
    num_windows = 8

    windows = []
    for i in range(num_windows):
        angle = (i / num_windows) * math.pi * 2
        pos = center + vec2.from_angle(angle, radius)
        win = wa.window(pos.x - 25, pos.y - 25, 50, 50, color="coral")
        windows.append((win, angle))

    # Rotate
    start_time = wa.get_time()
    while wa.update():
        elapsed = wa.get_time() - start_time
        if elapsed > 5:  # Run for 5 seconds
            break

        for win, base_angle in windows:
            angle = base_angle + elapsed * 2  # 2 radians per second
            pos = center + vec2.from_angle(angle, radius)
            win.position = (pos.x - 25, pos.y - 25)
```

## Window Following Mouse

A window that follows cursor movement (requires reading mouse position):

```python
import window_art as wa

# Note: This example requires additional SDL2 bindings for mouse input
# This is a simplified version using manual position updates

with wa.run():
    follower = wa.window(400, 300, 50, 50, color="coral")

    # Simulate mouse movement with animation
    positions = [(200, 200), (600, 200), (600, 500), (200, 500), (400, 350)]

    for x, y in positions:
        wa.move(follower, x - 25, y - 25, duration=0.5, ease="ease_out_cubic")

    wa.wait(1)
```

## More Examples

The `examples/` directory in the repository contains additional examples:

Clone the repository to run these examples:

```bash
git clone https://github.com/willmeyers/window-art.git
cd window-art
pip install -e .
```
