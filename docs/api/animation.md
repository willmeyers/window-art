# Animation API Reference

Functions for animating windows with movement, fading, resizing, and color transitions.

## Movement

### move()

Move a window to an absolute position.

```python
wa.move(
    win: Window,
    x: float,
    y: float,
    duration: float = 0.0,
    ease: str | EasingFunc = "linear"
) -> None
```

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `win` | Window | required | Window to move |
| `x` | float | required | Target X position |
| `y` | float | required | Target Y position |
| `duration` | float | `0.0` | Animation duration (seconds) |
| `ease` | str/func | `"linear"` | Easing function |

Blocks until animation completes.

---

### move_by()

Move a window by a relative offset.

```python
wa.move_by(
    win: Window,
    dx: float,
    dy: float,
    duration: float = 0.0,
    ease: str | EasingFunc = "linear"
) -> None
```

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `win` | Window | required | Window to move |
| `dx` | float | required | X offset |
| `dy` | float | required | Y offset |
| `duration` | float | `0.0` | Animation duration |
| `ease` | str/func | `"linear"` | Easing function |

---

### move_all()

Move multiple windows to the same position simultaneously.

```python
wa.move_all(
    windows: list[Window],
    x: float,
    y: float,
    duration: float = 0.0,
    ease: str | EasingFunc = "linear"
) -> None
```

---

### move_async()

Non-blocking move that returns an animation generator.

```python
wa.move_async(
    win: Window,
    x: float,
    y: float,
    duration: float,
    ease: str | EasingFunc = "linear"
) -> Animation
```

**Returns:** `Animation` generator.

---

## Fading

### fade()

Animate window opacity to a target value.

```python
wa.fade(
    win: Window,
    opacity: float,
    duration: float = 0.0,
    ease: str | EasingFunc = "linear"
) -> None
```

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `win` | Window | required | Window to fade |
| `opacity` | float | required | Target opacity (0.0-1.0) |
| `duration` | float | `0.0` | Animation duration |
| `ease` | str/func | `"linear"` | Easing function |

---

### fade_in()

Fade a window to full opacity.

```python
wa.fade_in(
    win: Window,
    duration: float = 0.5,
    ease: str | EasingFunc = "linear"
) -> None
```

Equivalent to `fade(win, 1.0, duration, ease)`.

---

### fade_out()

Fade a window to zero opacity.

```python
wa.fade_out(
    win: Window,
    duration: float = 0.5,
    ease: str | EasingFunc = "linear"
) -> None
```

Equivalent to `fade(win, 0.0, duration, ease)`.

---

### fade_async()

Non-blocking fade that returns an animation generator.

```python
wa.fade_async(
    win: Window,
    opacity: float,
    duration: float,
    ease: str | EasingFunc = "linear"
) -> Animation
```

---

## Resizing

### resize()

Resize a window to target dimensions.

```python
wa.resize(
    win: Window,
    w: float,
    h: float,
    duration: float = 0.0,
    ease: str | EasingFunc = "linear"
) -> None
```

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `win` | Window | required | Window to resize |
| `w` | float | required | Target width |
| `h` | float | required | Target height |
| `duration` | float | `0.0` | Animation duration |
| `ease` | str/func | `"linear"` | Easing function |

---

### resize_by()

Resize a window by a relative amount.

```python
wa.resize_by(
    win: Window,
    dw: float,
    dh: float,
    duration: float = 0.0,
    ease: str | EasingFunc = "linear"
) -> None
```

---

### resize_async()

Non-blocking resize that returns an animation generator.

```python
wa.resize_async(
    win: Window,
    w: float,
    h: float,
    duration: float,
    ease: str | EasingFunc = "linear"
) -> Animation
```

---

## Color Transitions

### color_to()

Animate a color transition.

```python
wa.color_to(
    win: Window,
    color: ColorLike,
    duration: float = 0.0,
    ease: str | EasingFunc = "linear"
) -> None
```

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `win` | Window | required | Window to color |
| `color` | ColorLike | required | Target color |
| `duration` | float | `0.0` | Animation duration |
| `ease` | str/func | `"linear"` | Easing function |

---

### color_async()

Non-blocking color transition.

```python
wa.color_async(
    win: Window,
    color: ColorLike,
    duration: float,
    ease: str | EasingFunc = "linear"
) -> Animation
```

---

## Timing

### wait()

Wait while continuing to process events.

```python
wa.wait(duration: float) -> None
```

| Parameter | Type | Description |
|-----------|------|-------------|
| `duration` | float | Wait time in seconds |

!!! warning
    Unlike `time.sleep()`, this processes SDL events to keep windows responsive.

---

## Combining Animations

### parallel()

Run multiple animations simultaneously.

```python
wa.parallel(*funcs: Callable[[], None]) -> None
```

| Parameter | Type | Description |
|-----------|------|-------------|
| `*funcs` | Callable | Animation functions to run in parallel |

Use `functools.partial` to create the callables:

```python
from functools import partial

wa.parallel(
    partial(wa.move, win1, 500, 100, duration=1.0),
    partial(wa.fade, win2, 0.5, duration=1.0),
)
```

---

### sequence()

Run animations one after another.

```python
wa.sequence(*funcs: Callable[[], None]) -> None
```

| Parameter | Type | Description |
|-----------|------|-------------|
| `*funcs` | Callable | Animation functions to run sequentially |

```python
from functools import partial

wa.sequence(
    partial(wa.move, win, 500, 100, duration=0.5),
    partial(wa.resize, win, 200, 200, duration=0.5),
)
```

---

### parallel_async()

Combine animations to run in parallel.

```python
wa.parallel_async(*animations: Animation) -> Animation
```

**Returns:** Combined `Animation` generator.

---

### sequence_async()

Combine animations to run sequentially.

```python
wa.sequence_async(*animations: Animation) -> Animation
```

**Returns:** Combined `Animation` generator.

---

### run_animation()

Run an animation generator to completion.

```python
wa.run_animation(animation: Animation) -> None
```

---

## Types

### Animation

Type alias for animation generators:

```python
Animation = Generator[None, None, None]
```

### EasingFunc

Type alias for easing functions:

```python
EasingFunc = Callable[[float], float]
```

Takes `t` (0.0 to 1.0) and returns modified progress value.
