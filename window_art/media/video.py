"""Video playback support using OpenCV."""
from __future__ import annotations

import ctypes
from typing import Any

_HAS_CV2 = False
_cv2: Any = None
_np: Any = None
try:
    import cv2
    import numpy as np

    _cv2 = cv2
    _np = np
    _HAS_CV2 = True
except ImportError:
    pass

_sdl2: Any = None
try:
    import sdl2

    _sdl2 = sdl2
except ImportError:
    pass


def has_video_support() -> bool:
    """Check if video playback support is available."""
    return _HAS_CV2 and _sdl2 is not None


class VideoPlayer:
    """Manages video playback with frame extraction."""

    def __init__(self, path: str) -> None:
        """Load a video from a file path.

        Args:
            path: Path to the video file (MP4, AVI, etc.)

        Raises:
            ImportError: If OpenCV is not available
            ValueError: If the file cannot be loaded
        """
        if not _HAS_CV2 or _cv2 is None:
            raise ImportError(
                "OpenCV is required for video support. "
                "Install it with: pip install opencv-python"
            )

        self._path = path
        self._cap: Any = None
        self._width = 0
        self._height = 0
        self._fps = 0.0
        self._frame_count = 0
        self._duration = 0.0
        self._current_frame = 0
        self._current_time = 0.0
        self._elapsed = 0.0
        self._playing = True
        self._loop = True
        self._speed = 1.0
        self._frame_data: bytes | None = None

        self._load_video(path)

    def _load_video(self, path: str) -> None:
        """Open the video file and extract metadata."""
        self._cap = _cv2.VideoCapture(path)

        if not self._cap.isOpened():
            raise ValueError(f"Failed to open video '{path}'")

        self._width = int(self._cap.get(_cv2.CAP_PROP_FRAME_WIDTH))
        self._height = int(self._cap.get(_cv2.CAP_PROP_FRAME_HEIGHT))
        self._fps = self._cap.get(_cv2.CAP_PROP_FPS) or 30.0
        self._frame_count = int(self._cap.get(_cv2.CAP_PROP_FRAME_COUNT))
        self._duration = self._frame_count / self._fps if self._fps > 0 else 0.0

        self._read_current_frame()

    def _read_current_frame(self) -> bool:
        """Read the current frame into memory. Returns True if successful."""
        if self._cap is None or _cv2 is None or _np is None:
            return False

        ret, frame = self._cap.read()
        if not ret:
            return False

        frame_rgba = _cv2.cvtColor(frame, _cv2.COLOR_BGR2RGBA)
        self._frame_data = frame_rgba.tobytes()
        return True

    @property
    def path(self) -> str:
        """Path to the video file."""
        return self._path

    @property
    def width(self) -> int:
        """Width of the video in pixels."""
        return self._width

    @property
    def height(self) -> int:
        """Height of the video in pixels."""
        return self._height

    @property
    def size(self) -> tuple[int, int]:
        """Size of the video as (width, height)."""
        return (self._width, self._height)

    @property
    def fps(self) -> float:
        """Frames per second of the video."""
        return self._fps

    @property
    def frame_count(self) -> int:
        """Total number of frames in the video."""
        return self._frame_count

    @property
    def duration(self) -> float:
        """Total duration of the video in seconds."""
        return self._duration

    @property
    def current_frame(self) -> int:
        """Current frame index (0-based)."""
        return self._current_frame

    @current_frame.setter
    def current_frame(self, value: int) -> None:
        """Seek to a specific frame."""
        if self._cap is None or _cv2 is None:
            return

        value = max(0, min(value, self._frame_count - 1))
        self._cap.set(_cv2.CAP_PROP_POS_FRAMES, value)
        self._current_frame = value
        self._current_time = value / self._fps if self._fps > 0 else 0.0
        self._elapsed = 0.0
        self._read_current_frame()

    @property
    def current_time(self) -> float:
        """Current playback time in seconds."""
        return self._current_time

    @current_time.setter
    def current_time(self, value: float) -> None:
        """Seek to a specific time in seconds."""
        if self._fps > 0:
            self.current_frame = int(value * self._fps)

    @property
    def playing(self) -> bool:
        """Whether the video is playing."""
        return self._playing

    @playing.setter
    def playing(self, value: bool) -> None:
        self._playing = value

    @property
    def loop(self) -> bool:
        """Whether the video loops."""
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

    def update(self, dt: float) -> bool:
        """Update video state. Returns True if frame changed.

        Args:
            dt: Delta time in seconds since last update
        """
        if not self._playing or self._cap is None:
            return False

        self._elapsed += dt * self._speed
        frame_duration = 1.0 / self._fps if self._fps > 0 else 1.0 / 30.0

        if self._elapsed < frame_duration:
            return False

        frames_to_advance = int(self._elapsed / frame_duration)
        self._elapsed -= frames_to_advance * frame_duration

        old_frame = self._current_frame
        self._current_frame += frames_to_advance
        self._current_time = self._current_frame / self._fps if self._fps > 0 else 0.0

        if self._current_frame >= self._frame_count:
            if self._loop:
                self._current_frame = self._current_frame % self._frame_count
                self._cap.set(_cv2.CAP_PROP_POS_FRAMES, self._current_frame)
                self._current_time = self._current_frame / self._fps if self._fps > 0 else 0.0
            else:
                self._current_frame = self._frame_count - 1
                self._current_time = self._duration
                self._playing = False
                return old_frame != self._current_frame

        if frames_to_advance > 1:
            self._cap.set(_cv2.CAP_PROP_POS_FRAMES, self._current_frame)

        self._read_current_frame()
        return True

    def get_frame_data(self) -> bytes | None:
        """Get raw RGBA data for the current frame."""
        return self._frame_data

    def reset(self) -> None:
        """Reset video to the beginning."""
        self.current_frame = 0
        self._playing = True

    def create_texture(self, renderer: Any) -> Any:
        """Create an SDL texture from the current frame.

        Args:
            renderer: SDL renderer to create texture for

        Returns:
            SDL_Texture pointer
        """
        if _sdl2 is None:
            raise ImportError("SDL2 is required")

        if self._frame_data is None:
            raise RuntimeError("No frame data available")

        rmask = 0x000000FF
        gmask = 0x0000FF00
        bmask = 0x00FF0000
        amask = 0xFF000000

        surface = _sdl2.SDL_CreateRGBSurfaceFrom(
            ctypes.c_char_p(self._frame_data),
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

    def close(self) -> None:
        """Release video resources."""
        if self._cap is not None:
            self._cap.release()
            self._cap = None
        self._frame_data = None

    def __del__(self) -> None:
        """Clean up on garbage collection."""
        self.close()


def get_video_size(path: str) -> tuple[int, int]:
    """Get dimensions of a video without keeping it loaded.

    Args:
        path: Path to the video file

    Returns:
        Tuple of (width, height)
    """
    if not _HAS_CV2 or _cv2 is None:
        raise ImportError(
            "OpenCV is required for video support. "
            "Install it with: pip install opencv-python"
        )

    cap = _cv2.VideoCapture(path)
    if not cap.isOpened():
        raise ValueError(f"Failed to open video '{path}'")

    width = int(cap.get(_cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(_cv2.CAP_PROP_FRAME_HEIGHT))
    cap.release()

    return (width, height)


def get_video_info(path: str) -> dict[str, Any]:
    """Get information about a video file.

    Args:
        path: Path to the video file

    Returns:
        Dictionary with width, height, fps, frame_count, duration
    """
    if not _HAS_CV2 or _cv2 is None:
        raise ImportError(
            "OpenCV is required for video support. "
            "Install it with: pip install opencv-python"
        )

    cap = _cv2.VideoCapture(path)
    if not cap.isOpened():
        raise ValueError(f"Failed to open video '{path}'")

    info = {
        "width": int(cap.get(_cv2.CAP_PROP_FRAME_WIDTH)),
        "height": int(cap.get(_cv2.CAP_PROP_FRAME_HEIGHT)),
        "fps": cap.get(_cv2.CAP_PROP_FPS),
        "frame_count": int(cap.get(_cv2.CAP_PROP_FRAME_COUNT)),
    }
    info["duration"] = info["frame_count"] / info["fps"] if info["fps"] > 0 else 0.0

    cap.release()
    return info


__all__ = ["VideoPlayer", "has_video_support", "get_video_size", "get_video_info"]
