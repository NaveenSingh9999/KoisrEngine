import json
from gui_engine.panels.scene_panel import ScenePanel, InspectorPanel, AssetBrowserPanel, ConsolePanel, GameViewportPanel
from koisrgui.layouts.horizontal import HorizontalLayout
from koisrgui.layouts.vertical import VerticalLayout

class LayoutManager:
    def __init__(self, gui, state):
        self.gui = gui
        self.state = state
        self.root_layout = None

    def load_layout(self, path):
        with open(path, 'r') as f:
            layout_cfg = json.load(f)
        self.root_layout = self._parse_layout(layout_cfg)
        self.gui.add_widget(self.root_layout)

    def load_default_layout(self):
        # Hardcoded default layout for now
        self.root_layout = HorizontalLayout([
            ScenePanel(width=200),
            VerticalLayout([
                GameViewportPanel(),
                ConsolePanel(height=120)
            ]),
            VerticalLayout([
                InspectorPanel(height=300),
                AssetBrowserPanel(height=200)
            ], width=250)
        ])
        self.gui.add_widget(self.root_layout)

    def _parse_layout(self, cfg):
        # TODO: Parse layout config to build layout tree
        pass

    def update(self, dt):
        if self.root_layout:
            self.root_layout.update(dt)

    def draw(self):
        if self.root_layout:
            self.root_layout.draw()

    def handle_event(self, event):
        if self.root_layout:
            self.root_layout.handle_event(event)
