"""Desktop singleton, SDL initialization, and event loop."""
from __future__ import annotations

import os
import signal
import sys
import time
from contextlib import contextmanager
from dataclasses import dataclass
from types import FrameType
from typing import Callable, Generator, Iterator

if sys.platform == "darwin":
    _stderr_fd = sys.stderr.fileno()
    _devnull_fd = os.open(os.devnull, os.O_WRONLY)
    _saved_stderr = os.dup(_stderr_fd)
    os.dup2(_devnull_fd, _stderr_fd)

import sdl2
import sdl2.ext

if sys.platform == "darwin":
    os.dup2(_saved_stderr, _stderr_fd)
    os.close(_saved_stderr)
    os.close(_devnull_fd)

from .color import ColorLike
from .window import PaddingLike, Window


@dataclass
class Screen:
    """Information about a display screen."""

    x: int
    y: int
    w: int
    h: int
    index: int

    @property
    def width(self) -> int:
        return self.w

    @property
    def height(self) -> int:
        return self.h

    @property
    def center(self) -> tuple[int, int]:
        return (self.x + self.w // 2, self.y + self.h // 2)


class Desktop:
    """Singleton managing SDL, windows, and the event loop."""

    _instance: Desktop | None = None

    def __init__(self) -> None:
        self._initialized = False
        self._windows: list[Window] = []
        self._running = False
        self._stop_requested = False
        self._last_update_time: float = 0.0
        self._delta_time: float = 0.0
        self._frame_count: int = 0
        self._original_sigint_handler: Callable[[int, FrameType | None], None] | int | None = None

    @classmethod
    def get(cls) -> Desktop:
        """Get the singleton Desktop instance."""
        if cls._instance is None:
            cls._instance = Desktop()
        return cls._instance

    def _sigint_handler(self, signum: int, frame: FrameType | None) -> None:
        """Handle Ctrl+C by stopping the event loop."""
        self._stop_requested = True
        self._running = False

    def init(self) -> None:
        """Initialize SDL2."""
        if self._initialized:
            return

        sdl2.SDL_SetHint(sdl2.SDL_HINT_NO_SIGNAL_HANDLERS, b"1")

        if sdl2.SDL_Init(sdl2.SDL_INIT_VIDEO) != 0:
            raise RuntimeError(f"SDL2 initialization failed: {sdl2.SDL_GetError()}")

        self._original_sigint_handler = signal.signal(signal.SIGINT, self._sigint_handler)
        signal.siginterrupt(signal.SIGINT, True)

        self._initialized = True
        self._stop_requested = False
        self._last_update_time = time.perf_counter()

    def quit(self) -> None:
        """Clean up SDL2 and all windows."""
        if not self._initialized:
            return

        if self._original_sigint_handler is not None:
            signal.signal(signal.SIGINT, self._original_sigint_handler)
            self._original_sigint_handler = None

        for win in list(self._windows):
            win.close()
        self._windows.clear()

        sdl2.SDL_Quit()
        self._initialized = False
        Desktop._instance = None

    def window(
        self,
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
        text: str | None = None,
        font: str = "Arial",
        font_size: int = 24,
        text_color: ColorLike = "black",
        text_align: str = "center",
        text_valign: str = "center",
        text_wrap: bool = False,
        text_padding: PaddingLike = 0,
    ) -> Window:
        """Create a new window."""
        self.init()
        win = Window(
            self, x, y, w, h, color, opacity,
            borderless=borderless,
            always_on_top=always_on_top,
            resizable=resizable,
            title=title,
            shadow=shadow,
            image=image,
            gif=gif,
            video=video,
            text=text,
            font=font,
            font_size=font_size,
            text_color=text_color,
            text_align=text_align,
            text_valign=text_valign,
            text_wrap=text_wrap,
            text_padding=text_padding,
        )
        self._windows.append(win)
        return win

    def _remove_window(self, win: Window) -> None:
        """Remove a window from tracking (called by Window.close)."""
        if win in self._windows:
            self._windows.remove(win)

    def windows(self) -> list[Window]:
        """Get all active windows."""
        return list(self._windows)

    def clear(self) -> None:
        """Close all windows."""
        for win in list(self._windows):
            win.close()

    def screens(self) -> list[Screen]:
        """Get information about all screens."""
        self.init()
        result = []
        num_displays = sdl2.SDL_GetNumVideoDisplays()
        for i in range(num_displays):
            bounds = sdl2.SDL_Rect()
            if sdl2.SDL_GetDisplayBounds(i, bounds) == 0:
                result.append(Screen(bounds.x, bounds.y, bounds.w, bounds.h, i))
        return result

    def primary_screen(self) -> Screen | None:
        """Get the primary screen."""
        screens = self.screens()
        return screens[0] if screens else None

    def update(self) -> bool:
        """Process one frame. Returns False if quit was requested or Ctrl+C pressed."""
        self.init()

        if self._stop_requested:
            return False

        self._running = True

        current_time = time.perf_counter()
        self._delta_time = current_time - self._last_update_time
        self._last_update_time = current_time
        self._frame_count += 1

        event = sdl2.SDL_Event()
        while sdl2.SDL_PollEvent(event):
            if event.type == sdl2.SDL_QUIT:
                return False
            if event.type == sdl2.SDL_KEYDOWN:
                if event.key.keysym.sym == sdl2.SDLK_ESCAPE:
                    return False
                if event.key.keysym.sym == sdl2.SDLK_c and (event.key.keysym.mod & sdl2.KMOD_CTRL):
                    return False

        for win in self._windows:
            if not win.closed:
                win._apply_changes(self._delta_time)

        return not self._stop_requested

    def run(self, fps: float = 60.0) -> None:
        """Run the main event loop."""
        self.init()
        self._running = True
        frame_time = 1.0 / fps

        try:
            while self._running:
                frame_start = time.perf_counter()

                if not self.update():
                    break

                elapsed = time.perf_counter() - frame_start
                if elapsed < frame_time:
                    time.sleep(frame_time - elapsed)
        finally:
            self._running = False

    def stop(self) -> None:
        """Stop the main event loop."""
        self._stop_requested = True
        self._running = False

    @property
    def delta_time(self) -> float:
        """Time since last update in seconds."""
        return self._delta_time

    @property
    def time(self) -> float:
        """Current time in seconds since init."""
        if not self._initialized:
            return 0.0
        return time.perf_counter()

    @property
    def frame_count(self) -> int:
        """Number of frames processed."""
        return self._frame_count

    @property
    def running(self) -> bool:
        """Whether the main loop is running."""
        return self._running


@contextmanager
def run_context(fps: float = 60.0) -> Generator[Desktop, None, None]:
    """Context manager for running desktop_windows."""
    desktop = Desktop.get()
    desktop.init()
    try:
        yield desktop
    finally:
        desktop.quit()


def init() -> None:
    """Initialize the desktop window system."""
    Desktop.get().init()


def quit() -> None:
    """Clean up and quit."""
    Desktop.get().quit()


def window(
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
    text: str | None = None,
    font: str = "Arial",
    font_size: int = 24,
    text_color: ColorLike = "black",
    text_align: str = "center",
    text_valign: str = "center",
    text_wrap: bool = False,
    text_padding: PaddingLike = 0,
) -> Window:
    """Create a new window."""
    return Desktop.get().window(
        x, y, w, h, color, opacity,
        borderless=borderless,
        always_on_top=always_on_top,
        resizable=resizable,
        title=title,
        shadow=shadow,
        image=image,
        gif=gif,
        video=video,
        text=text,
        font=font,
        font_size=font_size,
        text_color=text_color,
        text_align=text_align,
        text_valign=text_valign,
        text_wrap=text_wrap,
        text_padding=text_padding,
    )


def windows() -> list[Window]:
    """Get all active windows."""
    return Desktop.get().windows()


def clear() -> None:
    """Close all windows."""
    Desktop.get().clear()


def screens() -> list[Screen]:
    """Get information about all screens."""
    return Desktop.get().screens()


def primary_screen() -> Screen | None:
    """Get the primary screen."""
    return Desktop.get().primary_screen()


def update() -> bool:
    """Process one frame."""
    return Desktop.get().update()


def run(fps: float = 60.0) -> None:
    """Run the main event loop."""
    Desktop.get().run(fps)


def stop() -> None:
    """Stop the main event loop."""
    Desktop.get().stop()


def delta_time() -> float:
    """Get time since last update."""
    return Desktop.get().delta_time


def get_time() -> float:
    """Get current time."""
    return Desktop.get().time
