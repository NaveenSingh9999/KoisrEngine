import json
from koisrgui.core.manager import GUIManager
from gui_engine.layout.layout_manager import LayoutManager
from gui_engine.state.global_state import GlobalState
from gui_engine.panels import ScenePanel, InspectorPanel, AssetBrowserPanel, ConsolePanel, GameViewportPanel, ToolbarPanel
from koisrgui.layouts.horizontal import HorizontalLayout
from koisrgui.layouts.vertical import VerticalLayout
from koisrgui.widgets.panel import Panel
from koisrgui.widgets.button import Button
from koisrgui.widgets.label import Label
import webbrowser

class GuiEngine:
    def __init__(self, screen, layout_config_path=None, engine=None):
        print('[DEBUG] GuiEngine.__init__ called')
        self.screen = screen
        self.engine = engine
        self.gui = GUIManager(screen)
        self.state = GlobalState()
        self.panels = {}
        self._build_editor_layout()
        print('[DEBUG] GuiEngine.__init__ finished')

    def _build_editor_layout(self):
        # --- Toolbar (top) ---
        toolbar = ToolbarPanel(0, 0, 1200, 40, engine=self.engine)
        self.panels['toolbar'] = toolbar

        # --- Main horizontal split ---
        main_split = HorizontalLayout(0, 40)

        # --- Scene Panel (left) ---
        scene_panel = ScenePanel(0, 40, 220, 600, engine=self.engine)
        self.panels['scene'] = scene_panel

        # --- Center vertical split (Game Viewport + Console) ---
        center_split = VerticalLayout(220, 40)
        game_view = GameViewportPanel(220, 40, 760, 400, engine=self.engine)
        self.panels['game_view'] = game_view
        # Console panel (bottom of center)
        console_panel = ConsolePanel(220, 440, 760, 120, engine=self.engine)
        self.panels['console'] = console_panel
        center_split.add_child(game_view)
        center_split.add_child(console_panel)

        # --- Right vertical split (Inspector + Assets) ---
        right_split = VerticalLayout(980, 40)
        inspector_panel = InspectorPanel(980, 40, 220, 300, engine=self.engine)
        self.panels['inspector'] = inspector_panel
        asset_browser = AssetBrowserPanel(980, 340, 220, 220, engine=self.engine)
        self.panels['assets'] = asset_browser
        right_split.add_child(inspector_panel)
        right_split.add_child(asset_browser)

        # --- Assemble main split ---
        main_split.add_child(scene_panel)
        main_split.add_child(center_split)
        main_split.add_child(right_split)

        # --- Root vertical layout ---
        self.root_layout = VerticalLayout(0, 0)
        self.root_layout.add_child(toolbar)
        self.root_layout.add_child(main_split)
        self.gui.add_widget(self.root_layout)

        # --- Window menu for toggling panels ---
        self._add_window_menu()

    def _add_window_menu(self):
        # Simple top-left menu for toggling panels
        menu_panel = Panel(10, 10, 120, 200, title="Window")
        y = 40
        for key, panel in self.panels.items():
            def make_toggle(panel=panel):
                return lambda: self._toggle_panel(panel)
            btn = Button(20, y, 80, 28, f"{key.title()}", on_click=make_toggle(panel()))
            menu_panel.add_child(btn)
            y += 36
        self.gui.add_widget(menu_panel)

    def _toggle_panel(self, panel):
        panel.visible = not panel.visible

    def update(self, dt):
        if self.engine:
            self.engine.update(dt)
        self.root_layout.update(dt)
        self.gui.update(dt)

    def draw(self):
        self.root_layout.draw(self.screen)
        self.gui.draw()

    def handle_event(self, event):
        self.root_layout.handle_event(event)
        self.gui.handle_event(event)
