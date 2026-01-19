# Core API Reference

Core functions for managing the window-art lifecycle, creating windows, and controlling the event loop.

## Lifecycle Functions

### init()

Initialize the SDL2 subsystem. Called automatically when creating the first window.

```python
wa.init() -> None
```

!!! note
    You rarely need to call this directly. Use `run()` or let it auto-initialize.

---

### quit()

Clean up SDL2 and close all windows.

```python
wa.quit() -> None
```

---

### run()

Context manager that handles initialization and cleanup.

```python
wa.run(fps: float = 60.0) -> Generator[None, None, None]
```

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `fps` | float | `60.0` | Target frames per second for `wait()` calls |

**Example:**

```python
with wa.run():
    win = wa.window(100, 100, 200, 200)
    wa.wait(2)
# Automatic cleanup here
```

---

### run_loop()

Run a blocking event loop until `stop()` is called or window is closed.

```python
wa.run_loop(fps: float = 60.0) -> None
```

**Example:**

```python
wa.init()
win = wa.window(100, 100, 200, 200)
wa.run_loop()  # Blocks until quit
wa.quit()
```

---

### run_context()

Context manager that yields the Desktop singleton.

```python
wa.run_context(fps: float = 60.0) -> Generator[Desktop, None, None]
```

**Example:**

```python
with wa.run_context() as desktop:
    win = desktop.window(100, 100, 200, 200)
    wa.wait(2)
```

---

## Window Creation

### window()

Create a new window.

```python
wa.window(
    x: float,
    y: float,
    w: float,
    h: float,
    color: ColorLike = "white",
    opacity: float = 1.0,
    *,
    borderless: bool = True,
    always_on_top: bool = True,
    resizable: bool = False,
    title: str = "",
    shadow: bool = True,
    image: str | None = None,
    gif: str | None = None,
    video: str | None = None,
) -> Window
```

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `x` | float | required | X position |
| `y` | float | required | Y position |
| `w` | float | required | Width |
| `h` | float | required | Height |
| `color` | ColorLike | `"white"` | Background color |
| `opacity` | float | `1.0` | Opacity (0.0-1.0) |
| `borderless` | bool | `True` | Remove window decorations |
| `always_on_top` | bool | `True` | Keep above other windows |
| `resizable` | bool | `False` | Allow user resizing |
| `title` | str | `""` | Window title |
| `shadow` | bool | `True` | Drop shadow (macOS) |
| `image` | str | `None` | Path to image file |
| `gif` | str | `None` | Path to GIF file |
| `video` | str | `None` | Path to video file |

**Returns:** A new `Window` instance.

---

### windows()

Get a list of all active windows.

```python
wa.windows() -> list[Window]
```

---

### clear()

Close all windows.

```python
wa.clear() -> None
```

---

## Event Loop

### update()

Process one frame of the event loop.

```python
wa.update() -> bool
```

**Returns:** `False` if quit was requested (window closed, etc.), `True` otherwise.

**Example:**

```python
wa.init()
win = wa.window(100, 100, 100, 100)

while wa.update():
    win.x += 1
    if win.x > 500:
        break

wa.quit()
```

---

### stop()

Signal the event loop to stop.

```python
wa.stop() -> None
```

---

## Timing

### delta_time()

Get time elapsed since the last `update()` call.

```python
wa.delta_time() -> float
```

**Returns:** Time in seconds.

---

### get_time()

Get time elapsed since initialization.

```python
wa.get_time() -> float
```

**Returns:** Time in seconds.

---

## Screen Information

### screens()

Get information about all connected displays.

```python
wa.screens() -> list[Screen]
```

**Returns:** List of `Screen` dataclasses.

---

### primary_screen()

Get the primary display.

```python
wa.primary_screen() -> Screen | None
```

**Returns:** The primary `Screen` or `None` if unavailable.

---

## Screen Class

```python
@dataclass
class Screen:
    x: int        # X position of screen origin
    y: int        # Y position of screen origin
    w: int        # Screen width
    h: int        # Screen height
    index: int    # Display index

    @property
    def width(self) -> int: ...

    @property
    def height(self) -> int: ...

    @property
    def center(self) -> tuple[int, int]: ...
```

**Example:**

```python
for screen in wa.screens():
    print(f"Screen {screen.index}: {screen.w}x{screen.h} at ({screen.x}, {screen.y})")
    print(f"Center: {screen.center}")
```

---

## Desktop Singleton

The `Desktop` class manages all SDL2 state. Access via `Desktop.get()`.

```python
class Desktop:
    @classmethod
    def get(cls) -> Desktop
```

All module-level functions delegate to this singleton. Direct access is rarely needed.

### Desktop Methods

| Method | Description |
|--------|-------------|
| `init()` | Initialize SDL2 |
| `quit()` | Clean up |
| `window(...)` | Create a window |
| `windows()` | Get all windows |
| `clear()` | Close all windows |
| `screens()` | Get displays |
| `primary_screen()` | Get primary display |
| `update()` | Process one frame |
| `run(fps)` | Run event loop |
| `stop()` | Stop event loop |

### Desktop Properties

| Property | Type | Description |
|----------|------|-------------|
| `delta_time` | float | Time since last update |
| `time` | float | Time since init |
| `frame_count` | int | Frames processed |
| `running` | bool | Is loop running |
