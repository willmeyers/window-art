# Colors

window-art supports multiple color formats and includes all 147 CSS named colors.

## Color Formats

### Named Colors

Use any of the 147 CSS named colors:

```python
win.color = "coral"
win.color = "dodgerblue"
win.color = "mediumseagreen"
```

### Hex Codes

Standard hex color notation:

```python
win.color = "#ff6347"    # 6-digit hex
win.color = "#f00"       # 3-digit shorthand (expands to #ff0000)
win.color = "#ff634780"  # 8-digit with alpha
win.color = "#f008"      # 4-digit shorthand with alpha
```

### RGB Tuples

Integer values from 0-255:

```python
win.color = (255, 99, 71)       # RGB
win.color = (255, 99, 71, 128)  # RGBA
```

### Color Objects

For programmatic color manipulation:

```python
from window_art import Color

# Create directly
c = Color(255, 99, 71)
c = Color(255, 99, 71, 128)  # With alpha

# Parse from string
c = Color.parse("coral")
c = Color.parse("#ff6347")

# From specific format
c = Color.from_name("coral")
c = Color.from_hex("#ff6347")
```

## The Color Class

```python
from window_art import Color
```

### Properties

| Property | Type | Description |
|----------|------|-------------|
| `r` | int | Red component (0-255) |
| `g` | int | Green component (0-255) |
| `b` | int | Blue component (0-255) |
| `a` | int | Alpha component (0-255, default 255) |

### Methods

```python
# Get as tuples
c.as_tuple()      # (r, g, b, a)
c.as_rgb_tuple()  # (r, g, b)

# Convert to hex
c.to_hex()        # "#rrggbb" or "#rrggbbaa" if alpha != 255

# Modify alpha
c2 = c.with_alpha(128)    # Integer 0-255
c2 = c.with_alpha(0.5)    # Float 0.0-1.0

# Interpolate between colors
c1 = Color.parse("red")
c2 = Color.parse("blue")
mid = c1.lerp(c2, 0.5)    # Purple (halfway between)
```

## Color Interpolation

The `lerp()` method linearly interpolates between two colors:

```python
from window_art import Color

red = Color.parse("red")
blue = Color.parse("blue")

# t=0.0 returns red, t=1.0 returns blue
for t in [0.0, 0.25, 0.5, 0.75, 1.0]:
    c = red.lerp(blue, t)
    print(f"t={t}: rgb({c.r}, {c.g}, {c.b})")
```

This is used internally by `color_to()` for animated transitions.

## Animated Color Changes

```python
import window_art as wa

with wa.run():
    win = wa.window(100, 100, 200, 200, color="red")

    # Smooth transition to blue over 1 second
    wa.color_to(win, "blue", duration=1.0)

    # Chain multiple transitions
    wa.color_to(win, "green", duration=0.5)
    wa.color_to(win, "#ff6347", duration=0.5)

    wa.wait(1)
```

## Named Colors Reference

All CSS named colors are supported. Here are some commonly used ones:

### Basic Colors

| Name | Hex | Preview |
|------|-----|---------|
| `red` | #ff0000 | Red |
| `green` | #008000 | Green |
| `blue` | #0000ff | Blue |
| `white` | #ffffff | White |
| `black` | #000000 | Black |
| `yellow` | #ffff00 | Yellow |
| `cyan` | #00ffff | Cyan |
| `magenta` | #ff00ff | Magenta |

### Popular Web Colors

| Name | Hex | Description |
|------|-----|-------------|
| `coral` | #ff7f50 | Warm orange-pink |
| `dodgerblue` | #1e90ff | Bright blue |
| `tomato` | #ff6347 | Red-orange |
| `gold` | #ffd700 | Bright yellow |
| `hotpink` | #ff69b4 | Vibrant pink |
| `limegreen` | #32cd32 | Bright green |
| `orange` | #ffa500 | Pure orange |
| `purple` | #800080 | Deep purple |
| `salmon` | #fa8072 | Light red |
| `turquoise` | #40e0d0 | Blue-green |

### Grays

| Name | Hex |
|------|-----|
| `whitesmoke` | #f5f5f5 |
| `gainsboro` | #dcdcdc |
| `lightgray` | #d3d3d3 |
| `silver` | #c0c0c0 |
| `darkgray` | #a9a9a9 |
| `gray` | #808080 |
| `dimgray` | #696969 |

### Full List

The complete list of 147 CSS colors includes:

`aliceblue`, `antiquewhite`, `aqua`, `aquamarine`, `azure`, `beige`, `bisque`, `black`, `blanchedalmond`, `blue`, `blueviolet`, `brown`, `burlywood`, `cadetblue`, `chartreuse`, `chocolate`, `coral`, `cornflowerblue`, `cornsilk`, `crimson`, `cyan`, `darkblue`, `darkcyan`, `darkgoldenrod`, `darkgray`, `darkgreen`, `darkgrey`, `darkkhaki`, `darkmagenta`, `darkolivegreen`, `darkorange`, `darkorchid`, `darkred`, `darksalmon`, `darkseagreen`, `darkslateblue`, `darkslategray`, `darkslategrey`, `darkturquoise`, `darkviolet`, `deeppink`, `deepskyblue`, `dimgray`, `dimgrey`, `dodgerblue`, `firebrick`, `floralwhite`, `forestgreen`, `fuchsia`, `gainsboro`, `ghostwhite`, `gold`, `goldenrod`, `gray`, `green`, `greenyellow`, `grey`, `honeydew`, `hotpink`, `indianred`, `indigo`, `ivory`, `khaki`, `lavender`, `lavenderblush`, `lawngreen`, `lemonchiffon`, `lightblue`, `lightcoral`, `lightcyan`, `lightgoldenrodyellow`, `lightgray`, `lightgreen`, `lightgrey`, `lightpink`, `lightsalmon`, `lightseagreen`, `lightskyblue`, `lightslategray`, `lightslategrey`, `lightsteelblue`, `lightyellow`, `lime`, `limegreen`, `linen`, `magenta`, `maroon`, `mediumaquamarine`, `mediumblue`, `mediumorchid`, `mediumpurple`, `mediumseagreen`, `mediumslateblue`, `mediumspringgreen`, `mediumturquoise`, `mediumvioletred`, `midnightblue`, `mintcream`, `mistyrose`, `moccasin`, `navajowhite`, `navy`, `oldlace`, `olive`, `olivedrab`, `orange`, `orangered`, `orchid`, `palegoldenrod`, `palegreen`, `paleturquoise`, `palevioletred`, `papayawhip`, `peachpuff`, `peru`, `pink`, `plum`, `powderblue`, `purple`, `rebeccapurple`, `red`, `rosybrown`, `royalblue`, `saddlebrown`, `salmon`, `sandybrown`, `seagreen`, `seashell`, `sienna`, `silver`, `skyblue`, `slateblue`, `slategray`, `slategrey`, `snow`, `springgreen`, `steelblue`, `tan`, `teal`, `thistle`, `tomato`, `turquoise`, `violet`, `wheat`, `white`, `whitesmoke`, `yellow`, `yellowgreen`

## Type Alias: ColorLike

The `ColorLike` type accepts any of these formats:

```python
ColorLike = str | tuple[int, int, int] | tuple[int, int, int, int] | Color
```

All color parameters in the API accept `ColorLike`:

```python
wa.window(100, 100, 200, 200, color="coral")  # str
wa.window(100, 100, 200, 200, color=(255, 127, 80))  # tuple
wa.window(100, 100, 200, 200, color=Color(255, 127, 80))  # Color
```
