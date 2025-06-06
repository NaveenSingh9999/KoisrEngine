from koisrgui.widgets.panel import Panel
from koisrgui.widgets.label import Label

class AssetBrowserPanel(Panel):
    def __init__(self, x, y, width, height, engine=None, style=None):
        super().__init__(x, y, width, height, title="Assets", style=style)
        self.engine = engine
        self._build_ui()

    def _build_ui(self):
        self.children.clear()
        self.add_child(Label(self.x + 8, self.y + 32, self.width - 16, 24, "Asset list will appear here."))

    def update(self, dt):
        self._build_ui()
        for child in self.children:
            child.update(dt)

    def draw(self, surface):
        super().draw(surface)
