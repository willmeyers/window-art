# Grid Layout

window-art includes a CSS Grid-inspired layout system for creating complex arrangements of windows.

## Creating a Grid

```python
import window_art as wa

with wa.run():
    # Create a 3-column, 2-row grid
    grid = wa.grid(100, 100, 600, 400,
        columns="1fr 1fr 1fr",
        rows="1fr 1fr"
    )
```

### Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `x` | float | required | Grid X position |
| `y` | float | required | Grid Y position |
| `w` | float | required | Total grid width |
| `h` | float | required | Total grid height |
| `columns` | str | `"1fr"` | Column template |
| `rows` | str | `"1fr"` | Row template |
| `gap` | float/tuple | `0` | Gap between cells |

## Track Sizing

Track sizes use CSS-like syntax:

### Fractional Units (fr)

Distribute remaining space proportionally:

```python
# Three equal columns
grid = wa.grid(0, 0, 600, 400, columns="1fr 1fr 1fr")

# Middle column twice as wide
grid = wa.grid(0, 0, 600, 400, columns="1fr 2fr 1fr")
```

### Fixed Pixels (px)

Fixed-size tracks:

```python
# First column fixed at 100px, rest flexible
grid = wa.grid(0, 0, 600, 400, columns="100px 1fr 1fr")

# Both fixed
grid = wa.grid(0, 0, 600, 400, columns="100px 200px")
```

### Mixed

Combine fixed and flexible:

```python
# Sidebar (200px) + main content (flexible) + sidebar (200px)
grid = wa.grid(0, 0, 1000, 600, columns="200px 1fr 200px")
```

## Gaps

Space between cells:

```python
# Uniform gap
grid = wa.grid(0, 0, 600, 400, columns="1fr 1fr", gap=10)

# Different column and row gaps
grid = wa.grid(0, 0, 600, 400, columns="1fr 1fr", gap=(10, 20))
```

## Creating Cell Windows

### Single Cell

```python
win = grid.cell(row, col, color, **kwargs)
```

```python
grid = wa.grid(100, 100, 600, 400, columns="1fr 1fr 1fr", rows="1fr 1fr")

# Create window in top-left cell
win = grid.cell(0, 0, "coral")

# Create window in bottom-right cell
win = grid.cell(1, 2, "dodgerblue")
```

### Spanning Cells

```python
# Window spanning 2 columns
win = grid.cell(0, 0, "green", colspan=2)

# Window spanning 2 rows
win = grid.cell(0, 0, "blue", rowspan=2)

# Window spanning both
win = grid.cell(0, 0, "purple", rowspan=2, colspan=2)
```

### Fill All Cells

```python
# Fill with colors
colors = ["red", "orange", "yellow", "green", "blue", "purple"]
windows = grid.fill(colors)

# Windows are created left-to-right, top-to-bottom
```

## Media in Grid Cells

### Fill with Image

Split an image across the entire grid:

```python
grid = wa.grid(100, 100, 600, 400, columns="1fr 1fr 1fr", rows="1fr 1fr")
windows = grid.fill_image("photo.jpg")
```

Each cell displays its corresponding portion of the image.

### Fill with GIF

```python
windows = grid.fill_gif("animation.gif")
```

### Fill with Video

```python
windows = grid.fill_video("movie.mp4")
```

## Accessing Windows

### By Coordinates

```python
win = grid[0, 1]  # Get window at row 0, column 1
```

### By Index

```python
win = grid[0]  # First window
win = grid[3]  # Fourth window
```

### Check Existence

```python
if (0, 1) in grid:
    print("Cell (0, 1) has a window")
```

### Iterate

```python
for win in grid:
    win.color = "blue"
```

### Count

```python
print(f"Grid has {len(grid)} windows")
```

## Grid Properties

```python
grid.x, grid.y      # Grid position
grid.w, grid.h      # Grid size
grid.num_cols       # Number of columns
grid.num_rows       # Number of rows
grid.gap            # (column_gap, row_gap)
```

## Grid Operations

### Move Grid

```python
grid.move_to(200, 200)  # Moves all windows
```

### Resize Grid

```python
grid.resize_to(800, 600)  # Resize and reposition all windows
```

### Animated Resize

```python
grid.animate_to(200, 200, 800, 600, duration=1.0, ease="ease_out")
```

### Clear Grid

```python
grid.clear()  # Close all windows in grid
```

## Swapping Cells

### Instant Swap

```python
grid.swap(0, 0, 1, 2)  # Swap (0,0) with (1,2)
```

### Animated Swap

```python
grid.swap_animated(0, 0, 1, 2, duration=0.5, ease="ease_in_out")
```

## Cell Specifications

Get cell geometry without creating windows:

```python
from window_art import grid_layout

# Just calculate positions
cells = grid_layout(100, 100, 600, 400,
    columns="1fr 1fr 1fr",
    rows="1fr 1fr"
)

for cell in cells:
    print(f"Cell ({cell.row}, {cell.col}): {cell.x}, {cell.y}, {cell.w}x{cell.h}")
```

## Example: Photo Gallery

```python
import window_art as wa

with wa.run():
    # Create a 3x2 photo grid
    grid = wa.grid(50, 50, 900, 600,
        columns="1fr 1fr 1fr",
        rows="1fr 1fr",
        gap=10
    )

    photos = ["p1.jpg", "p2.jpg", "p3.jpg", "p4.jpg", "p5.jpg", "p6.jpg"]

    for i, photo in enumerate(photos):
        row, col = divmod(i, 3)
        grid.cell(row, col, "black", image=photo)

    wa.wait(5)
```

## Example: Dashboard Layout

```python
import window_art as wa

with wa.run():
    # Sidebar + main content + aside
    grid = wa.grid(0, 0, 1200, 800,
        columns="200px 1fr 250px",
        rows="60px 1fr 40px",
        gap=5
    )

    # Header spanning all columns
    grid.cell(0, 0, "darkblue", colspan=3)

    # Sidebar
    grid.cell(1, 0, "lightgray")

    # Main content
    grid.cell(1, 1, "white")

    # Aside
    grid.cell(1, 2, "lightgray")

    # Footer spanning all columns
    grid.cell(2, 0, "darkblue", colspan=3)

    wa.wait(5)
```

## Example: Animated Grid

```python
import window_art as wa
import random

with wa.run():
    grid = wa.grid(100, 100, 400, 400,
        columns="1fr 1fr 1fr",
        rows="1fr 1fr 1fr",
        gap=5
    )

    colors = ["coral", "dodgerblue", "gold", "limegreen",
              "hotpink", "orange", "purple", "turquoise", "tomato"]
    grid.fill(colors)

    wa.wait(1)

    # Shuffle animation
    for _ in range(10):
        r1, c1 = random.randint(0, 2), random.randint(0, 2)
        r2, c2 = random.randint(0, 2), random.randint(0, 2)
        grid.swap_animated(r1, c1, r2, c2, duration=0.3)

    wa.wait(1)
```
