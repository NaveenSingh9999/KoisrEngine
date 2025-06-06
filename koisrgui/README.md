# koisrgui - Custom Python GUI Framework for Game Engine

A modular, OpenGL-accelerated GUI framework for Python game engines.

## Features
- Widget-based architecture (Button, Label, InputField, Panel, etc.)
- OpenGL rendering (via PyOpenGL)
- Pygame windowing and input
- Style/theme system
- Text rendering (Pygame font, Freetype planned)
- Event system (mouse, keyboard, focus, drag, scroll)
- Layouts (horizontal, vertical, nested)
- Embeddable in custom OpenGL/game loops

## Quick Start

```python
import pygame
from koisrgui.core.manager import GUIManager
from koisrgui.widgets.button import Button

pygame.init()
screen = pygame.display.set_mode((800, 600), pygame.OPENGL | pygame.DOUBLEBUF)
gui = GUIManager(screen)

btn = Button(100, 100, 120, 40, "Click Me", on_click=lambda: print("Clicked!"))
gui.add_widget(btn)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        gui.handle_event(event)
    gui.update()
    gui.draw()
    pygame.display.flip()
```

See `examples/` for more.

## Directory Structure
- `koisrgui/core/` — Core classes (Widget, GUIManager, events, style)
- `koisrgui/widgets/` — Built-in widgets
- `koisrgui/themes/` — Theme definitions
- `koisrgui/fonts/` — Font utilities
- `koisrgui/layouts/` — Layout managers
- `examples/` — Example apps
- `tests/` — Unit tests

## License
MIT
