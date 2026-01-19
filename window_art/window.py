"""Window class wrapping SDL2 windows."""
from __future__ import annotations

import ctypes
import sys
from typing import TYPE_CHECKING, Any, Union

import sdl2
import sdl2.ext

from .color import Color, ColorLike

PaddingLike = Union[int, tuple[int, int], tuple[int, int, int, int]]

if TYPE_CHECKING:
    from .core import Desktop

_HAS_SDL2_IMAGE = False
try:
    from sdl2 import sdlimage as _sdlimage

    _HAS_SDL2_IMAGE = True
except ImportError:
    _sdlimage = None

_objc = None
_HAS_COCOA = False
if sys.platform == "darwin":
    try:
        _objc = ctypes.cdll.LoadLibrary("/usr/lib/libobjc.A.dylib")
        _objc.objc_msgSend.restype = ctypes.c_void_p
        _objc.objc_msgSend.argtypes = [ctypes.c_void_p, ctypes.c_void_p]
        _objc.sel_registerName.restype = ctypes.c_void_p
        _objc.sel_registerName.argtypes = [ctypes.c_char_p]
        _HAS_COCOA = True
    except Exception:
        pass


def _set_nswindow_shadow(sdl_window: Any, has_shadow: bool) -> bool:
    """Set shadow on NSWindow (macOS only). Returns True if successful."""
    if not _HAS_COCOA or not _objc:
        return False

    try:
        info = sdl2.SDL_SysWMinfo()
        sdl2.SDL_VERSION(info.version)
        if not sdl2.SDL_GetWindowWMInfo(sdl_window, ctypes.byref(info)):
            return False
        if info.subsystem != sdl2.SDL_SYSWM_COCOA:
            return False

        nswindow = info.info.cocoa.window
        if not nswindow:
            return False

        sel_setHasShadow = _objc.sel_registerName(b"setHasShadow:")
        objc_msgSend_bool = ctypes.CFUNCTYPE(
            None, ctypes.c_void_p, ctypes.c_void_p, ctypes.c_bool
        )(("objc_msgSend", _objc))
        objc_msgSend_bool(nswindow, sel_setHasShadow, has_shadow)
        return True
    except Exception:
        return False


class Window:
    """A desktop window that can be positioned, sized, and colored."""

    _id_counter: int = 0

    def __init__(
        self,
        desktop: Desktop,
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
    ) -> None:
        Window._id_counter += 1
        self._id = Window._id_counter
        self._desktop = desktop
        self._x = float(x)
        self._y = float(y)
        self._w = float(w)
        self._h = float(h)
        self._color = Color.parse(color)
        self._opacity = opacity
        self._closed = False
        self._borderless = borderless
        self._always_on_top = always_on_top
        self._resizable = resizable
        self._title = title
        self._shadow = shadow

        self._image_path: str | None = None
        self._image_texture: Any = None
        self._image_region: tuple[int, int, int, int] | None = None
        self._image_size: tuple[int, int] | None = None

        self._gif: Any = None
        self._gif_texture: Any = None
        self._gif_region: tuple[int, int, int, int] | None = None

        self._video: Any = None
        self._video_texture: Any = None
        self._video_region: tuple[int, int, int, int] | None = None

        self._text: str | None = None
        self._font: str = font
        self._font_size: int = font_size
        self._text_color: Color = Color.parse(text_color)
        self._text_align: str = text_align
        self._text_valign: str = text_valign
        self._text_wrap: bool = text_wrap
        self._text_padding: PaddingLike = text_padding
        self._text_renderer: Any = None
        self._text_texture: Any = None
        self._text_dirty: bool = False

        self._dirty = True
        self._position_dirty = False
        self._size_dirty = False
        self._opacity_dirty = False

        flags = 0
        if borderless:
            flags |= sdl2.SDL_WINDOW_BORDERLESS
        if always_on_top:
            flags |= sdl2.SDL_WINDOW_ALWAYS_ON_TOP
        if resizable:
            flags |= sdl2.SDL_WINDOW_RESIZABLE

        self._sdl_window = sdl2.SDL_CreateWindow(
            title.encode("utf-8"),
            int(self._x),
            int(self._y),
            int(self._w),
            int(self._h),
            flags,
        )
        if not self._sdl_window:
            raise RuntimeError(f"Failed to create window: {sdl2.SDL_GetError()}")

        self._renderer = sdl2.SDL_CreateRenderer(
            self._sdl_window,
            -1,
            sdl2.SDL_RENDERER_ACCELERATED,
        )
        if not self._renderer:
            sdl2.SDL_DestroyWindow(self._sdl_window)
            raise RuntimeError(f"Failed to create renderer: {sdl2.SDL_GetError()}")

        self._apply_opacity()
        self._render()
        self._dirty = False

        if not shadow:
            _set_nswindow_shadow(self._sdl_window, False)

        if image is not None:
            self._load_image(image)
            self._render()
        elif gif is not None:
            self._load_gif(gif)
            self._render()
        elif video is not None:
            self._load_video(video)
            self._render()

        if text is not None:
            self._create_or_update_text(text)
            self._render()

    @property
    def id(self) -> int:
        """Unique identifier for this window."""
        return self._id

    @property
    def x(self) -> float:
        """X position of the window."""
        return self._x

    @x.setter
    def x(self, value: float) -> None:
        self._x = float(value)
        self._position_dirty = True

    @property
    def y(self) -> float:
        """Y position of the window."""
        return self._y

    @y.setter
    def y(self, value: float) -> None:
        self._y = float(value)
        self._position_dirty = True

    @property
    def w(self) -> float:
        """Width of the window."""
        return self._w

    @w.setter
    def w(self, value: float) -> None:
        self._w = float(value)
        self._size_dirty = True

    @property
    def h(self) -> float:
        """Height of the window."""
        return self._h

    @h.setter
    def h(self, value: float) -> None:
        self._h = float(value)
        self._size_dirty = True

    @property
    def width(self) -> float:
        """Width of the window (alias for w)."""
        return self._w

    @width.setter
    def width(self, value: float) -> None:
        self.w = value

    @property
    def height(self) -> float:
        """Height of the window (alias for h)."""
        return self._h

    @height.setter
    def height(self, value: float) -> None:
        self.h = value

    @property
    def position(self) -> tuple[float, float]:
        """Position as (x, y) tuple."""
        return (self._x, self._y)

    @position.setter
    def position(self, value: tuple[float, float]) -> None:
        self._x, self._y = float(value[0]), float(value[1])
        self._position_dirty = True

    @property
    def size(self) -> tuple[float, float]:
        """Size as (w, h) tuple."""
        return (self._w, self._h)

    @size.setter
    def size(self, value: tuple[float, float]) -> None:
        self._w, self._h = float(value[0]), float(value[1])
        self._size_dirty = True

    @property
    def color(self) -> Color:
        """Color of the window."""
        return self._color

    @color.setter
    def color(self, value: ColorLike) -> None:
        self._color = Color.parse(value)
        self._dirty = True

    @property
    def opacity(self) -> float:
        """Opacity of the window (0.0 to 1.0)."""
        return self._opacity

    @opacity.setter
    def opacity(self, value: float) -> None:
        self._opacity = max(0.0, min(1.0, float(value)))
        self._opacity_dirty = True

    @property
    def shadow(self) -> bool:
        """Whether the window has a shadow (macOS only)."""
        return self._shadow

    @shadow.setter
    def shadow(self, value: bool) -> None:
        self._shadow = value
        if not self._closed:
            _set_nswindow_shadow(self._sdl_window, value)

    @property
    def image(self) -> str | None:
        """Path to the image displayed in the window (None for solid color)."""
        return self._image_path

    @image.setter
    def image(self, value: str | None) -> None:
        if value is None:
            self._destroy_texture()
            self._image_path = None
        else:
            self._load_image(value)
        self._dirty = True

    @property
    def image_region(self) -> tuple[int, int, int, int] | None:
        """Source region of the image to display (x, y, w, h) or None for full image."""
        return self._image_region

    @image_region.setter
    def image_region(self, value: tuple[int, int, int, int] | None) -> None:
        self._image_region = value
        self._dirty = True

    @property
    def image_size(self) -> tuple[int, int] | None:
        """Size of the loaded image (width, height) or None if no image."""
        return self._image_size

    @property
    def gif(self) -> str | None:
        """Path to the GIF displayed in the window (None if no GIF)."""
        return self._gif.path if self._gif else None

    @gif.setter
    def gif(self, value: str | None) -> None:
        if value is None:
            self._destroy_gif()
        else:
            self._load_gif(value)
        self._dirty = True

    @property
    def gif_region(self) -> tuple[int, int, int, int] | None:
        """Source region of the GIF to display (x, y, w, h) or None for full GIF."""
        return self._gif_region

    @gif_region.setter
    def gif_region(self, value: tuple[int, int, int, int] | None) -> None:
        self._gif_region = value
        self._dirty = True

    @property
    def gif_size(self) -> tuple[int, int] | None:
        """Size of the loaded GIF (width, height) or None if no GIF."""
        return self._gif.size if self._gif else None

    @property
    def gif_playing(self) -> bool:
        """Whether the GIF animation is playing."""
        return self._gif.playing if self._gif else False

    @gif_playing.setter
    def gif_playing(self, value: bool) -> None:
        if self._gif:
            self._gif.playing = value

    @property
    def gif_loop(self) -> bool:
        """Whether the GIF animation loops."""
        return self._gif.loop if self._gif else True

    @gif_loop.setter
    def gif_loop(self, value: bool) -> None:
        if self._gif:
            self._gif.loop = value

    @property
    def gif_speed(self) -> float:
        """GIF playback speed multiplier (1.0 = normal)."""
        return self._gif.speed if self._gif else 1.0

    @gif_speed.setter
    def gif_speed(self, value: float) -> None:
        if self._gif:
            self._gif.speed = value

    @property
    def gif_frame(self) -> int:
        """Current GIF frame index (0-based)."""
        return self._gif.current_frame if self._gif else 0

    @gif_frame.setter
    def gif_frame(self, value: int) -> None:
        if self._gif:
            self._gif.current_frame = value
            self._update_gif_texture()

    @property
    def gif_frame_count(self) -> int:
        """Total number of frames in the GIF."""
        return self._gif.frame_count if self._gif else 0

    @property
    def video(self) -> str | None:
        """Path to the video displayed in the window (None if no video)."""
        return self._video.path if self._video else None

    @video.setter
    def video(self, value: str | None) -> None:
        if value is None:
            self._destroy_video()
        else:
            self._load_video(value)
        self._dirty = True

    @property
    def video_region(self) -> tuple[int, int, int, int] | None:
        """Source region of the video to display (x, y, w, h) or None for full video."""
        return self._video_region

    @video_region.setter
    def video_region(self, value: tuple[int, int, int, int] | None) -> None:
        self._video_region = value
        self._dirty = True

    @property
    def video_size(self) -> tuple[int, int] | None:
        """Size of the loaded video (width, height) or None if no video."""
        return self._video.size if self._video else None

    @property
    def video_playing(self) -> bool:
        """Whether the video is playing."""
        return self._video.playing if self._video else False

    @video_playing.setter
    def video_playing(self, value: bool) -> None:
        if self._video:
            self._video.playing = value

    @property
    def video_loop(self) -> bool:
        """Whether the video loops."""
        return self._video.loop if self._video else True

    @video_loop.setter
    def video_loop(self, value: bool) -> None:
        if self._video:
            self._video.loop = value

    @property
    def video_speed(self) -> float:
        """Video playback speed multiplier (1.0 = normal)."""
        return self._video.speed if self._video else 1.0

    @video_speed.setter
    def video_speed(self, value: float) -> None:
        if self._video:
            self._video.speed = value

    @property
    def video_position(self) -> float:
        """Current video playback position in seconds."""
        return self._video.current_time if self._video else 0.0

    @video_position.setter
    def video_position(self, value: float) -> None:
        if self._video:
            self._video.current_time = value
            self._update_video_texture()

    @property
    def video_duration(self) -> float:
        """Total duration of the video in seconds."""
        return self._video.duration if self._video else 0.0

    @property
    def video_frame(self) -> int:
        """Current video frame index (0-based)."""
        return self._video.current_frame if self._video else 0

    @video_frame.setter
    def video_frame(self, value: int) -> None:
        if self._video:
            self._video.current_frame = value
            self._update_video_texture()

    @property
    def text(self) -> str | None:
        """Text content displayed in the window."""
        return self._text

    @text.setter
    def text(self, value: str | None) -> None:
        if value is None:
            self._destroy_text()
            self._text = None
        else:
            self._create_or_update_text(value)
        self._dirty = True

    @property
    def font(self) -> str:
        """Font family or path to .ttf file."""
        return self._font

    @font.setter
    def font(self, value: str) -> None:
        if self._font != value:
            self._font = value
            if self._text_renderer:
                self._text_renderer.font = value
                self._text_dirty = True
                self._dirty = True

    @property
    def font_size(self) -> int:
        """Font size in pixels."""
        return self._font_size

    @font_size.setter
    def font_size(self, value: int) -> None:
        if self._font_size != value:
            self._font_size = value
            if self._text_renderer:
                self._text_renderer.font_size = value
                self._text_dirty = True
                self._dirty = True

    @property
    def text_color(self) -> Color:
        """Text color."""
        return self._text_color

    @text_color.setter
    def text_color(self, value: ColorLike) -> None:
        new_color = Color.parse(value)
        if self._text_color != new_color:
            self._text_color = new_color
            if self._text_renderer:
                self._text_renderer.text_color = new_color.as_tuple()
                self._text_dirty = True
                self._dirty = True

    @property
    def text_align(self) -> str:
        """Horizontal text alignment (left, center, right)."""
        return self._text_align

    @text_align.setter
    def text_align(self, value: str) -> None:
        if self._text_align != value:
            self._text_align = value
            if self._text_renderer:
                self._text_renderer.text_align = value
                self._text_dirty = True
                self._dirty = True

    @property
    def text_valign(self) -> str:
        """Vertical text alignment (top, center, bottom)."""
        return self._text_valign

    @text_valign.setter
    def text_valign(self, value: str) -> None:
        if self._text_valign != value:
            self._text_valign = value
            if self._text_renderer:
                self._text_renderer.text_valign = value
                self._text_dirty = True
                self._dirty = True

    @property
    def text_wrap(self) -> bool:
        """Whether text wrapping is enabled."""
        return self._text_wrap

    @text_wrap.setter
    def text_wrap(self, value: bool) -> None:
        if self._text_wrap != value:
            self._text_wrap = value
            if self._text_renderer:
                self._text_renderer.text_wrap = value
                self._text_dirty = True
                self._dirty = True

    @property
    def text_padding(self) -> PaddingLike:
        """Padding around text."""
        return self._text_padding

    @text_padding.setter
    def text_padding(self, value: PaddingLike) -> None:
        self._text_padding = value
        if self._text_renderer:
            self._text_renderer.text_padding = value
            self._text_dirty = True
            self._dirty = True

    @property
    def closed(self) -> bool:
        """Whether the window has been closed."""
        return self._closed

    @property
    def title(self) -> str:
        """Window title."""
        return self._title

    @title.setter
    def title(self, value: str) -> None:
        self._title = value
        if not self._closed:
            sdl2.SDL_SetWindowTitle(self._sdl_window, value.encode("utf-8"))

    @property
    def borderless(self) -> bool:
        """Whether the window is borderless (no title bar)."""
        return self._borderless

    @borderless.setter
    def borderless(self, value: bool) -> None:
        self._borderless = value
        if not self._closed:
            sdl2.SDL_SetWindowBordered(self._sdl_window, not value)

    @property
    def always_on_top(self) -> bool:
        """Whether the window stays on top of other windows."""
        return self._always_on_top

    @always_on_top.setter
    def always_on_top(self, value: bool) -> None:
        self._always_on_top = value
        if not self._closed:
            sdl2.SDL_SetWindowAlwaysOnTop(self._sdl_window, value)

    @property
    def resizable(self) -> bool:
        """Whether the window can be resized by the user."""
        return self._resizable

    @resizable.setter
    def resizable(self, value: bool) -> None:
        self._resizable = value
        if not self._closed:
            sdl2.SDL_SetWindowResizable(self._sdl_window, value)

    def _load_image(self, path: str) -> None:
        """Load an image from a file and create a texture from it."""
        if not _HAS_SDL2_IMAGE or _sdlimage is None:
            raise ImportError(
                "SDL2_image is required for image support. "
                "Install it with: pip install pysdl2-dll"
            )

        self._destroy_texture()

        surface = _sdlimage.IMG_Load(path.encode("utf-8"))
        if not surface:
            error = sdl2.SDL_GetError()
            error_str = error.decode("utf-8") if error else "Unknown error"
            raise ValueError(f"Failed to load image '{path}': {error_str}")

        self._image_size = (surface.contents.w, surface.contents.h)

        self._image_texture = sdl2.SDL_CreateTextureFromSurface(
            self._renderer, surface
        )
        sdl2.SDL_FreeSurface(surface)

        if not self._image_texture:
            error = sdl2.SDL_GetError()
            error_str = error.decode("utf-8") if error else "Unknown error"
            raise ValueError(f"Failed to create texture: {error_str}")

        self._image_path = path

    def _destroy_texture(self) -> None:
        """Destroy the current image texture if it exists."""
        if self._image_texture:
            sdl2.SDL_DestroyTexture(self._image_texture)
            self._image_texture = None
            self._image_size = None
            self._image_region = None

    def _load_gif(self, path: str) -> None:
        """Load an animated GIF from a file."""
        from .media.gif import GifAnimation

        self._destroy_texture()
        self._destroy_gif()
        self._destroy_video()

        self._gif = GifAnimation(path)
        self._update_gif_texture()

    def _destroy_gif(self) -> None:
        """Destroy the current GIF and its texture."""
        if self._gif_texture:
            sdl2.SDL_DestroyTexture(self._gif_texture)
            self._gif_texture = None
        self._gif = None
        self._gif_region = None

    def _update_gif_texture(self) -> None:
        """Update the GIF texture to the current frame."""
        if not self._gif:
            return

        if self._gif_texture:
            sdl2.SDL_DestroyTexture(self._gif_texture)

        self._gif_texture = self._gif.create_texture(self._renderer)

    def _load_video(self, path: str) -> None:
        """Load a video from a file."""
        from .media.video import VideoPlayer

        self._destroy_texture()
        self._destroy_gif()
        self._destroy_video()

        self._video = VideoPlayer(path)
        self._update_video_texture()

    def _destroy_video(self) -> None:
        """Destroy the current video and its texture."""
        if self._video_texture:
            sdl2.SDL_DestroyTexture(self._video_texture)
            self._video_texture = None
        if self._video:
            self._video.close()
        self._video = None
        self._video_region = None

    def _update_video_texture(self) -> None:
        """Update the video texture to the current frame."""
        if not self._video:
            return

        if self._video_texture:
            sdl2.SDL_DestroyTexture(self._video_texture)

        self._video_texture = self._video.create_texture(self._renderer)

    def _create_or_update_text(self, text: str) -> None:
        """Create or update text rendering."""
        from .media.text import TextRenderer

        self._text = text

        if self._text_renderer is None:
            self._text_renderer = TextRenderer(
                text=text,
                width=int(self._w),
                height=int(self._h),
                font=self._font,
                font_size=self._font_size,
                text_color=self._text_color.as_tuple(),
                text_align=self._text_align,
                text_valign=self._text_valign,
                text_wrap=self._text_wrap,
                text_padding=self._text_padding,
            )
        else:
            self._text_renderer.text = text

        self._text_dirty = True
        self._update_text_texture()

    def _update_text_texture(self) -> None:
        """Update the text texture."""
        if not self._text_renderer:
            return

        if self._text_texture:
            sdl2.SDL_DestroyTexture(self._text_texture)

        self._text_renderer.resize(int(self._w), int(self._h))

        self._text_texture = self._text_renderer.create_texture(self._renderer)
        self._text_dirty = False

    def _destroy_text(self) -> None:
        """Destroy text renderer and texture."""
        if self._text_texture:
            sdl2.SDL_DestroyTexture(self._text_texture)
            self._text_texture = None
        self._text_renderer = None
        self._text_dirty = False

    def _apply_opacity(self) -> None:
        """Apply the current opacity to the window."""
        if not self._closed:
            sdl2.SDL_SetWindowOpacity(self._sdl_window, self._opacity)

    def _apply_changes(self, dt: float = 0.0) -> None:
        """Apply all pending changes. Called by the update loop.

        Args:
            dt: Delta time in seconds since last update (for animations)
        """
        if self._closed:
            return

        if self._position_dirty:
            sdl2.SDL_SetWindowPosition(self._sdl_window, int(self._x), int(self._y))
            self._position_dirty = False

        if self._size_dirty:
            sdl2.SDL_SetWindowSize(self._sdl_window, int(self._w), int(self._h))
            self._size_dirty = False
            self._dirty = True
            if self._text_renderer:
                self._text_dirty = True

        if self._opacity_dirty:
            sdl2.SDL_SetWindowOpacity(self._sdl_window, self._opacity)
            self._opacity_dirty = False

        if self._gif and dt > 0:
            if self._gif.update(dt):
                self._update_gif_texture()
                self._dirty = True

        if self._video and dt > 0:
            if self._video.update(dt):
                self._update_video_texture()
                self._dirty = True

        if self._text_dirty and self._text_renderer:
            self._update_text_texture()
            self._dirty = True

        if self._dirty:
            self._render()
            self._dirty = False

    def _render(self) -> None:
        """Render the window contents."""
        if self._closed:
            return

        sdl2.SDL_SetRenderDrawColor(
            self._renderer,
            self._color.r,
            self._color.g,
            self._color.b,
            self._color.a,
        )

        sdl2.SDL_RenderClear(self._renderer)

        if self._image_texture:
            src_rect = None
            if self._image_region is not None:
                src_rect = sdl2.SDL_Rect(
                    self._image_region[0],
                    self._image_region[1],
                    self._image_region[2],
                    self._image_region[3],
                )
            sdl2.SDL_RenderCopy(self._renderer, self._image_texture, src_rect, None)

        elif self._gif_texture:
            src_rect = None
            if self._gif_region is not None:
                src_rect = sdl2.SDL_Rect(
                    self._gif_region[0],
                    self._gif_region[1],
                    self._gif_region[2],
                    self._gif_region[3],
                )
            sdl2.SDL_RenderCopy(self._renderer, self._gif_texture, src_rect, None)

        elif self._video_texture:
            src_rect = None
            if self._video_region is not None:
                src_rect = sdl2.SDL_Rect(
                    self._video_region[0],
                    self._video_region[1],
                    self._video_region[2],
                    self._video_region[3],
                )
            sdl2.SDL_RenderCopy(self._renderer, self._video_texture, src_rect, None)

        if self._text_texture:
            sdl2.SDL_RenderCopy(self._renderer, self._text_texture, None, None)

        sdl2.SDL_RenderPresent(self._renderer)

    def close(self) -> None:
        """Close and destroy the window."""
        if self._closed:
            return
        self._closed = True

        self._destroy_texture()
        self._destroy_gif()
        self._destroy_video()
        self._destroy_text()

        if self._renderer:
            sdl2.SDL_DestroyRenderer(self._renderer)
            self._renderer = None

        if self._sdl_window:
            sdl2.SDL_DestroyWindow(self._sdl_window)
            self._sdl_window = None

        self._desktop._remove_window(self)

    def show(self) -> None:
        """Show the window."""
        if not self._closed:
            sdl2.SDL_ShowWindow(self._sdl_window)

    def hide(self) -> None:
        """Hide the window."""
        if not self._closed:
            sdl2.SDL_HideWindow(self._sdl_window)

    def raise_window(self) -> None:
        """Raise the window to the top."""
        if not self._closed:
            sdl2.SDL_RaiseWindow(self._sdl_window)

    def __repr__(self) -> str:
        status = "closed" if self._closed else "open"
        return (
            f"Window(id={self._id}, x={self._x}, y={self._y}, "
            f"w={self._w}, h={self._h}, color={self._color}, {status})"
        )

    def __del__(self) -> None:
        """Clean up on garbage collection."""
        self.close()
