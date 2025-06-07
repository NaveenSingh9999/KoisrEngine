from koisrgui.widgets.panel import Panel
from koisrgui.widgets.button import Button
from koisrgui.widgets.label import Label
import pygame

class GameViewportPanel(Panel):
    def __init__(self, *args, engine=None, style=None, **kwargs):
        super().__init__(*args, title="Game View", style=style, **kwargs)
        self.engine = engine
        self.is_focused = False
        self.current_tool = "select"  # select, move, rotate, scale
        self.gizmo_visible = True
        self.grid_visible = True
        self.stats_visible = True
        self._build_ui()
        
    def _build_ui(self):
        self.children.clear()
        
        # Viewport toolbar buttons
        btn_x = self.x + 8
        btn_y = self.y + 32
        
        # Gizmo toggle
        gizmo_btn = Button(btn_x, btn_y, 80, 24, "Gizmos: ON" if self.gizmo_visible else "Gizmos: OFF",
                         on_click=self._toggle_gizmos)
        self.add_child(gizmo_btn)
        btn_x += 90
        
        # Grid toggle
        grid_btn = Button(btn_x, btn_y, 80, 24, "Grid: ON" if self.grid_visible else "Grid: OFF",
                        on_click=self._toggle_grid)
        self.add_child(grid_btn)
        btn_x += 90
        
        # Camera dropdown (placeholder)
        cam_btn = Button(btn_x, btn_y, 80, 24, "Perspective",
                       on_click=self._toggle_camera)
        self.add_child(cam_btn)
        
        # Stats display (FPS, etc)
        if self.stats_visible:
            fps = getattr(self.engine, 'fps', 60)
            stats_label = Label(self.x + self.width - 100, self.y + 32, 90, 24, f"FPS: {fps}")
            self.add_child(stats_label)
            
            # Object count
            obj_count = len(getattr(self.engine, 'get_game_objects', lambda: [])())
            count_label = Label(self.x + self.width - 200, self.y + 32, 90, 24, f"Objects: {obj_count}")
            self.add_child(count_label)
    
    def _toggle_gizmos(self):
        self.gizmo_visible = not self.gizmo_visible
        self._build_ui()
    
    def _toggle_grid(self):
        self.grid_visible = not self.grid_visible
        self._build_ui()
    
    def _toggle_camera(self):
        # This would toggle between perspective and orthographic in a real implementation
        print("Toggling camera view")
    
    def handle_event(self, event):
        # Check if click is inside the viewport area
        viewport_rect = pygame.Rect(self.x, self.y + 60, self.width, self.height - 60)
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Check if click is inside viewport
            if viewport_rect.collidepoint(event.pos):
                self.is_focused = True
                # Handle viewport interaction
                print(f"Viewport clicked at {event.pos}")
            else:
                self.is_focused = False
        
        # Pass events to children
        super().handle_event(event)
    
    def update(self, dt):
        # Rebuild UI only when necessary, not every frame
        for child in self.children:
            child.update(dt)

    def draw(self, surface):
        # Draw panel background
        super().draw(surface)
        
        # Draw viewport area
        viewport_rect = (self.x + 2, self.y + 60, self.width - 4, self.height - 62)
        pygame.draw.rect(surface, (20, 20, 20), viewport_rect)
        
        # Draw a grid if enabled
        if self.grid_visible:
            grid_color = (40, 40, 40)
            grid_spacing = 20
            
            # Draw horizontal grid lines
            for y in range(self.y + 60 + grid_spacing, self.y + self.height, grid_spacing):
                pygame.draw.line(surface, grid_color, (self.x + 2, y), (self.x + self.width - 2, y))
            
            # Draw vertical grid lines
            for x in range(self.x + 2 + grid_spacing, self.x + self.width - 2, grid_spacing):
                pygame.draw.line(surface, grid_color, (x, self.y + 60), (x, self.y + self.height - 2))
        
        # Draw a sample 3D object (cube) in the center
        center_x = self.x + self.width // 2
        center_y = self.y + 60 + (self.height - 60) // 2
        
        # Draw a simple wireframe cube
        cube_size = 50
        points = [
            (center_x - cube_size, center_y - cube_size),  # Front top left
            (center_x + cube_size, center_y - cube_size),  # Front top right
            (center_x + cube_size, center_y + cube_size),  # Front bottom right
            (center_x - cube_size, center_y + cube_size),  # Front bottom left
            (center_x - cube_size//2, center_y - cube_size//2 - cube_size//4),  # Back top left
            (center_x + cube_size//2, center_y - cube_size//2 - cube_size//4),  # Back top right
            (center_x + cube_size//2, center_y + cube_size//2 - cube_size//4),  # Back bottom right
            (center_x - cube_size//2, center_y + cube_size//2 - cube_size//4),  # Back bottom left
        ]
        
        # Draw cube edges
        lines = [
            (0, 1), (1, 2), (2, 3), (3, 0),  # Front face
            (4, 5), (5, 6), (6, 7), (7, 4),  # Back face
            (0, 4), (1, 5), (2, 6), (3, 7),  # Connecting edges
        ]
        
        for line in lines:
            pygame.draw.line(surface, (100, 180, 255), points[line[0]], points[line[1]], 1)
        
        # Draw gizmos if enabled
        if self.gizmo_visible:
            # Draw XYZ axes at center of viewport
            axis_length = 30
            # X axis (red)
            pygame.draw.line(surface, (255, 0, 0), (center_x, center_y), (center_x + axis_length, center_y), 2)
            # Y axis (green)
            pygame.draw.line(surface, (0, 255, 0), (center_x, center_y), (center_x, center_y - axis_length), 2)
            # Z axis (blue)
            pygame.draw.line(surface, (0, 0, 255), (center_x, center_y), (center_x - axis_length//2, center_y + axis_length//2), 2)
        
        # Draw a "focused" border if this viewport is active
        if self.is_focused:
            pygame.draw.rect(surface, (100, 180, 255), viewport_rect, 2)
