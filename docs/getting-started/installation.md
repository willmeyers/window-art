# Installation

## Requirements

- Python 3.10 or higher
- macOS, Linux, or Windows

## Install from PyPI

```bash
pip install window-art
```

## Install from Source

```bash
git clone https://github.com/willmeyers/window-art.git
cd window-art
pip install -e .
```

## Development Installation

For development with testing and type checking:

```bash
pip install -e ".[dev]"
```

This installs additional dependencies:

- `pytest` - Testing framework
- `mypy` - Static type checker

## Dependencies

window-art automatically installs these dependencies:

| Package | Purpose |
|---------|---------|
| `pysdl2` | Core window management via SDL2 |
| `pysdl2-dll` | Pre-built SDL2 binaries |
| `pillow` | Image and GIF support |
| `opencv-python` | Video playback support |

## Verify Installation

```python
import window_art as wa

with wa.run():
    win = wa.window(100, 100, 200, 200, color="green")
    wa.wait(1)
```

If a green window appears for 1 second, the installation is successful.

## Platform-Specific Notes

### macOS

On macOS, window-art uses Cocoa integration for:

- Window shadows (`shadow=True/False`)
- Proper event handling
- Multiple monitor support

### Linux

Ensure SDL2 development libraries are available. On most distributions, `pysdl2-dll` handles this automatically.

### Windows

Works out of the box with `pysdl2-dll` providing the necessary binaries.

## Troubleshooting

### "No module named 'sdl2'"

Ensure pysdl2 is installed:

```bash
pip install pysdl2 pysdl2-dll
```

### Windows Don't Appear

Check that your display server is running (X11 on Linux, Quartz on macOS). On headless servers, a display is required.

### Permission Issues (macOS)

If windows appear but don't respond, grant "Accessibility" permissions to your terminal in System Preferences > Security & Privacy > Privacy > Accessibility.
