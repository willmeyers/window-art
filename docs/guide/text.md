# Text Support

window-art can display text in windows using Pillow for rendering.

## Basic Usage

### Creating a Text Window

```python
import window_art as wa

with wa.run():
    win = wa.window(100, 100, 300, 80, text="Hello World")
    wa.wait(3)
```

### Text with Styling

```python
win = wa.window(100, 100, 400, 100,
    text="Welcome!",
    font="Arial",
    font_size=48,
    text_color="navy",
    color="lightyellow",  # background color
)
```

## Text Properties

### Setting Text Content

```python
# Create window with text
win = wa.window(100, 100, 300, 80, text="Initial text")

# Update text dynamically
win.text = "New text"

# Clear text
win.text = None
```

### Font Settings

```python
# Font family (system font name)
win.font = "Arial"
win.font = "Times New Roman"
win.font = "Courier New"

# Or use a font file path
win.font = "/path/to/custom-font.ttf"

# Font size in pixels
win.font_size = 24   # default
win.font_size = 48   # larger
win.font_size = 12   # smaller
```

### Text Color

```python
# Named colors
win.text_color = "black"    # default
win.text_color = "red"
win.text_color = "navy"

# Hex colors
win.text_color = "#FF5500"
win.text_color = "#333"

# RGB tuples
win.text_color = (255, 128, 0)
```

### Text Alignment

```python
# Horizontal alignment
win.text_align = "center"  # default
win.text_align = "left"
win.text_align = "right"

# Vertical alignment
win.text_valign = "center"  # default
win.text_valign = "top"
win.text_valign = "bottom"
```

### Text Wrapping

```python
# Enable word wrapping
win.text_wrap = True

# Disable (default)
win.text_wrap = False
```

When wrapping is enabled, text will break at word boundaries to fit within the window width.

### Text Padding

```python
# Uniform padding (all sides)
win.text_padding = 20

# Horizontal and vertical padding
win.text_padding = (20, 10)  # (horizontal, vertical)

# Individual padding (left, top, right, bottom)
win.text_padding = (10, 5, 10, 5)
```

## Text with Images

Text is rendered on top of background colors and media (images, GIFs, videos):

```python
# Text on solid color background
win = wa.window(100, 100, 400, 300,
    color="lightblue",
    text="Caption",
    text_valign="bottom",
    text_padding=10,
)

# Text overlay on image
win = wa.window(100, 100, 400, 300,
    image="photo.jpg",
    text="Photo Title",
    text_color="white",
    text_valign="bottom",
    text_padding=20,
)

# Text overlay on video
win = wa.window(100, 100, 640, 480,
    video="movie.mp4",
    text="Now Playing",
    text_color="white",
    text_valign="top",
    text_align="left",
    text_padding=10,
)
```

## Checking Support

```python
from window_art import has_text_support

if has_text_support():
    win = wa.window(100, 100, 300, 80, text="Hello")
else:
    print("Text support not available (install Pillow)")
```

## Measuring Text

Get text dimensions without creating a window:

```python
from window_art import get_text_size

# Measure with default font
width, height = get_text_size("Hello World")

# Measure with specific font settings
width, height = get_text_size(
    "Hello World",
    font="Arial",
    font_size=48,
)

print(f"Text would be {width}x{height} pixels")
```

## Example: Dynamic Counter

```python
import window_art as wa

with wa.run():
    win = wa.window(100, 100, 200, 100,
        text="0",
        font_size=64,
        text_color="green",
    )

    for i in range(1, 11):
        wa.wait(1)
        win.text = str(i)
```

## Example: Multi-line Text

```python
import window_art as wa

with wa.run():
    win = wa.window(100, 100, 400, 200,
        text="Line 1\nLine 2\nLine 3",
        text_align="left",
        text_valign="top",
        text_padding=20,
    )
    wa.wait(3)
```

## Example: Wrapped Text

```python
import window_art as wa

long_text = "This is a long text that will automatically wrap to fit within the window boundaries."

with wa.run():
    win = wa.window(100, 100, 300, 200,
        text=long_text,
        text_wrap=True,
        text_padding=15,
    )
    wa.wait(5)
```

## Example: Animated Text

```python
import window_art as wa

with wa.run():
    win = wa.window(100, 100, 400, 100,
        text="Fading In",
        font_size=36,
        opacity=0,
    )

    # Fade in
    wa.fade_in(win, duration=1)
    wa.wait(1)

    # Change text
    win.text = "Fading Out"
    wa.wait(1)

    # Fade out
    wa.fade_out(win, duration=1)
```

## Example: Notification Banner

```python
import window_art as wa

def show_notification(message, duration=3):
    screen = wa.primary_screen()
    win = wa.window(
        screen.w - 420, 20, 400, 60,
        color="#333333",
        text=message,
        text_color="white",
        text_padding=15,
        opacity=0,
    )
    wa.fade_in(win, duration=0.3)
    wa.wait(duration)
    wa.fade_out(win, duration=0.3)
    win.close()

with wa.run():
    show_notification("File saved successfully!")
    show_notification("Download complete!")
```

## Performance Notes

- Text is rendered to a texture when created or modified
- Changing text properties triggers a re-render
- Window resizing also triggers text re-render
- For frequently changing text, consider using smaller font sizes

## Font Availability

The text renderer tries to find fonts in this order:

1. Direct font file path (`.ttf`, `.otf`)
2. System font by name
3. System font directories:
   - macOS: `/System/Library/Fonts/`, `/Library/Fonts/`
   - Windows: `C:\Windows\Fonts\`
   - Linux: `/usr/share/fonts/`, `~/.fonts/`
4. Pillow's default font as fallback
