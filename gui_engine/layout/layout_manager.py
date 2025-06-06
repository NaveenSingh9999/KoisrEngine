import json
from gui_engine.panels import *
from koisrgui.layouts.horizontal import HorizontalLayout
from koisrgui.layouts.vertical import VerticalLayout

class LayoutManager:
    def __init__(self, gui, state, engine=None):
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
        # Main editor layout: Toolbar (top), Scene (left), Game View (center), Inspector (right), Asset/Console (bottom)
        self.root_layout = VerticalLayout(0, 0)
        toolbar = ToolbarPanel(0, 0, 1200, 40, engine=self.engine)
        main_split = HorizontalLayout(0, 40)
        scene_panel = ScenePanel(0, 40, 220, 600, engine=self.engine)
        center_split = VerticalLayout(220, 40)
        game_view = GameViewportPanel(220, 40, 760, 400, engine=self.engine)
        console_panel = ConsolePanel(220, 440, 760, 120, engine=self.engine)
        right_split = VerticalLayout(980, 40)
        inspector_panel = InspectorPanel(980, 40, 220, 300, engine=self.engine)
        asset_browser = AssetBrowserPanel(980, 340, 220, 220, engine=self.engine)
        right_split.add_child(inspector_panel)
        right_split.add_child(asset_browser)
        center_split.add_child(game_view)
        center_split.add_child(console_panel)
        main_split.add_child(scene_panel)
        main_split.add_child(center_split)
        main_split.add_child(right_split)
        self.root_layout.add_child(toolbar)
        self.root_layout.add_child(main_split)
        self.gui.add_widget(self.root_layout)

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
