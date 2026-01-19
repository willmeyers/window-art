# Grid API Reference

CSS Grid-inspired layout system for arranging windows.

## grid()

Create a new grid layout.

```python
wa.grid(
    x: float,
    y: float,
    w: float,
    h: float,
    columns: str = "1fr",
    rows: str = "1fr",
    gap: float | tuple[float, float] = 0
) -> Grid
```

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `x` | float | required | Grid X position |
| `y` | float | required | Grid Y position |
| `w` | float | required | Total grid width |
| `h` | float | required | Total grid height |
| `columns` | str | `"1fr"` | Column template |
| `rows` | str | `"1fr"` | Row template |
| `gap` | float/tuple | `0` | Gap between cells |

---

## Grid Class

### Properties

| Property | Type | Description |
|----------|------|-------------|
| `x` | float | Grid X position |
| `y` | float | Grid Y position |
| `w` | float | Grid width |
| `h` | float | Grid height |
| `num_cols` | int | Number of columns |
| `num_rows` | int | Number of rows |
| `gap` | tuple[float, float] | (column_gap, row_gap) |

---

### Cell Creation

#### cell()

Create a window in a grid cell.

```python
grid.cell(
    row: int,
    col: int,
    color: ColorLike,
    rowspan: int = 1,
    colspan: int = 1,
    **kwargs
) -> Window
```

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `row` | int | required | Row index (0-based) |
| `col` | int | required | Column index (0-based) |
| `color` | ColorLike | required | Cell color |
| `rowspan` | int | `1` | Rows to span |
| `colspan` | int | `1` | Columns to span |
| `**kwargs` | | | Additional window options |

```python
grid.cell(0, 0, "red")
grid.cell(0, 1, "blue", colspan=2)
grid.cell(1, 0, "green", rowspan=2, opacity=0.5)
```

---

#### fill()

Fill all cells with colors.

```python
grid.fill(colors: list[ColorLike], **kwargs) -> list[Window]
```

Colors are applied left-to-right, top-to-bottom.

```python
colors = ["red", "orange", "yellow", "green", "blue", "purple"]
windows = grid.fill(colors)
```

---

#### fill_image()

Split an image across the grid.

```python
grid.fill_image(path: str, **kwargs) -> list[Window]
```

Each cell displays its corresponding portion of the image.

---

#### fill_gif()

Split a GIF across the grid.

```python
grid.fill_gif(path: str, **kwargs) -> list[Window]
```

---

#### fill_video()

Split a video across the grid.

```python
grid.fill_video(path: str, **kwargs) -> list[Window]
```

---

### Cell Access

#### get_cell_spec()

Get geometry for a cell without creating a window.

```python
grid.get_cell_spec(row: int, col: int) -> CellSpec
```

---

#### Container Protocol

```python
# By coordinates
win = grid[0, 1]

# By linear index
win = grid[0]

# Check existence
if (0, 1) in grid:
    ...

# Iterate
for win in grid:
    ...

# Count
len(grid)
```

---

### Grid Manipulation

#### move_to()

Move the entire grid to a new position.

```python
grid.move_to(x: float, y: float) -> None
```

---

#### resize_to()

Resize the grid and reposition all windows.

```python
grid.resize_to(w: float, h: float) -> None
```

---

#### animate_to()

Animate grid position and size.

```python
grid.animate_to(
    x: float,
    y: float,
    w: float,
    h: float,
    duration: float = 0.5,
    ease: str = "ease_out"
) -> None
```

---

#### swap()

Instantly swap two cells.

```python
grid.swap(r1: int, c1: int, r2: int, c2: int) -> None
```

---

#### swap_animated()

Swap two cells with animation.

```python
grid.swap_animated(
    r1: int, c1: int,
    r2: int, c2: int,
    duration: float = 0.3,
    ease: str = "ease_in_out"
) -> None
```

---

#### clear()

Close all windows in the grid.

```python
grid.clear() -> None
```

---

## Track Sizing

### TrackSize Class

```python
from window_art.layout import TrackSize
```

#### Properties

| Property | Type | Description |
|----------|------|-------------|
| `value` | float | Numeric value |
| `unit` | str | `"fr"` or `"px"` |

#### parse()

Parse a track size specification.

```python
TrackSize.parse(spec: str) -> TrackSize
```

| Input | Result |
|-------|--------|
| `"1fr"` | TrackSize(1.0, "fr") |
| `"2fr"` | TrackSize(2.0, "fr") |
| `"100px"` | TrackSize(100.0, "px") |
| `"100"` | TrackSize(100.0, "px") |

---

## CellSpec Class

Geometry specification for a cell.

```python
from window_art.layout import CellSpec
```

| Property | Type | Description |
|----------|------|-------------|
| `x` | float | Cell X position |
| `y` | float | Cell Y position |
| `w` | float | Cell width |
| `h` | float | Cell height |
| `row` | int | Row index |
| `col` | int | Column index |

---

## grid_layout()

Calculate cell positions without creating windows.

```python
from window_art import grid_layout

grid_layout(
    x: float,
    y: float,
    w: float,
    h: float,
    columns: str,
    rows: str,
    gap: float | tuple[float, float] = 0
) -> list[CellSpec]
```

```python
cells = grid_layout(0, 0, 600, 400, "1fr 1fr 1fr", "1fr 1fr")
for cell in cells:
    print(f"({cell.row}, {cell.col}): {cell.x}, {cell.y}, {cell.w}x{cell.h}")
```

---

## Examples

### Basic Grid

```python
import window_art as wa

with wa.run():
    grid = wa.grid(100, 100, 600, 400,
        columns="1fr 1fr 1fr",
        rows="1fr 1fr"
    )

    grid.fill(["red", "orange", "yellow", "green", "blue", "purple"])
    wa.wait(3)
```

### Mixed Sizing

```python
grid = wa.grid(0, 0, 800, 600,
    columns="200px 1fr 200px",  # Fixed-flexible-fixed
    rows="60px 1fr 40px"        # Header-content-footer
)
```

### Spanning Cells

```python
grid = wa.grid(100, 100, 400, 400, columns="1fr 1fr", rows="1fr 1fr")

# Top cell spans both columns
grid.cell(0, 0, "blue", colspan=2)

# Left cell spans both rows
grid.cell(0, 0, "green", rowspan=2)
```

### Animated Swap

```python
import random

grid = wa.grid(100, 100, 300, 300, columns="1fr 1fr 1fr", rows="1fr 1fr 1fr")
grid.fill(["red", "orange", "yellow", "green", "blue", "purple", "pink", "cyan", "white"])

for _ in range(10):
    r1, c1 = random.randint(0, 2), random.randint(0, 2)
    r2, c2 = random.randint(0, 2), random.randint(0, 2)
    grid.swap_animated(r1, c1, r2, c2, duration=0.3)
```
