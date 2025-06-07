from koisrgui.widgets.panel import Panel
from koisrgui.widgets.label import Label
from koisrgui.widgets.button import Button

class AssetBrowserPanel(Panel):
    def __init__(self, x, y, width=None, height=None, title=None, engine=None, style=None):
        super().__init__(x, y, width, height, title=title or "Assets", style=style)
        self.engine = engine
        self.current_folder = "assets"  # Current folder being viewed
        self.selected_asset = None
        self.view_mode = "grid"  # "grid" or "list"
        self._build_ui()

    def _build_ui(self):
        self.children.clear()
        
        # Top toolbar with navigation and view options
        # Back button
        self.add_child(Button(self.x + 8, self.y + 32, 30, 24, "←", on_click=self._go_back))
        
        # Current path
        self.add_child(Label(self.x + 44, self.y + 32, 200, 24, f"/{self.current_folder}"))
        
        # View mode toggle
        view_btn = Button(self.x + self.width - 40, self.y + 32, 30, 24, 
                        "□" if self.view_mode == "grid" else "≡", 
                        on_click=self._toggle_view_mode)
        self.add_child(view_btn)
        
        # Import button
        import_btn = Button(self.x + self.width - 120, self.y + 32, 70, 24, 
                           "Import", on_click=self._import_asset)
        self.add_child(import_btn)
        
        # Create button
        create_btn = Button(self.x + self.width - 200, self.y + 32, 70, 24, 
                           "Create", on_click=self._create_asset)
        self.add_child(create_btn)
        
        # Tab system for Assets/Console
        self.add_child(Button(self.x + 8, self.y + 8, 80, 24, "Assets", 
                             style={'bg': (70, 70, 80), 'fg': (220, 220, 220)}))
        self.add_child(Button(self.x + 96, self.y + 8, 80, 24, "Console", 
                             on_click=self._switch_to_console,
                             style={'bg': (50, 50, 60), 'fg': (180, 180, 180)}))
        
        # Asset grid/list
        y_offset = self.y + 64
        
        # Show sample assets
        mock_assets = [
            {"name": "cube.obj", "type": "model"},
            {"name": "player.png", "type": "texture"},
            {"name": "level1.scene", "type": "scene"},
            {"name": "ambient.wav", "type": "audio"},
            {"name": "material.mat", "type": "material"},
        ]
        
        if self.view_mode == "grid":
            # Grid view
            grid_size = 80
            grid_padding = 10
            items_per_row = (self.width - 16) // (grid_size + grid_padding)
            
            for i, asset in enumerate(mock_assets):
                row = i // items_per_row
                col = i % items_per_row
                
                x_pos = self.x + 8 + col * (grid_size + grid_padding)
                y_pos = y_offset + row * (grid_size + grid_padding + 20)
                
                # Asset icon (button)
                asset_btn = Button(x_pos, y_pos, grid_size, grid_size, 
                                  self._get_asset_icon(asset["type"]), 
                                  on_click=lambda a=asset: self._select_asset(a))
                self.add_child(asset_btn)
                
                # Asset name
                self.add_child(Label(x_pos, y_pos + grid_size, grid_size, 20, 
                                    asset["name"], 
                                    style={'font_size': 12, 'fg': (200, 200, 200)}))
        else:
            # List view
            for i, asset in enumerate(mock_assets):
                asset_btn = Button(self.x + 8, y_offset + i * 30, self.width - 16, 24, 
                                  f"{self._get_asset_icon(asset['type'])} {asset['name']}", 
                                  on_click=lambda a=asset: self._select_asset(a))
                self.add_child(asset_btn)
    
    def _get_asset_icon(self, asset_type):
        # Return an appropriate icon character based on asset type
        icons = {
            "model": "□",
            "texture": "▣",
            "scene": "♦",
            "audio": "♪",
            "material": "◉",
            "script": "✎",
            "folder": "▤",
        }
        return icons.get(asset_type, "○")
    
    def _go_back(self):
        if "/" in self.current_folder:
            self.current_folder = self.current_folder.rsplit("/", 1)[0]
        self._build_ui()
    
    def _toggle_view_mode(self):
        self.view_mode = "list" if self.view_mode == "grid" else "grid"
        self._build_ui()
    
    def _import_asset(self):
        # In a real implementation, this would open a file dialog
        print("Import asset dialog would appear here")
    
    def _create_asset(self):
        # In a real implementation, this would show a menu of asset types
        print("Create asset menu would appear here")
    
    def _select_asset(self, asset):
        self.selected_asset = asset
        print(f"Selected asset: {asset['name']}")
        # In a real implementation, this would update the inspector panel
    
    def _switch_to_console(self):
        # In a real implementation, this would switch the tab to show the console
        print("Switching to console view")

    def update(self, dt):
        for child in self.children:
            child.update(dt)

    def draw(self, surface):
        super().draw(surface)
