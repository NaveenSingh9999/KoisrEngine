from koisrgui.widgets.dockable_panel import DockablePanel
from koisrgui.widgets.button import Button
from koisrgui.widgets.label import Label

class ToolbarPanel(DockablePanel):
    def __init__(self, *args, engine=None, style=None, **kwargs):
        super().__init__(*args, title="Toolbar", style=style, engine=engine, **kwargs)
        self.engine = engine
        self._build_ui()

    def _build_ui(self):
        self.children.clear()
        
        # Add logo/title
        self.add_child(Label(self.x + 8, self.y + 10, 120, 24, "KoisrEditor", 
                           style={'font_size': 16, 'fg': (220, 220, 220)}))
        
        # Menu bar
        menu_x = self.x + 130
        for menu_item in ["File", "Edit", "View", "Window", "Help"]:
            self.add_child(Button(menu_x, self.y + 8, 60, 24, menu_item, 
                                 on_click=lambda m=menu_item: self._show_menu(m)))
            menu_x += 65
        
        # Separator
        menu_x += 20
        
        # Object manipulation buttons
        self.add_child(Button(menu_x, self.y + 8, 30, 24, "↖", on_click=self._activate_move_tool))
        menu_x += 35
        self.add_child(Button(menu_x, self.y + 8, 30, 24, "↻", on_click=self._activate_rotate_tool))
        menu_x += 35
        self.add_child(Button(menu_x, self.y + 8, 30, 24, "↔", on_click=self._activate_scale_tool))
        
        # Separator
        menu_x += 55
        
        # Add object buttons
        self.add_child(Button(menu_x, self.y + 8, 100, 24, "Add Cube", on_click=self.add_cube))
        menu_x += 105
        self.add_child(Button(menu_x, self.y + 8, 100, 24, "Add Plane", on_click=self.add_plane))
        
        # Separator
        menu_x += 120
        
        # Play/Stop buttons
        play_label = "■" if getattr(self.engine, 'running', False) else "▶"
        self.add_child(Button(menu_x, self.y + 8, 30, 24, play_label, on_click=self.toggle_play))
        
        # Step and pause buttons
        menu_x += 35
        self.add_child(Button(menu_x, self.y + 8, 30, 24, "⏸", on_click=self._pause_game))
        menu_x += 35
        self.add_child(Button(menu_x, self.y + 8, 30, 24, "⏭", on_click=self._step_game))
        
        # Project name in right side
        project_name = getattr(self.engine, 'project_name', "Untitled Project")
        self.add_child(Label(self.x + self.width - 200, self.y + 10, 190, 24, 
                           project_name, 
                           style={'font_size': 14, 'fg': (180, 180, 180)}))

    def _show_menu(self, menu_name):
        print(f"Opening {menu_name} menu")
        # In a full implementation, this would show a dropdown menu
        
    def _activate_move_tool(self):
        print("Activating move tool")
        # Set the current tool mode in the engine
        
    def _activate_rotate_tool(self):
        print("Activating rotate tool")
        
    def _activate_scale_tool(self):
        print("Activating scale tool")
        
    def _pause_game(self):
        print("Pausing game")
        # In a full implementation, this would pause the game without stopping it
        
    def _step_game(self):
        print("Stepping game")
        # In a full implementation, this would advance the game by one frame
        
    def add_cube(self):
        from engine.game_object import GameObject
        obj = GameObject("Cube")
        obj.mesh = 'cube'
        obj.transform.position = [0, 0, 0]
        self.engine.add_game_object(obj)
        print("[Toolbar] Added Cube")

    def add_plane(self):
        from engine.game_object import GameObject
        obj = GameObject("Plane")
        obj.mesh = 'plane'
        obj.transform.position = [0, -1, 0]
        self.engine.add_game_object(obj)
        print("[Toolbar] Added Plane")

    def toggle_play(self):
        if self.engine.running:
            self.engine.stop()
            print("[Toolbar] Stopped engine runtime")
        else:
            self.engine.start()
            print("[Toolbar] Started engine runtime")
        self._build_ui()  # Only rebuild when play state changes

    def update(self, dt):
        for child in self.children:
            child.update(dt)

    def draw(self, surface):
        # Draw base panel
        import pygame
        
        # Draw toolbar background (custom for toolbar)
        pygame.draw.rect(surface, (40, 42, 48), (self.x, self.y, self.width, self.height))
        # Draw separator line at bottom
        pygame.draw.line(surface, (60, 62, 68), (self.x, self.y + self.height - 1), 
                       (self.x + self.width, self.y + self.height - 1), 1)
        
        # Draw children
        for child in self.children:
            child.draw(surface)
