from koisrgui.widgets.panel import Panel

class GameViewportPanel(Panel):
    def __init__(self, x, y, width, height, engine=None, style=None):
        super().__init__(x, y, width, height, title="Game View", style=style)
        self.engine = engine

    def draw(self, surface):
        # The engine's renderer will already have drawn to the OpenGL context
        # Optionally, draw overlays or UI here
        super().draw(surface)
