from koisrgui.widgets.panel import Panel

class GameViewportPanel(Panel):
    def __init__(self, engine, *args, **kwargs):
        super().__init__(title="Game", *args, **kwargs)
        self.engine = engine
    def draw(self, surface):
        # Render the live game view using OpenGL
        self.engine.render()
        # Optionally, draw overlays/UI here
