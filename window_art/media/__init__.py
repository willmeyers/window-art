"""
Media plugins for desktop_windows.

Supports:
- Images (PNG, JPG, etc.) via SDL2_image
- Animated GIFs via Pillow
- Video (MP4, etc.) via OpenCV

Optional dependencies:
    pip install desktop-windows[images]   # SDL2_image
    pip install desktop-windows[gif]      # Pillow
    pip install desktop-windows[video]    # OpenCV
"""

from __future__ import annotations

from typing import Any, Union

ImageLike = Union[str, Any]

_HAS_SDL2_IMAGE = False

try:
    from sdl2 import sdlimage as _sdlimage

    _HAS_SDL2_IMAGE = True
except ImportError:
    _sdlimage = None


def has_image_support() -> bool:
    """Check if SDL2_image is available for loading images."""
    return _HAS_SDL2_IMAGE


def load_image(path: str) -> Any:
    """
    Load an image from a file path and return an SDL surface.

    Args:
        path: Path to the image file (PNG, JPG, etc.)

    Returns:
        SDL_Surface pointer

    Raises:
        ImportError: If SDL2_image is not available
        ValueError: If the image fails to load
    """
    if not _HAS_SDL2_IMAGE or _sdlimage is None:
        raise ImportError(
            "SDL2_image is required for image support. "
            "Install it with: pip install pysdl2-dll"
        )

    surface = _sdlimage.IMG_Load(path.encode("utf-8"))
    if not surface:
        from sdl2 import SDL_GetError

        error = SDL_GetError()
        error_str = error.decode("utf-8") if error else "Unknown error"
        raise ValueError(f"Failed to load image '{path}': {error_str}")

    return surface


def get_image_size(path: str) -> tuple[int, int]:
    """
    Get the dimensions of an image without keeping it loaded.

    Args:
        path: Path to the image file (PNG, JPG, etc.)

    Returns:
        Tuple of (width, height)

    Raises:
        ImportError: If SDL2_image is not available
        ValueError: If the image fails to load
    """
    from sdl2 import SDL_FreeSurface

    surface = load_image(path)
    size = (surface.contents.w, surface.contents.h)
    SDL_FreeSurface(surface)
    return size


from .gif import GifAnimation, get_gif_info, get_gif_size, has_gif_support

from .video import VideoPlayer, get_video_info, get_video_size, has_video_support

from .text import TextRenderer, get_text_size, has_text_support

__all__ = [
    "ImageLike",
    "has_image_support",
    "load_image",
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
]
