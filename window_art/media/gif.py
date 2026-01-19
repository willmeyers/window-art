"""GIF animation support using Pillow."""
from __future__ import annotations

import ctypes
from typing import Any

_HAS_PIL = False
_Image: Any = None
try:
    from PIL import Image

    _Image = Image
    _HAS_PIL = True
except ImportError:
    pass

_sdl2: Any = None
try:
    import sdl2

    _sdl2 = sdl2
except ImportError:
    pass


def has_gif_support() -> bool:
    """Check if GIF animation support is available."""
    return _HAS_PIL and _sdl2 is not None


class GifAnimation:
    """Manages an animated GIF with frame extraction and timing."""

    def __init__(self, path: str) -> None:
        """Load an animated GIF from a file path.

        Args:
            path: Path to the GIF file

        Raises:
            ImportError: If Pillow is not available
            ValueError: If the file cannot be loaded
        """
        if not _HAS_PIL or _Image is None:
            raise ImportError(
                "Pillow is required for GIF support. "
                "Install it with: pip install Pillow"
            )

        self._path = path
        self._frames: list[bytes] = []
        self._delays: list[float] = []
        self._width = 0
        self._height = 0
        self._current_frame = 0
        self._elapsed = 0.0
        self._playing = True
        self._loop = True
        self._speed = 1.0

        self._load_gif(path)

    def _load_gif(self, path: str) -> None:
        """Load and extract all frames from a GIF."""
        try:
            img = _Image.open(path)
        except Exception as e:
            raise ValueError(f"Failed to load GIF '{path}': {e}")

        self._width = img.width
        self._height = img.height

        try:
            frame_idx = 0
            while True:
                img.seek(frame_idx)

                frame = img.convert("RGBA")

                self._frames.append(frame.tobytes())

                delay_ms = img.info.get("duration", 100)
                self._delays.append(delay_ms / 1000.0)

                frame_idx += 1
        except EOFError:
            pass

        if not self._frames:
            raise ValueError(f"No frames found in GIF '{path}'")

    @property
    def path(self) -> str:
        """Path to the GIF file."""
        return self._path

    @property
    def width(self) -> int:
        """Width of the GIF in pixels."""
        return self._width

    @property
    def height(self) -> int:
        """Height of the GIF in pixels."""
        return self._height

    @property
    def size(self) -> tuple[int, int]:
        """Size of the GIF as (width, height)."""
        return (self._width, self._height)

    @property
    def frame_count(self) -> int:
        """Total number of frames in the animation."""
        return len(self._frames)

    @property
    def current_frame(self) -> int:
        """Current frame index (0-based)."""
        return self._current_frame

    @current_frame.setter
    def current_frame(self, value: int) -> None:
        """Set the current frame index."""
        self._current_frame = max(0, min(value, len(self._frames) - 1))

    @property
    def playing(self) -> bool:
        """Whether the animation is playing."""
        return self._playing

    @playing.setter
    def playing(self, value: bool) -> None:
        self._playing = value

    @property
    def loop(self) -> bool:
        """Whether the animation loops."""
        return self._loop

    @loop.setter
    def loop(self, value: bool) -> None:
        self._loop = value

    @property
    def speed(self) -> float:
        """Playback speed multiplier (1.0 = normal)."""
        return self._speed

    @speed.setter
    def speed(self, value: float) -> None:
        self._speed = max(0.1, value)

    @property
    def total_duration(self) -> float:
        """Total duration of one loop in seconds."""
        return sum(self._delays)

    def update(self, dt: float) -> bool:
        """Update animation state. Returns True if frame changed.

        Args:
            dt: Delta time in seconds since last update
        """
        if not self._playing or len(self._frames) <= 1:
            return False

        old_frame = self._current_frame
        self._elapsed += dt * self._speed

        while self._elapsed >= self._delays[self._current_frame]:
            self._elapsed -= self._delays[self._current_frame]
            self._current_frame += 1

            if self._current_frame >= len(self._frames):
                if self._loop:
                    self._current_frame = 0
                else:
                    self._current_frame = len(self._frames) - 1
                    self._playing = False
                    break

        return self._current_frame != old_frame

    def get_frame_data(self, frame: int | None = None) -> bytes:
        """Get raw RGBA data for a frame.

        Args:
            frame: Frame index, or None for current frame
        """
        if frame is None:
            frame = self._current_frame
        return self._frames[frame]

    def get_frame_delay(self, frame: int | None = None) -> float:
        """Get delay for a frame in seconds.

        Args:
            frame: Frame index, or None for current frame
        """
        if frame is None:
            frame = self._current_frame
        return self._delays[frame]

    def reset(self) -> None:
        """Reset animation to the first frame."""
        self._current_frame = 0
        self._elapsed = 0.0
        self._playing = True

    def create_texture(self, renderer: Any, frame: int | None = None) -> Any:
        """Create an SDL texture from a frame.

        Args:
            renderer: SDL renderer to create texture for
            frame: Frame index, or None for current frame

        Returns:
            SDL_Texture pointer
        """
        if _sdl2 is None:
            raise ImportError("SDL2 is required")

        if frame is None:
            frame = self._current_frame

        data = self._frames[frame]

        rmask = 0x000000FF
        gmask = 0x0000FF00
        bmask = 0x00FF0000
        amask = 0xFF000000

        surface = _sdl2.SDL_CreateRGBSurfaceFrom(
            ctypes.c_char_p(data),
            self._width,
            self._height,
            32,
            self._width * 4,
            rmask,
            gmask,
            bmask,
            amask,
        )

        if not surface:
            raise RuntimeError(f"Failed to create surface: {_sdl2.SDL_GetError()}")

        texture = _sdl2.SDL_CreateTextureFromSurface(renderer, surface)
        _sdl2.SDL_FreeSurface(surface)

        if not texture:
            raise RuntimeError(f"Failed to create texture: {_sdl2.SDL_GetError()}")

        return texture


def get_gif_size(path: str) -> tuple[int, int]:
    """Get dimensions of a GIF without fully loading it.

    Args:
        path: Path to the GIF file

    Returns:
        Tuple of (width, height)
    """
    if not _HAS_PIL or _Image is None:
        raise ImportError(
            "Pillow is required for GIF support. "
            "Install it with: pip install Pillow"
        )

    with _Image.open(path) as img:
        return (img.width, img.height)


def get_gif_info(path: str) -> dict[str, Any]:
    """Get information about a GIF file.

    Args:
        path: Path to the GIF file

    Returns:
        Dictionary with width, height, frame_count, total_duration
    """
    gif = GifAnimation(path)
    return {
        "width": gif.width,
        "height": gif.height,
        "frame_count": gif.frame_count,
        "total_duration": gif.total_duration,
    }


__all__ = ["GifAnimation", "has_gif_support", "get_gif_size", "get_gif_info"]
