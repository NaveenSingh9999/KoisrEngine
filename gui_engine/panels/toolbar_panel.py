from koisrgui.widgets.panel import Panel
from koisrgui.widgets.button import Button

class ToolbarPanel(Panel):
    def __init__(self, x, y, width, height, engine=None, style=None):
        super().__init__(x, y, width, height, title=None, style=style)
        self.engine = engine
        self._build_ui()
    def _build_ui(self):
        self.children.clear()
        # Add Cube
        self.add_child(Button(self.x + 8, self.y + 4, 100, 32, "Add Cube", on_click=self.add_cube))
        # Add Plane
        self.add_child(Button(self.x + 120, self.y + 4, 100, 32, "Add Plane", on_click=self.add_plane))
        # Play/Stop
        play_label = "Stop" if getattr(self.engine, 'running', False) else "Play"
        self.add_child(Button(self.x + 240, self.y + 4, 100, 32, play_label, on_click=self.toggle_play))
    def add_cube(self):
        from engine.game_object import GameObject
        obj = GameObject("Cube")
        obj.mesh = 'cube'
        obj.transform.position = [0, 0, 0]
        self.engine.add_game_object(obj)
        print("[Toolbar] Added Cube")
    def add_plane(self):
        from engine.game_object import GameObject
        obj = GameObject("Plane")
        obj.mesh = 'plane'
        obj.transform.position = [0, -1, 0]
        self.engine.add_game_object(obj)
        print("[Toolbar] Added Plane")
    def toggle_play(self):
        if self.engine.running:
            self.engine.stop()
            print("[Toolbar] Stopped engine runtime")
        else:
            self.engine.start()
            print("[Toolbar] Started engine runtime")
        self._build_ui()
    def update(self, dt):
        self._build_ui()
        for child in self.children:
            child.update(dt)
    def draw(self, surface):
        super().draw(surface)
