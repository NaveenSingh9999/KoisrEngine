from koisrgui.widgets.panel import Panel
from koisrgui.widgets.label import Label
from koisrgui.widgets.button import Button

class InspectorPanel(Panel):
    def __init__(self, x, y, width, height, engine=None, style=None):
        super().__init__(x, y, width, height, title="Inspector", style=style)
        self.engine = engine
        self._build_ui()
    def _build_ui(self):
        self.children.clear()
        obj = getattr(self.engine, 'selected_object', None)
        if obj:
            self.add_child(Label(self.x + 8, self.y + 32, 180, 24, f"Name: {obj.name}"))
            t = obj.transform
            # Position
            self.add_child(Label(self.x + 8, self.y + 64, 60, 24, "Position:"))
            for i, axis in enumerate('XYZ'):
                self.add_child(Label(self.x + 80 + i*60, self.y + 64, 40, 24, f"{t.position[i]:.2f}"))
            # Rotation
            self.add_child(Label(self.x + 8, self.y + 96, 60, 24, "Rotation:"))
            for i, axis in enumerate('XYZ'):
                self.add_child(Label(self.x + 80 + i*60, self.y + 96, 40, 24, f"{t.rotation[i]:.2f}"))
            # Scale
            self.add_child(Label(self.x + 8, self.y + 128, 60, 24, "Scale:"))
            for i, axis in enumerate('XYZ'):
                self.add_child(Label(self.x + 80 + i*60, self.y + 128, 40, 24, f"{t.scale[i]:.2f}"))
        else:
            self.add_child(Label(self.x + 8, self.y + 32, 180, 24, "No object selected"))
    def update(self, dt):
        self._build_ui()
        for child in self.children:
            child.update(dt)
    def draw(self, surface):
        super().draw(surface)
