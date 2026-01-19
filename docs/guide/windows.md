# Creating Windows

This guide covers everything about creating and manipulating windows.

## Creating a Window

```python
import window_art as wa

win = wa.window(x, y, w, h, **options)
```

### Required Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `x` | float | X position (screen pixels from left) |
| `y` | float | Y position (screen pixels from top) |
| `w` | float | Width in pixels |
| `h` | float | Height in pixels |

### Optional Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `color` | ColorLike | `"white"` | Background color |
| `opacity` | float | `1.0` | Opacity (0.0 to 1.0) |
| `borderless` | bool | `True` | Remove window decorations |
| `always_on_top` | bool | `True` | Keep above other windows |
| `resizable` | bool | `False` | Allow user resizing |
| `title` | str | `""` | Window title bar text |
| `shadow` | bool | `True` | Show drop shadow (macOS) |
| `image` | str | `None` | Path to image file |
| `gif` | str | `None` | Path to GIF file |
| `video` | str | `None` | Path to video file |

### Example

```python
import window_art as wa

with wa.run():
    # Simple colored window
    win1 = wa.window(100, 100, 200, 200, color="coral")

    # Window with border and title
    win2 = wa.window(350, 100, 200, 200,
        color="dodgerblue",
        borderless=False,
        title="Hello World"
    )

    # Semi-transparent window
    win3 = wa.window(600, 100, 200, 200,
        color="green",
        opacity=0.7
    )

    wa.wait(3)
```

## Position Properties

### Reading Position

```python
x = win.x          # X coordinate
y = win.y          # Y coordinate
pos = win.position # (x, y) tuple
```

### Setting Position

```python
# Individual coordinates
win.x = 200
win.y = 300

# Both at once (more efficient)
win.position = (200, 300)
```

### Animated Movement

```python
# Move to absolute position
wa.move(win, 500, 300, duration=1.0)

# Move by relative offset
wa.move_by(win, 100, -50, duration=0.5)
```

## Size Properties

### Reading Size

```python
w = win.w          # Width
h = win.h          # Height
w = win.width      # Alias for w
h = win.height     # Alias for h
size = win.size    # (w, h) tuple
```

### Setting Size

```python
# Individual dimensions
win.w = 300
win.h = 200

# Both at once
win.size = (300, 200)
```

### Animated Resizing

```python
# Resize to absolute size
wa.resize(win, 400, 300, duration=1.0)

# Resize by relative amount
wa.resize_by(win, 50, 50, duration=0.5)
```

## Appearance

### Color

See [Colors Guide](colors.md) for full details.

```python
# Set color (many formats supported)
win.color = "coral"
win.color = "#ff6347"
win.color = (255, 99, 71)

# Animated color change
wa.color_to(win, "blue", duration=1.0)
```

### Opacity

```python
# Set opacity (0.0 = transparent, 1.0 = opaque)
win.opacity = 0.5

# Animated opacity change
wa.fade(win, 0.3, duration=1.0)
wa.fade_in(win, duration=0.5)   # Fade to 1.0
wa.fade_out(win, duration=0.5)  # Fade to 0.0
```

### Window Decorations

```python
# Toggle border
win.borderless = False  # Show title bar and borders
win.borderless = True   # Hide decorations

# Window title (visible when borderless=False)
win.title = "My Application"
```

### Shadow (macOS)

```python
# Control drop shadow
win.shadow = True   # Enable shadow
win.shadow = False  # Disable shadow
```

## Z-Order and Visibility

### Always on Top

```python
win.always_on_top = True   # Keep above other windows
win.always_on_top = False  # Normal z-order
```

### Raise to Front

```python
win.raise_window()  # Bring to front of z-order
```

### Show/Hide

```python
win.hide()  # Make invisible
win.show()  # Make visible again
```

## Window Lifecycle

### Checking State

```python
if not win.closed:
    # Window is still active
    win.x += 10
```

### Closing Windows

```python
# Explicit close
win.close()

# Clear all windows
wa.clear()
```

Windows are also closed automatically:

- When the `run()` context exits
- When garbage collected (no references)
- When `wa.quit()` is called

## Multiple Windows

### Listing Windows

```python
# Get all active windows
for win in wa.windows():
    print(f"Window at ({win.x}, {win.y})")
```

### Moving Multiple Windows

```python
windows = [
    wa.window(100 + i*150, 100, 100, 100, color=c)
    for i, c in enumerate(["red", "green", "blue"])
]

# Move all to the same position
wa.move_all(windows, 400, 400, duration=1.0)
```

## Screen Information

### Query Displays

```python
# Get all screens
for screen in wa.screens():
    print(f"Screen {screen.index}: {screen.w}x{screen.h}")
    print(f"  Position: ({screen.x}, {screen.y})")
    print(f"  Center: {screen.center}")

# Get primary screen
primary = wa.primary_screen()
if primary:
    # Center a window on the primary screen
    cx, cy = primary.center
    win = wa.window(cx - 100, cy - 100, 200, 200)
```

### Screen Properties

| Property | Type | Description |
|----------|------|-------------|
| `x` | int | X position of screen origin |
| `y` | int | Y position of screen origin |
| `w` / `width` | int | Screen width |
| `h` / `height` | int | Screen height |
| `index` | int | Display index |
| `center` | (int, int) | Center coordinate |

