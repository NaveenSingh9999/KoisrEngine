from koisrgui.widgets.panel import Panel
from koisrgui.widgets.label import Label

class AssetBrowserPanel(Panel):
    def __init__(self, engine, *args, **kwargs):
        super().__init__(title="Assets", *args, **kwargs)
        self.engine = engine
        self._build_ui()
    def _build_ui(self):
        self.children.clear()
        # TODO: Integrate with real asset manager
        y = self.y + 32
        self.add_child(Label(self.x + 8, y, self.width - 16, 28, "(No assets yet)"))
    def update(self, dt):
        self._build_ui()
        super().update(dt)
