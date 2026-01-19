# Media Support

window-art can display images, animated GIFs, and videos in windows.

## Images

### Creating an Image Window

```python
import window_art as wa

with wa.run():
    win = wa.window(100, 100, 400, 300, image="photo.jpg")
    wa.wait(3)
```

Supported formats: PNG, JPG, BMP, GIF (static), and other formats supported by SDL2_image.

### Image Properties

```python
# Set image path
win.image = "new_photo.png"

# Clear image (show solid color again)
win.image = None

# Get image dimensions
width, height = win.image_size
```

### Image Region (Cropping)

Display only a portion of the image:

```python
# Show a 200x200 region starting at (100, 50)
win.image_region = (100, 50, 200, 200)

# Reset to show full image
win.image_region = None
```

### Checking Support

```python
from window_art import has_image_support

if has_image_support():
    win = wa.window(100, 100, 400, 300, image="photo.jpg")
else:
    print("Image support not available")
```

## Animated GIFs

### Creating a GIF Window

```python
import window_art as wa

with wa.run():
    win = wa.window(100, 100, 400, 300, gif="animation.gif")
    wa.wait(5)  # GIF plays automatically
```

### GIF Playback Control

```python
# Pause/resume
win.gif_playing = False
win.gif_playing = True

# Loop control
win.gif_loop = True   # Loop continuously (default)
win.gif_loop = False  # Play once

# Speed control
win.gif_speed = 2.0   # 2x speed
win.gif_speed = 0.5   # Half speed
```

### Frame Control

```python
# Get current frame
current = win.gif_frame

# Set specific frame
win.gif_frame = 0  # Jump to first frame

# Get total frames
total = win.gif_frame_count
```

### GIF Properties

```python
# Dimensions
width, height = win.gif_size

# Source region (crop)
win.gif_region = (0, 0, 100, 100)
```

### Checking Support

```python
from window_art import has_gif_support

if has_gif_support():
    win = wa.window(100, 100, 400, 300, gif="animation.gif")
```

## Video

### Creating a Video Window

```python
import window_art as wa

with wa.run():
    win = wa.window(100, 100, 640, 480, video="movie.mp4")
    wa.wait(10)  # Video plays automatically
```

Supported formats: MP4, AVI, MOV, and other formats supported by OpenCV.

### Video Playback Control

```python
# Pause/resume
win.video_playing = False
win.video_playing = True

# Loop control
win.video_loop = True
win.video_loop = False

# Speed control
win.video_speed = 1.5  # 1.5x speed
```

### Seeking

```python
# Get current position (seconds)
current_time = win.video_position

# Seek to position (seconds)
win.video_position = 30.0  # Jump to 30 seconds

# Get duration
duration = win.video_duration
```

### Frame Access

```python
# Get current frame number
frame = win.video_frame

# Get total frames
total = win.video_frame_count
```

### Video Properties

```python
# Dimensions
width, height = win.video_size

# Source region (crop)
win.video_region = (0, 0, 320, 240)
```

### Checking Support

```python
from window_art import has_video_support

if has_video_support():
    win = wa.window(100, 100, 640, 480, video="movie.mp4")
```

## Media Information Functions

Get information about media files without loading them into windows:

### Images

```python
from window_art import get_image_size

width, height = get_image_size("photo.jpg")
print(f"Image is {width}x{height}")
```

### GIFs

```python
from window_art import get_gif_size, get_gif_info

# Quick size check
width, height = get_gif_size("animation.gif")

# Detailed info
info = get_gif_info("animation.gif")
print(f"Size: {info['width']}x{info['height']}")
print(f"Frames: {info['frame_count']}")
print(f"Duration: {info['total_duration']}s")
```

### Videos

```python
from window_art import get_video_size, get_video_info

# Quick size check
width, height = get_video_size("movie.mp4")

# Detailed info
info = get_video_info("movie.mp4")
print(f"Size: {info['width']}x{info['height']}")
print(f"FPS: {info['fps']}")
print(f"Frames: {info['frame_count']}")
print(f"Duration: {info['duration']}s")
```

## Switching Media

You can switch between media types on the same window:

```python
win = wa.window(100, 100, 400, 300, color="black")

# Show an image
win.image = "photo.jpg"
wa.wait(2)

# Switch to GIF (clears image)
win.gif = "animation.gif"
wa.wait(2)

# Switch to video (clears GIF)
win.video = "movie.mp4"
wa.wait(2)

# Clear all media, back to solid color
win.video = None
```

## Grid Media

See [Grid Layout](grid.md) for splitting media across multiple windows:

```python
grid = wa.grid(100, 100, 600, 400, columns="1fr 1fr 1fr", rows="1fr 1fr")

# Split image across grid
grid.fill_image("panorama.jpg")

# Split GIF across grid
grid.fill_gif("animation.gif")

# Split video across grid
grid.fill_video("movie.mp4")
```

## Example: Image Gallery

```python
import window_art as wa

images = ["photo1.jpg", "photo2.jpg", "photo3.jpg"]

with wa.run():
    win = wa.window(100, 100, 600, 400)

    for image in images:
        win.image = image
        wa.fade_in(win, duration=0.5)
        wa.wait(2)
        wa.fade_out(win, duration=0.5)
```

## Example: GIF with Controls

```python
import window_art as wa

with wa.run():
    win = wa.window(100, 100, 400, 300, gif="animation.gif")

    # Play for 3 seconds
    wa.wait(3)

    # Pause
    win.gif_playing = False
    wa.wait(1)

    # Step through frames manually
    for i in range(win.gif_frame_count):
        win.gif_frame = i
        wa.wait(0.1)

    # Resume at 2x speed
    win.gif_speed = 2.0
    win.gif_playing = True
    wa.wait(3)
```

## Example: Video Player

```python
import window_art as wa

with wa.run():
    win = wa.window(100, 100, 800, 450, video="movie.mp4")

    # Play for 10 seconds
    wa.wait(10)

    # Skip forward
    win.video_position = win.video_position + 30

    # Play at half speed
    win.video_speed = 0.5
    wa.wait(5)

    # Jump to near the end
    win.video_position = win.video_duration - 10
    wa.wait(10)
```

## Performance Considerations

- **Images**: Fastest, loaded once into GPU texture
- **GIFs**: Moderate, each frame decoded on demand
- **Videos**: Most demanding, continuous frame decoding

For best performance with video:
- Use lower resolutions when possible
- Avoid too many simultaneous video windows
- Consider the `video_speed` property to reduce decode frequency
