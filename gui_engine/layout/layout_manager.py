import json
from gui_engine.panels.scene_panel import ScenePanel, InspectorPanel, AssetBrowserPanel, ConsolePanel, GameViewportPanel
from koisrgui.layouts.horizontal import HorizontalLayout
from koisrgui.layouts.vertical import VerticalLayout

class LayoutManager:
    def __init__(self, gui, state, engine):
        self.gui = gui
        self.state = state
        self.engine = engine
        self.root_layout = None

    def load_layout(self, path):
        with open(path, 'r') as f:
            layout_cfg = json.load(f)
        self.root_layout = self._parse_layout(layout_cfg)
        self.gui.add_widget(self.root_layout)

    def load_default_layout(self):
        # Real editor layout with all panels
        from gui_engine.panels.scene_panel import ScenePanel
        from gui_engine.panels.inspector_panel import InspectorPanel
        from gui_engine.panels.asset_browser_panel import AssetBrowserPanel
        from gui_engine.panels.console_panel import ConsolePanel
        from gui_engine.panels.game_viewport_panel import GameViewportPanel
        from gui_engine.panels.toolbar_panel import ToolbarPanel
        from koisrgui.layouts.horizontal import HorizontalLayout
        from koisrgui.layouts.vertical import VerticalLayout
        # Top toolbar
        toolbar = ToolbarPanel(self.engine, 0, 0, 1200, 40)
        # Main split
        left = ScenePanel(self.engine, 0, 40, 200, 600)
        center = GameViewportPanel(self.engine, 200, 40, 800, 480)
        right = InspectorPanel(self.engine, 1000, 40, 200, 600)
        bottom_left = AssetBrowserPanel(self.engine, 0, 640, 600, 160)
        bottom_right = ConsolePanel(self.engine, 600, 640, 600, 160)
        # Add to GUI
        self.gui.add_widget(toolbar)
        self.gui.add_widget(left)
        self.gui.add_widget(center)
        self.gui.add_widget(right)
        self.gui.add_widget(bottom_left)
        self.gui.add_widget(bottom_right)

    def _parse_layout(self, cfg):
        # TODO: Parse layout config to build layout tree
        pass

    def update(self, dt):
        if self.root_layout:
            self.root_layout.update(dt)

    def draw(self, surface):
        if self.root_layout:
            self.root_layout.draw(surface)

    def handle_event(self, event):
        if self.root_layout:
            self.root_layout.handle_event(event)
