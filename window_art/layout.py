"""CSS Grid-like layout system for desktop windows."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Iterator, Sequence, overload

from .animate import _parallel_gen, _run_animation, move_async, resize_async
from .color import ColorLike
from .core import Desktop
from .easing import EasingFunc, get_easing, linear
from .media import get_gif_size, get_image_size, get_video_size
from .window import Window


@dataclass(slots=True)
class TrackSize:
    """Represents a grid track size (column width or row height).

    Supports two units:
    - "fr": Fractional unit, shares remaining space proportionally
    - "px": Fixed pixels
    """
    value: float
    unit: str

    @classmethod
    def parse(cls, spec: str) -> TrackSize:
        """Parse a track size specification.

        Examples:
            "1fr" -> TrackSize(1.0, "fr")
            "2fr" -> TrackSize(2.0, "fr")
            "100px" -> TrackSize(100.0, "px")
            "100" -> TrackSize(100.0, "px")
        """
        spec = spec.strip()
        if spec.endswith("fr"):
            value = float(spec[:-2])
            return cls(value, "fr")
        elif spec.endswith("px"):
            value = float(spec[:-2])
            return cls(value, "px")
        else:
            value = float(spec)
            return cls(value, "px")


@dataclass(slots=True)
class CellSpec:
    """Specification for a grid cell's computed position and size."""
    x: float
    y: float
    w: float
    h: float
    row: int
    col: int


def _parse_template(template: str) -> list[TrackSize]:
    """Parse a space-separated template string into track sizes."""
    parts = template.split()
    return [TrackSize.parse(p) for p in parts]


def _compute_track_sizes(
    tracks: list[TrackSize],
    available: float,
    gap: float,
) -> list[float]:
    """Compute actual pixel sizes for tracks.

    Algorithm:
    1. Subtract total gaps from available space
    2. Allocate fixed (px) tracks first
    3. Distribute remaining space to fr tracks proportionally
    """
    num_gaps = len(tracks) - 1 if len(tracks) > 1 else 0
    usable = available - (gap * num_gaps)

    fixed_total = sum(t.value for t in tracks if t.unit == "px")
    fr_total = sum(t.value for t in tracks if t.unit == "fr")

    remaining = max(0.0, usable - fixed_total)
    fr_unit = remaining / fr_total if fr_total > 0 else 0.0

    sizes = []
    for track in tracks:
        if track.unit == "px":
            sizes.append(track.value)
        else:
            sizes.append(track.value * fr_unit)

    return sizes


def _compute_track_positions(sizes: list[float], start: float, gap: float) -> list[float]:
    """Compute starting positions for each track."""
    positions = []
    pos = start
    for size in sizes:
        positions.append(pos)
        pos += size + gap
    return positions


def grid_layout(
    x: float,
    y: float,
    w: float,
    h: float,
    columns: str,
    rows: str,
    gap: float | tuple[float, float] = 0,
) -> list[CellSpec]:
    """Compute cell specifications for a grid layout.

    This is a pure calculation function that doesn't create windows.

    Args:
        x, y: Grid origin position
        w, h: Grid total size
        columns: Column template (e.g., "1fr 2fr 100px")
        rows: Row template (e.g., "100px 1fr 1fr")
        gap: Gap between cells (single value or (column_gap, row_gap))

    Returns:
        List of CellSpec objects for each cell, in row-major order.
    """
    col_gap, row_gap = (gap, gap) if isinstance(gap, (int, float)) else gap

    col_tracks = _parse_template(columns)
    row_tracks = _parse_template(rows)

    col_sizes = _compute_track_sizes(col_tracks, w, col_gap)
    row_sizes = _compute_track_sizes(row_tracks, h, row_gap)

    col_positions = _compute_track_positions(col_sizes, x, col_gap)
    row_positions = _compute_track_positions(row_sizes, y, row_gap)

    cells = []
    for row_idx, (row_pos, row_size) in enumerate(zip(row_positions, row_sizes)):
        for col_idx, (col_pos, col_size) in enumerate(zip(col_positions, col_sizes)):
            cells.append(CellSpec(
                x=col_pos,
                y=row_pos,
                w=col_size,
                h=row_size,
                row=row_idx,
                col=col_idx,
            ))

    return cells


class Grid:
    """A CSS Grid-like layout that manages a grid of windows.

    Example:
        grid = Grid(100, 100, 800, 600,
            columns="1fr 2fr 1fr",
            rows="100px 1fr",
            gap=10)

        grid.cell(0, 0, color="red")       # Row 0, Col 0
        grid.cell(0, 1, color="blue")      # Row 0, Col 1
        grid.fill(["red", "green", "blue", "yellow"])  # Fill remaining
    """

    def __init__(
        self,
        x: float,
        y: float,
        w: float,
        h: float,
        columns: str = "1fr",
        rows: str = "1fr",
        gap: float | tuple[float, float] = 0,
    ) -> None:
        """Create a new grid.

        Args:
            x, y: Grid origin position
            w, h: Grid total size
            columns: Column template (e.g., "1fr 2fr 100px")
            rows: Row template (e.g., "100px 1fr 1fr")
            gap: Gap between cells (single value or (column_gap, row_gap))
        """
        self._x = float(x)
        self._y = float(y)
        self._w = float(w)
        self._h = float(h)
        self._columns = columns
        self._rows = rows
        self._gap = gap

        self._col_tracks = _parse_template(columns)
        self._row_tracks = _parse_template(rows)

        self._windows: dict[tuple[int, int], Window] = {}

        self._spans: dict[tuple[int, int], tuple[int, int]] = {}

    @property
    def x(self) -> float:
        """Grid X position."""
        return self._x

    @property
    def y(self) -> float:
        """Grid Y position."""
        return self._y

    @property
    def w(self) -> float:
        """Grid width."""
        return self._w

    @property
    def h(self) -> float:
        """Grid height."""
        return self._h

    @property
    def num_rows(self) -> int:
        """Number of rows in the grid."""
        return len(self._row_tracks)

    @property
    def num_cols(self) -> int:
        """Number of columns in the grid."""
        return len(self._col_tracks)

    @property
    def gap(self) -> tuple[float, float]:
        """Gap as (column_gap, row_gap)."""
        if isinstance(self._gap, (int, float)):
            return (self._gap, self._gap)
        return self._gap

    def _compute_cell(
        self,
        row: int,
        col: int,
        rowspan: int = 1,
        colspan: int = 1,
    ) -> CellSpec:
        """Compute the position and size for a cell (with optional spanning)."""
        col_gap, row_gap = self.gap

        col_sizes = _compute_track_sizes(self._col_tracks, self._w, col_gap)
        row_sizes = _compute_track_sizes(self._row_tracks, self._h, row_gap)

        col_positions = _compute_track_positions(col_sizes, self._x, col_gap)
        row_positions = _compute_track_positions(row_sizes, self._y, row_gap)

        cell_x = col_positions[col]
        cell_y = row_positions[row]

        cell_w = sum(col_sizes[col:col + colspan])
        if colspan > 1:
            cell_w += col_gap * (colspan - 1)

        cell_h = sum(row_sizes[row:row + rowspan])
        if rowspan > 1:
            cell_h += row_gap * (rowspan - 1)

        return CellSpec(x=cell_x, y=cell_y, w=cell_w, h=cell_h, row=row, col=col)

    def get_cell_spec(self, row: int, col: int) -> CellSpec:
        """Get the computed specification for a cell."""
        rowspan, colspan = self._spans.get((row, col), (1, 1))
        return self._compute_cell(row, col, rowspan, colspan)

    def cell(
        self,
        row: int,
        col: int,
        color: ColorLike = "white",
        rowspan: int = 1,
        colspan: int = 1,
        **kwargs: Any,
    ) -> Window:
        """Create a window in a grid cell.

        Args:
            row: Row index (0-based)
            col: Column index (0-based)
            color: Window color
            rowspan: Number of rows to span
            colspan: Number of columns to span
            **kwargs: Additional arguments passed to window()

        Returns:
            The created Window
        """
        if row < 0 or row >= self.num_rows:
            raise ValueError(f"Row {row} out of range [0, {self.num_rows})")
        if col < 0 or col >= self.num_cols:
            raise ValueError(f"Column {col} out of range [0, {self.num_cols})")
        if row + rowspan > self.num_rows:
            raise ValueError(f"Row span exceeds grid bounds")
        if col + colspan > self.num_cols:
            raise ValueError(f"Column span exceeds grid bounds")

        if (row, col) in self._windows:
            self._windows[(row, col)].close()

        spec = self._compute_cell(row, col, rowspan, colspan)
        desktop = Desktop.get()
        win = desktop.window(spec.x, spec.y, spec.w, spec.h, color=color, **kwargs)

        self._windows[(row, col)] = win
        self._spans[(row, col)] = (rowspan, colspan)

        return win

    def fill(
        self,
        colors: Sequence[ColorLike],
        **kwargs: Any,
    ) -> list[Window]:
        """Fill the grid with windows of the given colors.

        Creates windows in row-major order. If more colors than cells,
        extra colors are ignored. If fewer colors than cells, only
        fills as many cells as there are colors.

        Args:
            colors: Sequence of colors to fill with
            **kwargs: Additional arguments passed to window()

        Returns:
            List of created windows
        """
        windows: list[Window] = []
        color_idx = 0

        for row in range(self.num_rows):
            for col in range(self.num_cols):
                if color_idx >= len(colors):
                    return windows

                if (row, col) in self._windows:
                    continue

                win = self.cell(row, col, color=colors[color_idx], **kwargs)
                windows.append(win)
                color_idx += 1

        return windows

    def fill_image(
        self,
        image_path: str,
        **kwargs: Any,
    ) -> list[Window]:
        """Fill the grid with a single image split across all cells.

        Each cell displays a portion of the image corresponding to its
        position in the grid, creating a tiled/split image effect.

        Args:
            image_path: Path to the image file
            **kwargs: Additional arguments passed to window()

        Returns:
            List of created windows
        """
        img_w, img_h = get_image_size(image_path)

        col_gap, row_gap = self.gap
        col_sizes = _compute_track_sizes(self._col_tracks, self._w, col_gap)
        row_sizes = _compute_track_sizes(self._row_tracks, self._h, row_gap)

        total_col = sum(col_sizes)
        total_row = sum(row_sizes)

        windows: list[Window] = []

        img_y = 0.0
        for row in range(self.num_rows):
            img_x = 0.0
            row_h = (row_sizes[row] / total_row) * img_h

            for col in range(self.num_cols):
                col_w = (col_sizes[col] / total_col) * img_w

                src_x = int(img_x)
                src_y = int(img_y)
                src_w = int(col_w)
                src_h = int(row_h)

                if col == self.num_cols - 1:
                    src_w = img_w - src_x
                if row == self.num_rows - 1:
                    src_h = img_h - src_y

                win = self.cell(row, col, image=image_path, **kwargs)
                win.image_region = (src_x, src_y, src_w, src_h)
                windows.append(win)

                img_x += col_w
            img_y += row_h

        return windows

    def fill_gif(
        self,
        gif_path: str,
        **kwargs: Any,
    ) -> list[Window]:
        """Fill the grid with a single animated GIF split across all cells.

        Each cell displays a portion of the GIF corresponding to its
        position in the grid, creating a tiled/split animated effect.

        Args:
            gif_path: Path to the GIF file
            **kwargs: Additional arguments passed to window()

        Returns:
            List of created windows
        """
        gif_w, gif_h = get_gif_size(gif_path)

        col_gap, row_gap = self.gap
        col_sizes = _compute_track_sizes(self._col_tracks, self._w, col_gap)
        row_sizes = _compute_track_sizes(self._row_tracks, self._h, row_gap)

        total_col = sum(col_sizes)
        total_row = sum(row_sizes)

        windows: list[Window] = []

        gif_y = 0.0
        for row in range(self.num_rows):
            gif_x = 0.0
            row_h = (row_sizes[row] / total_row) * gif_h

            for col in range(self.num_cols):
                col_w = (col_sizes[col] / total_col) * gif_w

                src_x = int(gif_x)
                src_y = int(gif_y)
                src_w = int(col_w)
                src_h = int(row_h)

                if col == self.num_cols - 1:
                    src_w = gif_w - src_x
                if row == self.num_rows - 1:
                    src_h = gif_h - src_y

                win = self.cell(row, col, gif=gif_path, **kwargs)
                win.gif_region = (src_x, src_y, src_w, src_h)
                windows.append(win)

                gif_x += col_w
            gif_y += row_h

        return windows

    def fill_video(
        self,
        video_path: str,
        **kwargs: Any,
    ) -> list[Window]:
        """Fill the grid with a single video split across all cells.

        Each cell displays a portion of the video corresponding to its
        position in the grid, creating a tiled/split video effect.

        Args:
            video_path: Path to the video file
            **kwargs: Additional arguments passed to window()

        Returns:
            List of created windows
        """
        vid_w, vid_h = get_video_size(video_path)

        col_gap, row_gap = self.gap
        col_sizes = _compute_track_sizes(self._col_tracks, self._w, col_gap)
        row_sizes = _compute_track_sizes(self._row_tracks, self._h, row_gap)

        total_col = sum(col_sizes)
        total_row = sum(row_sizes)

        windows: list[Window] = []

        vid_y = 0.0
        for row in range(self.num_rows):
            vid_x = 0.0
            row_h = (row_sizes[row] / total_row) * vid_h

            for col in range(self.num_cols):
                col_w = (col_sizes[col] / total_col) * vid_w

                src_x = int(vid_x)
                src_y = int(vid_y)
                src_w = int(col_w)
                src_h = int(row_h)

                if col == self.num_cols - 1:
                    src_w = vid_w - src_x
                if row == self.num_rows - 1:
                    src_h = vid_h - src_y

                win = self.cell(row, col, video=video_path, **kwargs)
                win.video_region = (src_x, src_y, src_w, src_h)
                windows.append(win)

                vid_x += col_w
            vid_y += row_h

        return windows

    @overload
    def __getitem__(self, key: tuple[int, int]) -> Window: ...

    @overload
    def __getitem__(self, key: int) -> Window: ...

    def __getitem__(self, key: tuple[int, int] | int) -> Window:
        """Get a window by (row, col) tuple or linear index."""
        if isinstance(key, int):
            row = key // self.num_cols
            col = key % self.num_cols
            key = (row, col)

        if key not in self._windows:
            raise KeyError(f"No window at {key}")
        return self._windows[key]

    def __contains__(self, key: tuple[int, int] | int) -> bool:
        """Check if a cell has a window."""
        if isinstance(key, int):
            row = key // self.num_cols
            col = key % self.num_cols
            key = (row, col)
        return key in self._windows

    def __iter__(self) -> Iterator[Window]:
        """Iterate over windows in row-major order."""
        for row in range(self.num_rows):
            for col in range(self.num_cols):
                if (row, col) in self._windows:
                    yield self._windows[(row, col)]

    def __len__(self) -> int:
        """Number of windows in the grid."""
        return len(self._windows)

    def _update_all_windows(self) -> None:
        """Update all window positions and sizes based on current grid bounds."""
        for (row, col), win in self._windows.items():
            if win.closed:
                continue
            rowspan, colspan = self._spans.get((row, col), (1, 1))
            spec = self._compute_cell(row, col, rowspan, colspan)
            win.x = spec.x
            win.y = spec.y
            win.w = spec.w
            win.h = spec.h

    def move_to(self, x: float, y: float) -> None:
        """Move the grid to a new position (instant)."""
        self._x = float(x)
        self._y = float(y)
        self._update_all_windows()

    def resize_to(self, w: float, h: float) -> None:
        """Resize the grid (instant)."""
        self._w = float(w)
        self._h = float(h)
        self._update_all_windows()

    def animate_to(
        self,
        x: float,
        y: float,
        w: float,
        h: float,
        duration: float = 0.5,
        ease: str | EasingFunc = "ease_out",
    ) -> None:
        """Animate the grid to new position and size.

        All windows are animated in parallel to their new positions.
        """
        if duration <= 0:
            self._x = float(x)
            self._y = float(y)
            self._w = float(w)
            self._h = float(h)
            self._update_all_windows()
            return

        old_x, old_y, old_w, old_h = self._x, self._y, self._w, self._h

        self._x, self._y, self._w, self._h = float(x), float(y), float(w), float(h)

        targets: dict[tuple[int, int], CellSpec] = {}
        for (row, col), win in self._windows.items():
            if win.closed:
                continue
            rowspan, colspan = self._spans.get((row, col), (1, 1))
            targets[(row, col)] = self._compute_cell(row, col, rowspan, colspan)

        self._x, self._y, self._w, self._h = old_x, old_y, old_w, old_h

        ease_func = get_easing(ease)
        animations = []

        for (row, col), win in self._windows.items():
            if win.closed:
                continue
            target = targets[(row, col)]
            animations.append(move_async(win, target.x, target.y, duration, ease_func))
            animations.append(resize_async(win, target.w, target.h, duration, ease_func))

        if animations:
            _run_animation(_parallel_gen(animations))

        self._x, self._y, self._w, self._h = float(x), float(y), float(w), float(h)

    def swap(self, r1: int, c1: int, r2: int, c2: int) -> None:
        """Swap two cells instantly."""
        key1 = (r1, c1)
        key2 = (r2, c2)

        win1 = self._windows.get(key1)
        win2 = self._windows.get(key2)
        span1 = self._spans.get(key1, (1, 1))
        span2 = self._spans.get(key2, (1, 1))

        if win1 and win2:
            self._windows[key1] = win2
            self._windows[key2] = win1
            self._spans[key1] = span2
            self._spans[key2] = span1
        elif win1:
            del self._windows[key1]
            self._windows[key2] = win1
            if key1 in self._spans:
                del self._spans[key1]
            self._spans[key2] = span1
        elif win2:
            del self._windows[key2]
            self._windows[key1] = win2
            if key2 in self._spans:
                del self._spans[key2]
            self._spans[key1] = span2

        self._update_all_windows()

    def swap_animated(
        self,
        r1: int,
        c1: int,
        r2: int,
        c2: int,
        duration: float = 0.3,
        ease: str | EasingFunc = "ease_in_out",
    ) -> None:
        """Swap two cells with animation."""
        key1 = (r1, c1)
        key2 = (r2, c2)

        win1 = self._windows.get(key1)
        win2 = self._windows.get(key2)
        span1 = self._spans.get(key1, (1, 1))
        span2 = self._spans.get(key2, (1, 1))

        if not win1 and not win2:
            return

        if duration <= 0:
            self.swap(r1, c1, r2, c2)
            return

        spec1 = self._compute_cell(r1, c1, span2[0], span2[1]) if win2 else self._compute_cell(r1, c1, 1, 1)
        spec2 = self._compute_cell(r2, c2, span1[0], span1[1]) if win1 else self._compute_cell(r2, c2, 1, 1)

        ease_func = get_easing(ease)
        animations = []

        if win1 and not win1.closed:
            animations.append(move_async(win1, spec2.x, spec2.y, duration, ease_func))
            if span1 != span2:
                animations.append(resize_async(win1, spec2.w, spec2.h, duration, ease_func))

        if win2 and not win2.closed:
            animations.append(move_async(win2, spec1.x, spec1.y, duration, ease_func))
            if span1 != span2:
                animations.append(resize_async(win2, spec1.w, spec1.h, duration, ease_func))

        if animations:
            _run_animation(_parallel_gen(animations))

        if win1 and win2:
            self._windows[key1] = win2
            self._windows[key2] = win1
            self._spans[key1] = span2
            self._spans[key2] = span1
        elif win1:
            del self._windows[key1]
            self._windows[key2] = win1
            if key1 in self._spans:
                del self._spans[key1]
            self._spans[key2] = span1
        elif win2:
            del self._windows[key2]
            self._windows[key1] = win2
            if key2 in self._spans:
                del self._spans[key2]
            self._spans[key1] = span2

    def clear(self) -> None:
        """Close all windows in the grid."""
        for win in self._windows.values():
            if not win.closed:
                win.close()
        self._windows.clear()
        self._spans.clear()

    def __repr__(self) -> str:
        return (
            f"Grid(x={self._x}, y={self._y}, w={self._w}, h={self._h}, "
            f"columns={self._columns!r}, rows={self._rows!r}, "
            f"windows={len(self._windows)})"
        )


def grid(
    x: float,
    y: float,
    w: float,
    h: float,
    columns: str = "1fr",
    rows: str = "1fr",
    gap: float | tuple[float, float] = 0,
) -> Grid:
    """Create a new grid layout.

    Module-level convenience function.

    Args:
        x, y: Grid origin position
        w, h: Grid total size
        columns: Column template (e.g., "1fr 2fr 100px")
        rows: Row template (e.g., "100px 1fr 1fr")
        gap: Gap between cells (single value or (column_gap, row_gap))

    Returns:
        A new Grid instance
    """
    return Grid(x, y, w, h, columns, rows, gap)
