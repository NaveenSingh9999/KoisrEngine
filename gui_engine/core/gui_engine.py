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
        self.layout_manager = LayoutManager(self.gui, self.state, engine=self.engine)
        self._build_editor_layout()
        print('[DEBUG] GuiEngine.__init__ finished')

    def _build_editor_layout(self):
        # Use LayoutManager to build the main editor layout
        self.layout_manager.load_default_layout()
        # Collect all panels for toggling
        # The layout_manager creates the panels, so we need to find them in the layout tree
        self._collect_panels(self.layout_manager.root_layout)
        # Add Window menu for toggling panels
        self._add_window_menu()

    def _collect_panels(self, widget):
        # Recursively collect all panels by type
        from gui_engine.panels import ScenePanel, InspectorPanel, AssetBrowserPanel, ConsolePanel, GameViewportPanel, ToolbarPanel
        if isinstance(widget, ScenePanel):
            self.panels['scene'] = widget
        elif isinstance(widget, InspectorPanel):
            self.panels['inspector'] = widget
        elif isinstance(widget, AssetBrowserPanel):
            self.panels['assets'] = widget
        elif isinstance(widget, ConsolePanel):
            self.panels['console'] = widget
        elif isinstance(widget, GameViewportPanel):
            self.panels['game_view'] = widget
        elif isinstance(widget, ToolbarPanel):
            self.panels['toolbar'] = widget
        for child in getattr(widget, 'children', []):
            self._collect_panels(child)

    def _add_window_menu(self):
        # Simple floating menu for toggling panel visibility
        menu_panel = Panel(10, 10, 140, 220, title="Window")
        y = 40
        for key, panel in self.panels.items():
            def make_toggle(panel=panel):
                return lambda: self._toggle_panel(panel)
            btn = Button(20, y, 100, 28, f"{key.title()}", on_click=make_toggle(panel))
            menu_panel.add_child(btn)
            y += 36
        self.gui.add_widget(menu_panel)

    def _toggle_panel(self, panel):
        panel.visible = not panel.visible

    def update(self, dt):
        if self.engine:
            self.engine.update(dt)
        self.layout_manager.update(dt)
        self.gui.update(dt)

    def draw(self):
        self.layout_manager.draw(self.screen)
        self.gui.draw()

    def handle_event(self, event):
        self.layout_manager.handle_event(event)
        self.gui.handle_event(event)
