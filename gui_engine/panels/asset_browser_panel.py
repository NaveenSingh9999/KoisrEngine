from koisrgui.widgets.panel import Panel
from koisrgui.widgets.label import Label

class AssetBrowserPanel(Panel):
    def __init__(self, *args, engine=None, style=None, **kwargs):
        super().__init__(*args, title="Assets", style=style, **kwargs)
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
