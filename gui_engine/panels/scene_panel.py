from koisrgui.widgets.panel import Panel
from koisrgui.widgets.label import Label
from koisrgui.widgets.button import Button

class ScenePanel(Panel):
    def __init__(self, *args, engine=None, style=None, **kwargs):
        super().__init__(*args, title="Scene", style=style, **kwargs)
        self.engine = engine
        self.selected_id = None
        self._build_ui()

    def _build_ui(self):
        self.children.clear()
        if self.engine:
            y_offset = self.y + 32
            for obj in self.engine.get_game_objects():
                btn = Button(self.x + 8, y_offset, self.width - 16, 28, obj.name, on_click=lambda o=obj: self.select_object(o))
                self.add_child(btn)
                y_offset += 36

    def select_object(self, obj):
        self.selected_id = obj.id
        # Notify global state or InspectorPanel (to be implemented)
        if hasattr(self.engine, 'selected_object'):
            self.engine.selected_object = obj
        self._build_ui()

    def update(self, dt):
        self._build_ui()
        for child in self.children:
            child.update(dt)

    def draw(self, surface):
        super().draw(surface)
