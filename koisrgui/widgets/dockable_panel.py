# koisrgui/widgets/dockable_panel.py
import pygame
from koisrgui.widgets.panel import Panel
from koisrgui.themes.dark import DARK_THEME

class DockablePanel(Panel):
    RESIZE_BORDER_SIZE = 5
    
    def __init__(self, x, y, width, height, title=None, style=None, min_width=100, min_height=100):
        super().__init__(x, y, width, height, title, style or DARK_THEME)
        self.min_width = min_width
        self.min_height = min_height
        self.is_dragging = False
        self.is_resizing = False
        self.resize_edge = None  # can be 'right', 'bottom', 'corner'
        self.drag_offset_x = 0
        self.drag_offset_y = 0
        self.dock_position = None  # can be 'left', 'right', 'top', 'bottom', 'center'
        self.dock_manager = None
        self.is_docked = False
        self.collapsed = False
        self.previous_size = (width, height)
        
        # Header area for dragging
        self.header_height = 30
        
        # Add a collapse button
        self.collapse_btn_rect = pygame.Rect(self.x + self.width - 30, self.y + 5, 20, 20)
        
    def set_dock_manager(self, dock_manager):
        self.dock_manager = dock_manager
        
    def handle_event(self, event):
        if not self.visible:
            return
        
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_x, mouse_y = event.pos
            
            # Check if collapse button was clicked
            if self.collapse_btn_rect.collidepoint(mouse_x, mouse_y):
                self.toggle_collapse()
                return True
                
            # Check if mouse is in the header area (for dragging)
            if (self.x <= mouse_x <= self.x + self.width and 
                self.y <= mouse_y <= self.y + self.header_height):
                self.is_dragging = True
                self.drag_offset_x = self.x - mouse_x
                self.drag_offset_y = self.y - mouse_y
                return True
                
            # Check if mouse is on resize edges
            is_on_right = (self.x + self.width - self.RESIZE_BORDER_SIZE <= mouse_x <= self.x + self.width)
            is_on_bottom = (self.y + self.height - self.RESIZE_BORDER_SIZE <= mouse_y <= self.y + self.height)
            
            if is_on_right and is_on_bottom:
                self.is_resizing = True
                self.resize_edge = 'corner'
                return True
            elif is_on_right:
                self.is_resizing = True
                self.resize_edge = 'right'
                return True
            elif is_on_bottom:
                self.is_resizing = True
                self.resize_edge = 'bottom'
                return True
                
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            if self.is_dragging or self.is_resizing:
                self.is_dragging = False
                self.is_resizing = False
                
                # Check for docking opportunity if we have a dock manager
                if self.dock_manager and self.is_dragging:
                    self.dock_manager.try_dock(self)
                    
                return True
                
        elif event.type == pygame.MOUSEMOTION:
            mouse_x, mouse_y = event.pos
            
            # Handle dragging
            if self.is_dragging:
                new_x = mouse_x + self.drag_offset_x
                new_y = mouse_y + self.drag_offset_y
                self.set_position(new_x, new_y)
                return True
                
            # Handle resizing
            if self.is_resizing:
                if self.resize_edge in ('right', 'corner'):
                    new_width = max(self.min_width, mouse_x - self.x)
                    self.width = new_width
                    
                if self.resize_edge in ('bottom', 'corner'):
                    new_height = max(self.min_height, mouse_y - self.y)
                    self.height = new_height
                
                # Update collapse button position
                self.collapse_btn_rect.x = self.x + self.width - 30
                return True
                
            # Update cursor based on mouse position
            is_on_right = (self.x + self.width - self.RESIZE_BORDER_SIZE <= mouse_x <= self.x + self.width)
            is_on_bottom = (self.y + self.height - self.RESIZE_BORDER_SIZE <= mouse_y <= self.y + self.height)
            
            if is_on_right and is_on_bottom:
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_SIZENWSE)
            elif is_on_right:
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_SIZEWE)
            elif is_on_bottom:
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_SIZENS)
            else:
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
        
        # Pass the event to children
        super().handle_event(event)
        return False
        
    def set_position(self, x, y):
        self.x = x
        self.y = y
        # Update collapse button position
        self.collapse_btn_rect.x = self.x + self.width - 30
        self.collapse_btn_rect.y = self.y + 5
        
    def toggle_collapse(self):
        if not self.collapsed:
            self.previous_size = (self.width, self.height)
            self.height = self.header_height
            self.collapsed = True
        else:
            self.width, self.height = self.previous_size
            self.collapsed = False
            
    def draw(self, surface):
        if not self.visible:
            return
            
        # Draw panel background
        bg_color = self.style.get('bg', (50, 50, 50))
        header_color = (bg_color[0] + 10, bg_color[1] + 10, bg_color[2] + 10)
        border_radius = self.style.get('border_radius', 4)
        border_color = self.style.get('border', (70, 70, 70))
        
        # Draw main panel rectangle
        pygame.draw.rect(surface, bg_color, (self.x, self.y, self.width, self.height), border_radius=border_radius)
        
        # Draw header bar
        pygame.draw.rect(surface, header_color, (self.x, self.y, self.width, self.header_height), 
                       border_top_left_radius=border_radius, border_top_right_radius=border_radius)
        
        # Draw panel border
        pygame.draw.rect(surface, border_color, (self.x, self.y, self.width, self.height), 
                       width=1, border_radius=border_radius)
        
        # Draw title if present
        if self.title:
            font = pygame.font.SysFont(None, 20)
            text_surf = font.render(self.title, True, self.style.get('fg', (220, 220, 220)))
            surface.blit(text_surf, (self.x + 8, self.y + 8))
        
        # Draw collapse button
        collapse_color = (180, 180, 180)
        pygame.draw.rect(surface, collapse_color, self.collapse_btn_rect, width=1, border_radius=2)
        
        # Draw the collapse/expand icon
        if self.collapsed:
            # Draw plus icon
            pygame.draw.line(surface, collapse_color, 
                          (self.collapse_btn_rect.x + 5, self.collapse_btn_rect.y + 10),
                          (self.collapse_btn_rect.x + 15, self.collapse_btn_rect.y + 10), 2)
            pygame.draw.line(surface, collapse_color, 
                          (self.collapse_btn_rect.x + 10, self.collapse_btn_rect.y + 5),
                          (self.collapse_btn_rect.x + 10, self.collapse_btn_rect.y + 15), 2)
        else:
            # Draw minus icon
            pygame.draw.line(surface, collapse_color, 
                          (self.collapse_btn_rect.x + 5, self.collapse_btn_rect.y + 10),
                          (self.collapse_btn_rect.x + 15, self.collapse_btn_rect.y + 10), 2)
        
        # Don't draw children if collapsed
        if not self.collapsed:
            for child in sorted(self.children, key=lambda w: w.z_index):
                child.draw(surface)
                
        # Draw resize handles if not collapsed
        if not self.collapsed:
            # Draw bottom-right corner resize handle
            pygame.draw.line(surface, border_color, 
                          (self.x + self.width - 10, self.y + self.height),
                          (self.x + self.width, self.y + self.height - 10), 2)
