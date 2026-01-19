"""Text rendering support using Pillow."""
from __future__ import annotations

import ctypes
from typing import Any, Union

_HAS_PIL = False
_Image: Any = None
_ImageDraw: Any = None
_ImageFont: Any = None
try:
    from PIL import Image, ImageDraw, ImageFont

    _Image = Image
    _ImageDraw = ImageDraw
    _ImageFont = ImageFont
    _HAS_PIL = True
except ImportError:
    pass

_sdl2: Any = None
try:
    import sdl2

    _sdl2 = sdl2
except ImportError:
    pass

PaddingLike = Union[int, tuple[int, int], tuple[int, int, int, int]]


def has_text_support() -> bool:
    """Check if text rendering support is available."""
    return _HAS_PIL and _sdl2 is not None


def _normalize_padding(padding: PaddingLike) -> tuple[int, int, int, int]:
    """Convert padding to (left, top, right, bottom) tuple."""
    if isinstance(padding, int):
        return (padding, padding, padding, padding)
    elif len(padding) == 2:
        h, v = padding
        return (h, v, h, v)
    elif len(padding) == 4:
        return (padding[0], padding[1], padding[2], padding[3])
    else:
        raise ValueError(f"Invalid padding format: {padding}")


def get_text_size(
    text: str,
    font: str = "Arial",
    font_size: int = 24,
) -> tuple[int, int]:
    """Measure text dimensions without rendering.

    Args:
        text: Text to measure
        font: Font family name or path to .ttf file
        font_size: Font size in pixels

    Returns:
        Tuple of (width, height) in pixels
    """
    if not _HAS_PIL or _ImageFont is None:
        raise ImportError(
            "Pillow is required for text support. "
            "Install it with: pip install Pillow"
        )

    pil_font = _load_font(font, font_size)

    dummy = _Image.new("RGBA", (1, 1))
    draw = _ImageDraw.Draw(dummy)
    bbox = draw.textbbox((0, 0), text, font=pil_font)
    width = bbox[2] - bbox[0]
    height = bbox[3] - bbox[1]

    return (width, height)


def _load_font(font: str, font_size: int) -> Any:
    """Load a PIL font from name or path."""
    if not _HAS_PIL or _ImageFont is None:
        raise ImportError(
            "Pillow is required for text support. "
            "Install it with: pip install Pillow"
        )

    if font.endswith((".ttf", ".otf", ".TTF", ".OTF")):
        try:
            return _ImageFont.truetype(font, font_size)
        except OSError as e:
            raise ValueError(f"Failed to load font file '{font}': {e}")

    try:
        return _ImageFont.truetype(font, font_size)
    except OSError:
        pass

    import sys

    font_paths = []
    if sys.platform == "darwin":
        font_paths = [
            f"/System/Library/Fonts/{font}.ttf",
            f"/System/Library/Fonts/{font}.ttc",
            f"/Library/Fonts/{font}.ttf",
            f"/Library/Fonts/{font}.ttc",
            f"~/Library/Fonts/{font}.ttf",
            f"~/Library/Fonts/{font}.ttc",
            f"/System/Library/Fonts/Supplemental/{font}.ttf",
            f"/System/Library/Fonts/Supplemental/{font}.ttc",
        ]
    elif sys.platform == "win32":
        import os

        windir = os.environ.get("WINDIR", "C:\\Windows")
        font_paths = [
            f"{windir}\\Fonts\\{font}.ttf",
            f"{windir}\\Fonts\\{font.lower()}.ttf",
        ]
    else:
        font_paths = [
            f"/usr/share/fonts/truetype/{font.lower()}/{font}.ttf",
            f"/usr/share/fonts/TTF/{font}.ttf",
            f"~/.fonts/{font}.ttf",
        ]

    import os

    for path in font_paths:
        expanded = os.path.expanduser(path)
        if os.path.exists(expanded):
            try:
                return _ImageFont.truetype(expanded, font_size)
            except OSError:
                continue

    try:
        return _ImageFont.load_default()
    except Exception:
        return _ImageFont.load_default(size=font_size)


class TextRenderer:
    """Renders text to RGBA bytes for use as SDL textures."""

    def __init__(
        self,
        text: str,
        width: int,
        height: int,
        font: str = "Arial",
        font_size: int = 24,
        text_color: tuple[int, int, int, int] = (0, 0, 0, 255),
        text_align: str = "center",
        text_valign: str = "center",
        text_wrap: bool = False,
        text_padding: PaddingLike = 0,
    ) -> None:
        """Create a text renderer.

        Args:
            text: Text content to render
            width: Target width in pixels
            height: Target height in pixels
            font: Font family name or path to .ttf file
            font_size: Font size in pixels
            text_color: RGBA color tuple for text
            text_align: Horizontal alignment (left, center, right)
            text_valign: Vertical alignment (top, center, bottom)
            text_wrap: Enable word wrapping
            text_padding: Padding around text
        """
        if not _HAS_PIL:
            raise ImportError(
                "Pillow is required for text support. "
                "Install it with: pip install Pillow"
            )

        self._text = text
        self._width = width
        self._height = height
        self._font_name = font
        self._font_size = font_size
        self._text_color = text_color
        self._text_align = text_align
        self._text_valign = text_valign
        self._text_wrap = text_wrap
        self._text_padding = _normalize_padding(text_padding)

        self._font = _load_font(font, font_size)
        self._image: Any = None
        self._data: bytes | None = None
        self._dirty = True

    @property
    def text(self) -> str:
        return self._text

    @text.setter
    def text(self, value: str) -> None:
        if self._text != value:
            self._text = value
            self._dirty = True

    @property
    def font(self) -> str:
        return self._font_name

    @font.setter
    def font(self, value: str) -> None:
        if self._font_name != value:
            self._font_name = value
            self._font = _load_font(value, self._font_size)
            self._dirty = True

    @property
    def font_size(self) -> int:
        return self._font_size

    @font_size.setter
    def font_size(self, value: int) -> None:
        if self._font_size != value:
            self._font_size = value
            self._font = _load_font(self._font_name, value)
            self._dirty = True

    @property
    def text_color(self) -> tuple[int, int, int, int]:
        return self._text_color

    @text_color.setter
    def text_color(self, value: tuple[int, int, int, int]) -> None:
        if self._text_color != value:
            self._text_color = value
            self._dirty = True

    @property
    def text_align(self) -> str:
        return self._text_align

    @text_align.setter
    def text_align(self, value: str) -> None:
        if self._text_align != value:
            self._text_align = value
            self._dirty = True

    @property
    def text_valign(self) -> str:
        return self._text_valign

    @text_valign.setter
    def text_valign(self, value: str) -> None:
        if self._text_valign != value:
            self._text_valign = value
            self._dirty = True

    @property
    def text_wrap(self) -> bool:
        return self._text_wrap

    @text_wrap.setter
    def text_wrap(self, value: bool) -> None:
        if self._text_wrap != value:
            self._text_wrap = value
            self._dirty = True

    @property
    def text_padding(self) -> tuple[int, int, int, int]:
        return self._text_padding

    @text_padding.setter
    def text_padding(self, value: PaddingLike) -> None:
        normalized = _normalize_padding(value)
        if self._text_padding != normalized:
            self._text_padding = normalized
            self._dirty = True

    def resize(self, width: int, height: int) -> None:
        """Resize the render target."""
        if self._width != width or self._height != height:
            self._width = width
            self._height = height
            self._dirty = True

    def _wrap_text(self, text: str, max_width: int) -> list[str]:
        """Wrap text to fit within max_width."""
        if not text:
            return [""]

        words = text.split()
        if not words:
            return [""]

        lines: list[str] = []
        current_line: list[str] = []

        for word in words:
            test_line = " ".join(current_line + [word])
            bbox = self._font.getbbox(test_line)
            width = bbox[2] - bbox[0]

            if width <= max_width:
                current_line.append(word)
            else:
                if current_line:
                    lines.append(" ".join(current_line))
                    current_line = [word]
                else:
                    lines.append(word)

        if current_line:
            lines.append(" ".join(current_line))

        return lines if lines else [""]

    def render(self) -> bytes:
        """Render text to RGBA bytes.

        Returns:
            Raw RGBA pixel data as bytes
        """
        if not self._dirty and self._data is not None:
            return self._data

        self._image = _Image.new("RGBA", (self._width, self._height), (0, 0, 0, 0))
        draw = _ImageDraw.Draw(self._image)

        if not self._text:
            self._data = self._image.tobytes()
            self._dirty = False
            return self._data

        pad_left, pad_top, pad_right, pad_bottom = self._text_padding
        content_width = self._width - pad_left - pad_right
        content_height = self._height - pad_top - pad_bottom

        if content_width <= 0 or content_height <= 0:
            self._data = self._image.tobytes()
            self._dirty = False
            return self._data

        if self._text_wrap:
            lines = self._wrap_text(self._text, content_width)
        else:
            lines = self._text.split("\n")

        line_heights: list[int] = []
        for line in lines:
            if line:
                bbox = self._font.getbbox(line)
                line_heights.append(bbox[3] - bbox[1])
            else:
                bbox = self._font.getbbox(" ")
                line_heights.append(bbox[3] - bbox[1])

        total_height = sum(line_heights)
        line_spacing = int(self._font_size * 0.2)
        total_height += line_spacing * (len(lines) - 1) if len(lines) > 1 else 0

        if self._text_valign == "top":
            y = pad_top
        elif self._text_valign == "bottom":
            y = pad_top + content_height - total_height
        else:
            y = pad_top + (content_height - total_height) // 2

        for i, line in enumerate(lines):
            if not line:
                y += line_heights[i] + line_spacing
                continue

            bbox = self._font.getbbox(line)
            line_width = bbox[2] - bbox[0]

            if self._text_align == "left":
                x = pad_left
            elif self._text_align == "right":
                x = pad_left + content_width - line_width
            else:
                x = pad_left + (content_width - line_width) // 2

            draw.text((x, y), line, font=self._font, fill=self._text_color)
            y += line_heights[i] + line_spacing

        self._data = self._image.tobytes()
        self._dirty = False
        return self._data

    def create_texture(self, renderer: Any) -> Any:
        """Create an SDL texture from rendered text.

        Args:
            renderer: SDL renderer to create texture for

        Returns:
            SDL_Texture pointer
        """
        if _sdl2 is None:
            raise ImportError("SDL2 is required")

        data = self.render()

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

        _sdl2.SDL_SetTextureBlendMode(texture, _sdl2.SDL_BLENDMODE_BLEND)

        return texture


__all__ = ["TextRenderer", "has_text_support", "get_text_size", "PaddingLike"]
