from koisrgui.widgets.panel import Panel
from koisrgui.widgets.label import Label

class ConsolePanel(Panel):
    def __init__(self, *args, engine=None, style=None, **kwargs):
        super().__init__(*args, title="Console", style=style, **kwargs)
        self.engine = engine
        self._build_ui()
    def _build_ui(self):
        self.children.clear()
        # For now, show a static message or engine log if available
        self.add_child(Label(self.x + 8, self.y + 32, self.width - 16, 24, "Console output will appear here."))
    def update(self, dt):
        self._build_ui()
        for child in self.children:
            child.update(dt)
    def draw(self, surface):
        super().draw(surface)
