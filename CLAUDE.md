# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

A minimal Python library for live coding visual scenes using desktop windows. Creates, animates, and manipulates colored desktop windows with smooth animations and easing functions.

## Commands

```bash
# Install for development
pip install -e ".[dev]"

# Type checking (strict mode)
mypy window_art

# Run examples
python examples/basic.py
python examples/dvd_bounce.py
```

## Architecture

**Singleton Pattern:** `Desktop.get()` manages SDL2 initialization, event loop, and window tracking. Auto-initializes on first window creation.

**Immediate-Mode Animation:** Functions like `move()`, `fade()`, `resize()` block until complete. Generator-based engine internally (`_move_gen()`, etc.) with `_async` suffix variants for non-blocking control.

**Dirty Flag Optimization:** Windows use `_position_dirty`, `_size_dirty`, `_opacity_dirty` flags to batch SDL calls in `_apply_changes()`, reducing WindowServer overhead.

**Core Modules:**
- `core.py` - Desktop singleton, SDL init, event loop, `init()`, `quit()`, `window()`, `update()`, `run()`
- `window.py` - Window class wrapping SDL2 windows with property setters
- `animate.py` - Animation generators and blocking wrappers, `parallel()`, `sequence()`
- `color.py` - Color dataclass with CSS name/hex/RGB parsing
- `easing.py` - 24+ easing functions (quad, cubic, elastic, bounce, etc.)
- `vec.py` - vec2 math primitive

**Adding new animations:** Create `_*_gen()` generator in `animate.py`, add blocking wrapper function, export in `__init__.py`.
