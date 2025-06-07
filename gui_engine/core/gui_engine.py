import json
import pygame
from koisrgui.core.manager import GUIManager
from gui_engine.layout.layout_manager import LayoutManager
from gui_engine.state.global_state import GlobalState
from koisrgui.layouts.horizontal import HorizontalLayout
from koisrgui.layouts.vertical import VerticalLayout
from koisrgui.widgets.panel import Panel
from koisrgui.widgets.button import Button
from koisrgui.widgets.label import Label
from koisrgui.themes.dark import DARK_THEME
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
        self._add_window_menu()
        print('[DEBUG] GuiEngine.__init__ finished')

    def _build_editor_layout(self):
        # Use LayoutManager to build the main editor layout
        self.layout_manager.load_default_layout()
        # Store reference to panels
        self.panels = self.layout_manager.panels
        
    def _add_window_menu(self):
        # Add Window menu for toggling panels
        menu_panel = Panel(10, 10, 140, 220, title="Window", style=DARK_THEME)
        menu_panel.visible = False  # Hidden by default
        
        # Add toggle button in toolbar
        if 'toolbar' in self.panels:
            toolbar = self.panels['toolbar']
            window_btn = Button(toolbar.x + 120, toolbar.y + 8, 80, 24, "Window", 
                              on_click=lambda: self._toggle_window_menu(menu_panel))
            toolbar.add_child(window_btn)
        
        # Add panel toggle buttons
        y = 40
        for key, panel in self.panels.items():
            if key != 'toolbar':  # Skip toolbar in the window menu
                label = key.replace('_', ' ').title()
                btn = Button(20, y, 100, 28, label, 
                           on_click=lambda p=panel: self._toggle_panel(p))
                menu_panel.add_child(btn)
                y += 36
        
        self.gui.add_widget(menu_panel)
        self.window_menu = menu_panel

    def _toggle_window_menu(self, menu_panel):
        menu_panel.visible = not menu_panel.visible

    def _toggle_panel(self, panel):
        panel.visible = not panel.visible

    def update(self, dt):
        if self.engine:
            self.engine.update(dt)
        self.layout_manager.update(dt)
        self.gui.update(dt)

    def draw(self):
        # Fill background
        self.screen.fill((30, 30, 30))
        # Draw layout
        self.layout_manager.draw(self.screen)
        # Draw GUI widgets
        self.gui.draw()

    def handle_event(self, event):
        # First try to handle with layout manager (which handles docking)
        if not self.layout_manager.handle_event(event):
            # If not handled by layout, pass to GUI manager
            self.gui.handle_event(event)
