"""
window_art - A minimal Python library for live coding visual scenes using desktop windows.

Simple example:
    import window_art as wa

    wa.init()
    win = wa.window(100, 100, 200, 200, color="red")
    wa.move(win, 500, 300, duration=2.0)
    wa.run()

Context manager example:
    import window_art as wa

    with wa.run():
        win = wa.window(100, 100, 200, 200, color="blue")
        wa.move(win, 500, 300, duration=2.0, ease="ease_out")
"""

from __future__ import annotations

from contextlib import contextmanager
from typing import Generator

from .color import Color, ColorLike
from .vec import vec2
from .window import Window

from .core import (
    Desktop,
    Screen,
    clear,
    delta_time,
    get_time,
    init,
    primary_screen,
    quit,
    run_context,
    screens,
    stop,
    update,
    window,
    windows,
)
from .core import run as _run

from .animate import (
    Animation,
    color_async,
    color_to,
    fade,
    fade_async,
    fade_in,
    fade_out,
    move,
    move_all,
    move_async,
    move_by,
    parallel,
    parallel_async,
    resize,
    resize_async,
    resize_by,
    run_animation,
    sequence,
    sequence_async,
    wait,
)

from .media import (
    GifAnimation,
    TextRenderer,
    VideoPlayer,
    get_gif_info,
    get_gif_size,
    get_image_size,
    get_text_size,
    get_video_info,
    get_video_size,
    has_gif_support,
    has_image_support,
    has_text_support,
    has_video_support,
    load_image,
)

from .layout import CellSpec, Grid, TrackSize, grid, grid_layout

from .easing import (
    EASING_FUNCTIONS,
    EasingFunc,
    ease_in,
    ease_in_back,
    ease_in_bounce,
    ease_in_circ,
    ease_in_cubic,
    ease_in_elastic,
    ease_in_expo,
    ease_in_out,
    ease_in_out_back,
    ease_in_out_bounce,
    ease_in_out_circ,
    ease_in_out_cubic,
    ease_in_out_elastic,
    ease_in_out_expo,
    ease_in_out_quad,
    ease_in_out_quart,
    ease_in_out_quint,
    ease_in_out_sine,
    ease_in_quad,
    ease_in_quart,
    ease_in_quint,
    ease_in_sine,
    ease_out,
    ease_out_back,
    ease_out_bounce,
    ease_out_circ,
    ease_out_cubic,
    ease_out_elastic,
    ease_out_expo,
    ease_out_quad,
    ease_out_quart,
    ease_out_quint,
    ease_out_sine,
    get_easing,
    linear,
)


@contextmanager
def run(fps: float = 60.0) -> Generator[None, None, None]:
    """
    Context manager for running window_art.

    Usage:
        with wa.run():
            win = wa.window(100, 100, 200, 200, color="red")
            wa.move(win, 500, 300, duration=2.0)
    """
    init()
    try:
        yield
    finally:
        quit()


def run_loop(fps: float = 60.0) -> None:
    """Run the main event loop (blocking)."""
    _run(fps)


__version__ = "0.1.0"

__all__ = [
    "__version__",
    "Color",
    "ColorLike",
    "vec2",
    "Window",
    "Screen",
    "Desktop",
    "Animation",
    "EasingFunc",
    "Grid",
    "CellSpec",
    "TrackSize",
    "load_image",
    "has_image_support",
    "get_image_size",
    "GifAnimation",
    "has_gif_support",
    "get_gif_size",
    "get_gif_info",
    "VideoPlayer",
    "has_video_support",
    "get_video_size",
    "get_video_info",
    "TextRenderer",
    "has_text_support",
    "get_text_size",
    "grid",
    "grid_layout",
    "init",
    "quit",
    "window",
    "windows",
    "clear",
    "screens",
    "primary_screen",
    "update",
    "run",
    "run_loop",
    "run_context",
    "stop",
    "delta_time",
    "get_time",
    "move",
    "move_by",
    "move_all",
    "resize",
    "resize_by",
    "fade",
    "fade_in",
    "fade_out",
    "color_to",
    "wait",
    "parallel",
    "sequence",
    "run_animation",
    "move_async",
    "resize_async",
    "fade_async",
    "color_async",
    "parallel_async",
    "sequence_async",
    "linear",
    "ease_in",
    "ease_out",
    "ease_in_out",
    "ease_in_quad",
    "ease_out_quad",
    "ease_in_out_quad",
    "ease_in_cubic",
    "ease_out_cubic",
    "ease_in_out_cubic",
    "ease_in_quart",
    "ease_out_quart",
    "ease_in_out_quart",
    "ease_in_quint",
    "ease_out_quint",
    "ease_in_out_quint",
    "ease_in_sine",
    "ease_out_sine",
    "ease_in_out_sine",
    "ease_in_expo",
    "ease_out_expo",
    "ease_in_out_expo",
    "ease_in_circ",
    "ease_out_circ",
    "ease_in_out_circ",
    "ease_in_back",
    "ease_out_back",
    "ease_in_out_back",
    "ease_in_elastic",
    "ease_out_elastic",
    "ease_in_out_elastic",
    "ease_in_bounce",
    "ease_out_bounce",
    "ease_in_out_bounce",
    "get_easing",
    "EASING_FUNCTIONS",
]
