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
        # Hardcoded default layout for now, with explicit x, y, width, height
        self.root_layout = HorizontalLayout(0, 0)
        scene_panel = ScenePanel(0, 0, 200, 600)
        center_layout = VerticalLayout(200, 0)
        game_viewport_panel = GameViewportPanel(200, 0, 600, 480)
        console_panel = ConsolePanel(200, 480, 600, 120)
        center_layout.add_child(game_viewport_panel)
        center_layout.add_child(console_panel)
        right_layout = VerticalLayout(800, 0)
        inspector_panel = InspectorPanel(800, 0, 250, 300)
        asset_browser_panel = AssetBrowserPanel(800, 300, 250, 300)
        right_layout.add_child(inspector_panel)
        right_layout.add_child(asset_browser_panel)
        self.root_layout.add_child(scene_panel)
        self.root_layout.add_child(center_layout)
        self.root_layout.add_child(right_layout)
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
