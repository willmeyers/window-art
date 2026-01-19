# Color API Reference

Color representation and parsing utilities.

## Color Class

```python
from window_art import Color
```

### Constructor

```python
Color(r: int, g: int, b: int, a: int = 255)
```

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `r` | int | required | Red component (0-255) |
| `g` | int | required | Green component (0-255) |
| `b` | int | required | Blue component (0-255) |
| `a` | int | `255` | Alpha component (0-255) |

---

### Class Methods

#### from_name()

Create a Color from a CSS color name.

```python
Color.from_name(name: str) -> Color
```

```python
red = Color.from_name("red")
coral = Color.from_name("coral")
```

Raises `ValueError` if the name is not recognized.

---

#### from_hex()

Create a Color from a hex string.

```python
Color.from_hex(hex_str: str) -> Color
```

Supported formats:
- `#rgb` - 3-digit shorthand
- `#rrggbb` - 6-digit
- `#rgba` - 4-digit with alpha
- `#rrggbbaa` - 8-digit with alpha

```python
red = Color.from_hex("#ff0000")
red = Color.from_hex("#f00")
semi_red = Color.from_hex("#ff000080")
```

---

#### parse()

Parse a color from any supported format.

```python
Color.parse(value: ColorLike) -> Color
```

| Input Type | Description |
|------------|-------------|
| `str` | Color name or hex code |
| `(r, g, b)` | RGB tuple |
| `(r, g, b, a)` | RGBA tuple |
| `Color` | Returns unchanged |

```python
Color.parse("coral")
Color.parse("#ff6347")
Color.parse((255, 99, 71))
Color.parse((255, 99, 71, 128))
```

---

### Properties

| Property | Type | Description |
|----------|------|-------------|
| `r` | int | Red component (0-255) |
| `g` | int | Green component (0-255) |
| `b` | int | Blue component (0-255) |
| `a` | int | Alpha component (0-255) |

---

### Instance Methods

#### as_tuple()

Get color as an RGBA tuple.

```python
color.as_tuple() -> tuple[int, int, int, int]
```

```python
Color(255, 99, 71).as_tuple()  # (255, 99, 71, 255)
```

---

#### as_rgb_tuple()

Get color as an RGB tuple (without alpha).

```python
color.as_rgb_tuple() -> tuple[int, int, int]
```

```python
Color(255, 99, 71).as_rgb_tuple()  # (255, 99, 71)
```

---

#### to_hex()

Convert color to hex string.

```python
color.to_hex() -> str
```

```python
Color(255, 99, 71).to_hex()      # "#ff6347"
Color(255, 99, 71, 128).to_hex() # "#ff634780"
```

---

#### with_alpha()

Create a new Color with modified alpha.

```python
color.with_alpha(alpha: int | float) -> Color
```

| Parameter | Type | Description |
|-----------|------|-------------|
| `alpha` | int | Alpha value 0-255 |
| `alpha` | float | Alpha value 0.0-1.0 |

```python
red = Color(255, 0, 0)
semi_red = red.with_alpha(128)
semi_red = red.with_alpha(0.5)
```

---

#### lerp()

Linearly interpolate between two colors.

```python
color.lerp(other: Color, t: float) -> Color
```

| Parameter | Type | Description |
|-----------|------|-------------|
| `other` | Color | Target color |
| `t` | float | Interpolation factor (0.0-1.0) |

```python
red = Color.parse("red")
blue = Color.parse("blue")

# t=0.0 returns red, t=1.0 returns blue
purple = red.lerp(blue, 0.5)
```

---

## Type Aliases

### ColorLike

Any value that can be converted to a Color:

```python
ColorLike = str | tuple[int, int, int] | tuple[int, int, int, int] | Color
```

All color parameters in the API accept `ColorLike`.

---

## Named Colors

All 147 CSS named colors are supported:

```python
# Basic colors
"red", "green", "blue", "white", "black", "yellow", "cyan", "magenta"

# Popular web colors
"coral", "dodgerblue", "tomato", "gold", "hotpink", "limegreen"

# Grays
"whitesmoke", "gainsboro", "lightgray", "silver", "gray", "dimgray"
```

See the [Colors Guide](../guide/colors.md) for the complete list.

---

## Example

```python
from window_art import Color

# Create colors
c1 = Color(255, 99, 71)
c2 = Color.parse("dodgerblue")
c3 = Color.from_hex("#ffd700")

# Manipulate
semi = c1.with_alpha(0.5)
mid = c1.lerp(c2, 0.5)

# Convert
print(c1.to_hex())       # "#ff6347"
print(c1.as_tuple())     # (255, 99, 71, 255)
print(c1.as_rgb_tuple()) # (255, 99, 71)
```
