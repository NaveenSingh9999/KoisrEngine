from koisrgui.widgets.panel import Panel
from koisrgui.widgets.button import Button

class ToolbarPanel(Panel):
    def __init__(self, engine, *args, **kwargs):
        super().__init__(title=None, *args, **kwargs)
        self.engine = engine
        self._build_ui()
    def _build_ui(self):
        self.children.clear()
        x = self.x + 8
        y = self.y + 8
        self.add_child(Button(x, y, 80, 32, "Add Cube", on_click=self.add_cube))
        self.add_child(Button(x+90, y, 80, 32, "Add Plane", on_click=self.add_plane))
        self.add_child(Button(x+180, y, 80, 32, "Play", on_click=self.toggle_play))
    def add_cube(self):
        from engine.game_object import GameObject
        obj = GameObject("Cube")
        obj.set_mesh('cube')
        self.engine.add_game_object(obj)
    def add_plane(self):
        from engine.game_object import GameObject
        obj = GameObject("Plane")
        obj.set_mesh('plane')
        self.engine.add_game_object(obj)
    def toggle_play(self):
        if getattr(self.engine, 'running', False):
            self.engine.stop_runtime()
        else:
            self.engine.play()
    def update(self, dt):
        self._build_ui()
        super().update(dt)
