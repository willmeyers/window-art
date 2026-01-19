"""Animation engine with immediate-mode API."""
from __future__ import annotations

import time
from typing import Callable, Generator, Sequence

from .color import Color, ColorLike
from .core import Desktop
from .easing import EasingFunc, get_easing, linear
from .window import Window

Animation = Generator[None, None, None]


def _run_animation(animation: Animation) -> None:
    """Run an animation to completion, processing frames."""
    desktop = Desktop.get()
    desktop.init()

    frame_time = 1.0 / 60.0

    try:
        while True:
            frame_start = time.perf_counter()

            if not desktop.update():
                break

            try:
                next(animation)
            except StopIteration:
                break

            elapsed = time.perf_counter() - frame_start
            if elapsed < frame_time:
                time.sleep(frame_time - elapsed)
    except GeneratorExit:
        pass


def _lerp(a: float, b: float, t: float) -> float:
    """Linear interpolation between two values."""
    return a + (b - a) * t


def _move_gen(
    win: Window,
    x: float,
    y: float,
    duration: float,
    ease: EasingFunc,
) -> Animation:
    """Generator that animates window position."""
    start_x, start_y = win.x, win.y
    start_time = time.perf_counter()

    while True:
        elapsed = time.perf_counter() - start_time
        if elapsed >= duration:
            win.x = x
            win.y = y
            return

        t = ease(elapsed / duration)
        win.x = _lerp(start_x, x, t)
        win.y = _lerp(start_y, y, t)
        yield


def _resize_gen(
    win: Window,
    w: float,
    h: float,
    duration: float,
    ease: EasingFunc,
) -> Animation:
    """Generator that animates window size."""
    start_w, start_h = win.w, win.h
    start_time = time.perf_counter()

    while True:
        elapsed = time.perf_counter() - start_time
        if elapsed >= duration:
            win.w = w
            win.h = h
            return

        t = ease(elapsed / duration)
        win.w = _lerp(start_w, w, t)
        win.h = _lerp(start_h, h, t)
        yield


def _fade_gen(
    win: Window,
    opacity: float,
    duration: float,
    ease: EasingFunc,
) -> Animation:
    """Generator that animates window opacity."""
    start_opacity = win.opacity
    start_time = time.perf_counter()

    while True:
        elapsed = time.perf_counter() - start_time
        if elapsed >= duration:
            win.opacity = opacity
            return

        t = ease(elapsed / duration)
        win.opacity = _lerp(start_opacity, opacity, t)
        yield


def _color_gen(
    win: Window,
    color: Color,
    duration: float,
    ease: EasingFunc,
) -> Animation:
    """Generator that animates window color."""
    start_color = win.color
    start_time = time.perf_counter()

    while True:
        elapsed = time.perf_counter() - start_time
        if elapsed >= duration:
            win.color = color
            return

        t = ease(elapsed / duration)
        win.color = start_color.lerp(color, t)
        yield


def _parallel_gen(animations: list[Animation]) -> Animation:
    """Generator that runs multiple animations in parallel."""
    active = list(animations)

    while active:
        still_active = []
        for anim in active:
            try:
                next(anim)
                still_active.append(anim)
            except StopIteration:
                pass
        active = still_active
        yield


def _sequence_gen(animations: list[Animation]) -> Animation:
    """Generator that runs animations in sequence."""
    for anim in animations:
        yield from anim


def _wait_gen(duration: float) -> Animation:
    """Generator that waits for a duration."""
    start_time = time.perf_counter()

    while time.perf_counter() - start_time < duration:
        yield


def move(
    win: Window,
    x: float,
    y: float,
    duration: float = 0.0,
    ease: str | EasingFunc = linear,
) -> None:
    """Move a window to a position. Blocks until complete."""
    if duration <= 0:
        win.x = x
        win.y = y
        return
    _run_animation(_move_gen(win, x, y, duration, get_easing(ease)))


def resize(
    win: Window,
    w: float,
    h: float,
    duration: float = 0.0,
    ease: str | EasingFunc = linear,
) -> None:
    """Resize a window. Blocks until complete."""
    if duration <= 0:
        win.w = w
        win.h = h
        return
    _run_animation(_resize_gen(win, w, h, duration, get_easing(ease)))


def fade(
    win: Window,
    opacity: float,
    duration: float = 0.0,
    ease: str | EasingFunc = linear,
) -> None:
    """Fade a window to an opacity. Blocks until complete."""
    if duration <= 0:
        win.opacity = opacity
        return
    _run_animation(_fade_gen(win, opacity, duration, get_easing(ease)))


def fade_in(
    win: Window,
    duration: float = 0.5,
    ease: str | EasingFunc = linear,
) -> None:
    """Fade in a window from 0 opacity. Blocks until complete."""
    win.opacity = 0.0
    fade(win, 1.0, duration, ease)


def fade_out(
    win: Window,
    duration: float = 0.5,
    ease: str | EasingFunc = linear,
) -> None:
    """Fade out a window to 0 opacity. Blocks until complete."""
    fade(win, 0.0, duration, ease)


def color_to(
    win: Window,
    color: ColorLike,
    duration: float = 0.0,
    ease: str | EasingFunc = linear,
) -> None:
    """Animate window color. Blocks until complete."""
    target = Color.parse(color)
    if duration <= 0:
        win.color = target
        return
    _run_animation(_color_gen(win, target, duration, get_easing(ease)))


def move_all(
    windows: Sequence[Window],
    x: float,
    y: float,
    duration: float = 0.0,
    ease: str | EasingFunc = linear,
) -> None:
    """Move multiple windows to the same position. Blocks until complete."""
    if duration <= 0:
        for win in windows:
            win.x = x
            win.y = y
        return

    ease_func = get_easing(ease)
    animations = [_move_gen(win, x, y, duration, ease_func) for win in windows]
    _run_animation(_parallel_gen(animations))


def move_by(
    win: Window,
    dx: float,
    dy: float,
    duration: float = 0.0,
    ease: str | EasingFunc = linear,
) -> None:
    """Move a window by a relative amount. Blocks until complete."""
    move(win, win.x + dx, win.y + dy, duration, ease)


def resize_by(
    win: Window,
    dw: float,
    dh: float,
    duration: float = 0.0,
    ease: str | EasingFunc = linear,
) -> None:
    """Resize a window by a relative amount. Blocks until complete."""
    resize(win, win.w + dw, win.h + dh, duration, ease)


def wait(duration: float) -> None:
    """Wait for a duration while processing events. Blocks until complete."""
    _run_animation(_wait_gen(duration))


def parallel(*funcs: Callable[[], None]) -> None:
    """
    Run multiple animation functions in parallel.

    Usage:
        parallel(
            lambda: move(win1, 100, 100, 1.0),
            lambda: move(win2, 200, 200, 1.0),
        )
    """
    desktop = Desktop.get()
    desktop.init()

    import threading

    threads: list[threading.Thread] = []
    for func in funcs:
        t = threading.Thread(target=func)
        t.start()
        threads.append(t)

    for t in threads:
        t.join()


def sequence(*funcs: Callable[[], None]) -> None:
    """
    Run animation functions in sequence.

    Usage:
        sequence(
            lambda: move(win, 100, 100, 1.0),
            lambda: move(win, 200, 200, 1.0),
        )
    """
    for func in funcs:
        func()


def move_async(
    win: Window,
    x: float,
    y: float,
    duration: float,
    ease: str | EasingFunc = linear,
) -> Animation:
    """Create a move animation generator (non-blocking)."""
    return _move_gen(win, x, y, duration, get_easing(ease))


def resize_async(
    win: Window,
    w: float,
    h: float,
    duration: float,
    ease: str | EasingFunc = linear,
) -> Animation:
    """Create a resize animation generator (non-blocking)."""
    return _resize_gen(win, w, h, duration, get_easing(ease))


def fade_async(
    win: Window,
    opacity: float,
    duration: float,
    ease: str | EasingFunc = linear,
) -> Animation:
    """Create a fade animation generator (non-blocking)."""
    return _fade_gen(win, opacity, duration, get_easing(ease))


def color_async(
    win: Window,
    color: ColorLike,
    duration: float,
    ease: str | EasingFunc = linear,
) -> Animation:
    """Create a color animation generator (non-blocking)."""
    return _color_gen(win, Color.parse(color), duration, get_easing(ease))


def parallel_async(*animations: Animation) -> Animation:
    """Combine multiple animation generators to run in parallel."""
    return _parallel_gen(list(animations))


def sequence_async(*animations: Animation) -> Animation:
    """Combine multiple animation generators to run in sequence."""
    return _sequence_gen(list(animations))


def run_animation(animation: Animation) -> None:
    """Run an animation generator to completion."""
    _run_animation(animation)
