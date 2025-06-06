from koisrgui.widgets.panel import Panel

class GameViewportPanel(Panel):
    def __init__(self, *args, engine=None, style=None, **kwargs):
        super().__init__(*args, title="Game View", style=style, **kwargs)
        self.engine = engine

    def draw(self, surface):
        # The engine's renderer will already have drawn to the OpenGL context
        # Optionally, draw overlays or UI here
        super().draw(surface)
