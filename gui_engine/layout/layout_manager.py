import json
import pygame
from gui_engine.layout.dock_manager import DockManager
from koisrgui.widgets.dockable_panel import DockablePanel
from koisrgui.layouts.horizontal import HorizontalLayout
from koisrgui.layouts.vertical import VerticalLayout
from koisrgui.widgets.panel import Panel
from koisrgui.widgets.label import Label
from koisrgui.themes.dark import DARK_THEME
from gui_engine.panels.scene_panel import ScenePanel
from gui_engine.panels.game_viewport_panel import GameViewportPanel
from gui_engine.panels.inspector_panel import InspectorPanel
from gui_engine.panels.asset_browser_panel import AssetBrowserPanel
from gui_engine.panels.console_panel import ConsolePanel
from gui_engine.panels.toolbar_panel import ToolbarPanel

class LayoutManager:
    def __init__(self, gui, state, engine=None):
        self.gui = gui
        self.state = state
        self.engine = engine
        self.screen_width = 1200
        self.screen_height = 800
        self.toolbar_height = 40
        self.status_bar_height = 20
        self.root_layout = None
        self.dock_manager = None
        self.panels = {}

    def load_layout(self, path):
        with open(path, 'r') as f:
            layout_cfg = json.load(f)
        self.root_layout = self._parse_layout(layout_cfg)
        self.gui.add_widget(self.root_layout)

    def load_default_layout(self):
        print('[DEBUG] LayoutManager.load_default_layout called')
        
        # Initialize dock manager
        self.dock_manager = DockManager(
            self.screen_width, 
            self.screen_height,
            self.toolbar_height, 
            self.status_bar_height
        )
        
        # Background panel for the entire editor area
        bg_panel = Panel(0, 0, self.screen_width, self.screen_height, title=None, 
                       style={**DARK_THEME, 'bg': (30, 30, 30)})
        self.gui.add_widget(bg_panel)
        
        # Create dockable panels
        
        # Toolbar panel (top)
        toolbar = ToolbarPanel(
            0, 0, 
            self.screen_width, self.toolbar_height, 
            engine=self.engine
        )
        
        # Scene Hierarchy panel (left)
        scene_panel = DockablePanel(
            0, self.toolbar_height, 
            int(self.screen_width * 0.2), int(self.screen_height * 0.6),
            title="Scene Hierarchy", 
            engine=self.engine,
            style=DARK_THEME
        )
        scene_hierarchy = ScenePanel(
            10, scene_panel.header_height + 10, 
            scene_panel.width - 20, scene_panel.height - scene_panel.header_height - 20, 
            engine=self.engine
        )
        scene_panel.add_child(scene_hierarchy)
        
        # Game Viewport panel (center)
        game_viewport_panel = DockablePanel(
            int(self.screen_width * 0.2), self.toolbar_height, 
            int(self.screen_width * 0.55), int(self.screen_height * 0.6),
            title="Game View", 
            engine=self.engine,
            style=DARK_THEME
        )
        game_viewport = GameViewportPanel(
            10, game_viewport_panel.header_height + 10, 
            game_viewport_panel.width - 20, game_viewport_panel.height - game_viewport_panel.header_height - 20, 
            engine=self.engine
        )
        game_viewport_panel.add_child(game_viewport)
        
        # Inspector panel (right)
        inspector_panel = DockablePanel(
            int(self.screen_width * 0.75), self.toolbar_height, 
            int(self.screen_width * 0.25), int(self.screen_height * 0.6),
            title="Inspector", 
            engine=self.engine,
            style=DARK_THEME
        )
        inspector = InspectorPanel(
            10, inspector_panel.header_height + 10, 
            inspector_panel.width - 20, inspector_panel.height - inspector_panel.header_height - 20, 
            engine=self.engine
        )
        inspector_panel.add_child(inspector)
        
        # Asset Browser panel (bottom)
        asset_panel = DockablePanel(
            0, int(self.screen_height * 0.7), 
            self.screen_width, int(self.screen_height * 0.25),
            title="Asset Browser", 
            engine=self.engine,
            style=DARK_THEME
        )
        asset_browser = AssetBrowserPanel(
            10, asset_panel.header_height + 10, 
            asset_panel.width - 20, asset_panel.height - asset_panel.header_height - 20, 
            engine=self.engine
        )
        asset_panel.add_child(asset_browser)
        
        # Console panel (as a tab in bottom area)
        console_panel = DockablePanel(
            0, int(self.screen_height * 0.7), 
            self.screen_width, int(self.screen_height * 0.25),
            title="Console", 
            engine=self.engine,
            style=DARK_THEME
        )
        console = ConsolePanel(
            10, console_panel.header_height + 10, 
            console_panel.width - 20, console_panel.height - console_panel.header_height - 20, 
            engine=self.engine
        )
        console_panel.add_child(console)
        
        # Store panels for reference
        self.panels = {
            'toolbar': toolbar,
            'scene': scene_panel,
            'game_view': game_viewport_panel,
            'inspector': inspector_panel,
            'asset_browser': asset_panel,
            'console': console_panel
        }
        
        # Add panels to dock manager
        self.dock_manager.add_panel(toolbar, 'top')
        self.dock_manager.add_panel(scene_panel, 'left')
        self.dock_manager.add_panel(game_viewport_panel, 'center')
        self.dock_manager.add_panel(inspector_panel, 'right')
        self.dock_manager.add_panel(asset_panel, 'bottom')
        self.dock_manager.add_panel(console_panel, 'bottom')  # Will be in tabs with asset browser
        
        # Status bar at the bottom
        status_bar = Panel(
            0, self.screen_height - self.status_bar_height,
            self.screen_width, self.status_bar_height,
            title=None,
            style={**DARK_THEME, 'bg': (40, 40, 40)}
        )
        status_label = Label(
            10, self.screen_height - self.status_bar_height + 2,
            300, 16,
            "KoisrEngine Ready",
            style={**DARK_THEME, 'font_size': 14}
        )
        status_bar.add_child(status_label)
        
        # Add status bar to GUI
        self.gui.add_widget(status_bar)
        
        print('[DEBUG] LayoutManager.load_default_layout finished')

    def _parse_layout(self, cfg):
        # TODO: Parse layout config to build layout tree
        pass

    def handle_event(self, event):
        if self.dock_manager:
            return self.dock_manager.handle_event(event)
        return False

    def update(self, dt):
        # Update panels
        for panel in self.panels.values():
            panel.update(dt)

    def draw(self, surface):
        # Draw the dock manager (which will draw all docked panels)
        if self.dock_manager:
            print(f"[DEBUG] LayoutManager.draw() calling dock_manager.draw()")
            self.dock_manager.draw(surface)
            
            # Additional drawing for debug visualization
            import pygame
            for name, panel in self.panels.items():
                # Draw a box around each panel for debugging
                if panel.visible:
                    pygame.draw.rect(
                        surface, 
                        (255, 0, 0), 
                        (panel.x, panel.y, panel.width, panel.height), 
                        1
                    )
                    print(f"[DEBUG] Panel '{name}' at ({panel.x}, {panel.y}, {panel.width}, {panel.height})")

