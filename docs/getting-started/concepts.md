# Basic Concepts

Understanding these core concepts will help you use window-art effectively.

## The Desktop Singleton

window-art uses a singleton pattern for managing the SDL2 subsystem and all windows. The `Desktop` class handles:

- SDL2 initialization
- Event loop processing
- Window tracking
- Timing and frame management

You rarely interact with it directly. Instead, use the module-level functions:

```python
import window_art as wa

# These all delegate to Desktop.get()
wa.init()           # Initialize SDL2
wa.window(...)      # Create a window
wa.update()         # Process one frame
wa.quit()           # Clean up
```

### Auto-Initialization

The first call to `wa.window()` automatically initializes SDL2 if needed:

```python
import window_art as wa

# No explicit init() needed
win = wa.window(100, 100, 200, 200)  # Auto-initializes
```

### The run() Context Manager

The recommended way to use window-art:

```python
import window_art as wa

with wa.run():
    # SDL2 initialized, windows can be created
    win = wa.window(100, 100, 200, 200)
    wa.wait(1)
# Automatic cleanup when exiting the context
```

## Immediate-Mode Animation

Animation functions like `move()`, `fade()`, and `resize()` are **blocking**. They run to completion before returning:

```python
import window_art as wa

with wa.run():
    win = wa.window(100, 100, 100, 100)

    wa.move(win, 500, 100, duration=1.0)  # Blocks for 1 second
    wa.move(win, 100, 100, duration=1.0)  # Then blocks for another second
    # Total time: 2 seconds
```

This makes animations predictable and easy to reason about.

### Non-Blocking Alternatives

For advanced use cases, `_async` variants return generators:

```python
import window_art as wa

with wa.run():
    win = wa.window(100, 100, 100, 100)

    # Get animation generator
    anim = wa.move_async(win, 500, 100, duration=1.0)

    # Run it manually
    wa.run_animation(anim)
```

## The Update Loop

The `update()` function processes one frame:

1. Handles SDL events (window, keyboard, mouse)
2. Updates animation state
3. Applies pending changes to windows
4. Returns `False` if quit was requested

```python
import window_art as wa

wa.init()
win = wa.window(100, 100, 100, 100)

while wa.update():
    # Custom per-frame logic
    win.x += 1

wa.quit()
```

### Frame Timing

Access timing information via:

```python
wa.delta_time()  # Seconds since last update()
wa.get_time()    # Seconds since init()
```

## Window Properties

Windows have many readable and writable properties:

```python
win = wa.window(100, 100, 200, 200, color="red")

# Position
win.x = 150
win.y = 200
win.position = (150, 200)  # Set both at once

# Size
win.w = 300
win.h = 250
win.size = (300, 250)  # Set both at once

# Appearance
win.color = "blue"
win.opacity = 0.8
win.title = "My Window"

# Behavior
win.borderless = False
win.always_on_top = True
win.resizable = True
win.shadow = False  # macOS only
```

### Dirty Flag Optimization

Property changes are batched internally. When you set `win.x` and `win.y` separately, the actual SDL calls happen together in the next `update()`:

```python
# These don't cause two separate window moves
win.x = 100
win.y = 200
# Both applied in next update()
```

This reduces WindowServer overhead significantly.

## Color System

Colors can be specified in multiple ways:

```python
# CSS named colors (147 supported)
win.color = "coral"
win.color = "dodgerblue"

# Hex codes
win.color = "#ff6347"
win.color = "#f00"      # Short form

# RGB tuples
win.color = (255, 99, 71)

# RGBA tuples
win.color = (255, 99, 71, 128)

# Color objects
from window_art import Color
win.color = Color(255, 99, 71)
```

See [Colors Guide](../guide/colors.md) for the full list of named colors.

## Coordinate System

Coordinates use **screen pixels** with origin at the **top-left** of the primary display:

```
(0, 0) ─────────────────────► X
  │
  │      (x, y)
  │        ┌────────┐
  │        │ Window │
  │        └────────┘
  │
  ▼
  Y
```

Multiple monitors extend this coordinate space. Use `wa.screens()` to query monitor geometry:

```python
for screen in wa.screens():
    print(f"Screen {screen.index}: {screen.w}x{screen.h} at ({screen.x}, {screen.y})")
```

## Window Lifecycle

```python
# Creation
win = wa.window(100, 100, 200, 200)

# Visibility
win.hide()
win.show()

# Z-order
win.raise_window()

# Destruction
win.close()  # Explicit
# or let it be garbage collected
```

All windows are automatically closed when using the `run()` context manager.

## Next Steps

- [Windows Guide](../guide/windows.md) - Full window documentation
- [Animation Guide](../guide/animation.md) - Animation in depth
- [API Reference](../api/core.md) - Complete API documentation
