# Window API Reference

The `Window` class represents a desktop window managed by SDL2.

## Creating Windows

Windows are created via `wa.window()`:

```python
win = wa.window(x, y, w, h, **kwargs)
```

See [Core API](core.md#window) for full constructor documentation.

## Position Properties

### x

The window's X coordinate.

```python
win.x -> float
win.x = value
```

### y

The window's Y coordinate.

```python
win.y -> float
win.y = value
```

### position

The window's (x, y) position as a tuple.

```python
win.position -> tuple[float, float]
win.position = (x, y)
```

Setting `position` is more efficient than setting `x` and `y` separately.

---

## Size Properties

### w

The window's width.

```python
win.w -> float
win.w = value
```

### h

The window's height.

```python
win.h -> float
win.h = value
```

### width

Alias for `w`.

```python
win.width -> float
win.width = value
```

### height

Alias for `h`.

```python
win.height -> float
win.height = value
```

### size

The window's (width, height) as a tuple.

```python
win.size -> tuple[float, float]
win.size = (w, h)
```

---

## Appearance Properties

### color

The window's background color.

```python
win.color -> Color
win.color = value  # ColorLike: str, tuple, or Color
```

Accepts CSS color names, hex codes, RGB tuples, or `Color` objects.

### opacity

The window's opacity (0.0 = transparent, 1.0 = opaque).

```python
win.opacity -> float
win.opacity = value  # 0.0 to 1.0
```

### title

The window's title bar text.

```python
win.title -> str
win.title = value
```

Only visible when `borderless=False`.

---

## Behavior Properties

### borderless

Whether the window has decorations (title bar, borders).

```python
win.borderless -> bool
win.borderless = value
```

### always_on_top

Whether the window stays above other windows.

```python
win.always_on_top -> bool
win.always_on_top = value
```

### resizable

Whether the user can resize the window.

```python
win.resizable -> bool
win.resizable = value
```

### shadow

Whether the window has a drop shadow (macOS only).

```python
win.shadow -> bool
win.shadow = value
```

---

## Image Properties

### image

Path to the displayed image file.

```python
win.image -> str | None
win.image = path  # str or None to clear
```

### image_region

Source region to display from the image.

```python
win.image_region -> tuple[int, int, int, int] | None  # (x, y, w, h)
win.image_region = (x, y, w, h)  # or None for full image
```

### image_size

Dimensions of the loaded image.

```python
win.image_size -> tuple[int, int]  # (width, height)
```

Read-only.

---

## GIF Properties

### gif

Path to the displayed GIF file.

```python
win.gif -> str | None
win.gif = path  # str or None to clear
```

### gif_playing

Whether the GIF animation is playing.

```python
win.gif_playing -> bool
win.gif_playing = value
```

### gif_loop

Whether the GIF loops continuously.

```python
win.gif_loop -> bool
win.gif_loop = value
```

### gif_speed

Playback speed multiplier.

```python
win.gif_speed -> float
win.gif_speed = value  # 1.0 = normal, 2.0 = double speed
```

### gif_frame

Current frame index.

```python
win.gif_frame -> int
win.gif_frame = value  # Jump to frame
```

### gif_frame_count

Total number of frames.

```python
win.gif_frame_count -> int
```

Read-only.

### gif_region

Source region to display from each frame.

```python
win.gif_region -> tuple[int, int, int, int] | None
win.gif_region = (x, y, w, h)
```

### gif_size

Dimensions of the GIF.

```python
win.gif_size -> tuple[int, int]  # (width, height)
```

Read-only.

---

## Video Properties

### video

Path to the displayed video file.

```python
win.video -> str | None
win.video = path  # str or None to clear
```

### video_playing

Whether video playback is active.

```python
win.video_playing -> bool
win.video_playing = value
```

### video_loop

Whether video loops continuously.

```python
win.video_loop -> bool
win.video_loop = value
```

### video_speed

Playback speed multiplier.

```python
win.video_speed -> float
win.video_speed = value
```

### video_position

Current playback position in seconds.

```python
win.video_position -> float
win.video_position = value  # Seek to time
```

### video_duration

Total video duration in seconds.

```python
win.video_duration -> float
```

Read-only.

### video_frame

Current frame index.

```python
win.video_frame -> int
```

Read-only.

### video_region

Source region to display.

```python
win.video_region -> tuple[int, int, int, int] | None
win.video_region = (x, y, w, h)
```

### video_size

Dimensions of the video.

```python
win.video_size -> tuple[int, int]  # (width, height)
```

Read-only.

---

## State Properties

### closed

Whether the window has been closed.

```python
win.closed -> bool
```

Read-only.

### id

Unique window identifier.

```python
win.id -> int
```

Read-only.

---

## Methods

### close()

Close and destroy the window.

```python
win.close() -> None
```

### show()

Make the window visible.

```python
win.show() -> None
```

### hide()

Make the window invisible.

```python
win.hide() -> None
```

### raise_window()

Bring the window to the front of the z-order.

```python
win.raise_window() -> None
```

---

## Example

```python
import window_art as wa

with wa.run():
    # Create window
    win = wa.window(100, 100, 200, 200, color="coral")

    # Modify properties
    win.position = (300, 200)
    win.size = (300, 250)
    win.color = "dodgerblue"
    win.opacity = 0.8
    win.title = "Hello"
    win.borderless = False

    wa.wait(2)

    # Check state
    if not win.closed:
        win.close()
```
