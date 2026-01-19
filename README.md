# window-art

A minimal Python library for live coding visual scenes using desktop windows.

![window-art demo](docs/window-art.gif)

## Installation

```bash
pip install window-art
```

## Quick Start

```python
import window_art as wa

with wa.run():
    win = wa.window(100, 100, 200, 200, color="coral")
    wa.move(win, 500, 300, duration=2.0, ease="ease_out")
    wa.wait(1)
```

## Examples

```python
import window_art as wa

with wa.run():
    # Create windows
    win = wa.window(100, 100, 200, 200, color="red")

    # Animate
    wa.move(win, 500, 300, duration=1.0)
    wa.fade(win, 0.5, duration=0.5)
    wa.color_to(win, "blue", duration=0.5)

    # Display media
    img = wa.window(400, 100, 300, 200, image="photo.jpg")
    vid = wa.window(400, 350, 300, 200, video="movie.mp4")

    # Text
    txt = wa.window(100, 400, 200, 50, text="Hello!", font_size=32)

    wa.wait(3)
```
