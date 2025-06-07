# gui_engine/layout/dock_manager.py
import pygame

class DockArea:
    def __init__(self, x, y, width, height, position):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.position = position  # 'left', 'right', 'top', 'bottom', 'center'
        self.panels = []
        self.active_panel_index = 0
        
    def add_panel(self, panel):
        if panel not in self.panels:
            self.panels.append(panel)
            self.active_panel_index = len(self.panels) - 1
            panel.dock_position = self.position
            panel.is_docked = True
            self._update_panel_positions()
            
    def remove_panel(self, panel):
        if panel in self.panels:
            index = self.panels.index(panel)
            self.panels.remove(panel)
            panel.is_docked = False
            panel.dock_position = None
            if self.panels and self.active_panel_index >= len(self.panels):
                self.active_panel_index = len(self.panels) - 1
            self._update_panel_positions()
            
    def _update_panel_positions(self):
        for panel in self.panels:
            panel.x = self.x
            panel.y = self.y
            panel.width = self.width
            panel.height = self.height
            
    def resize(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self._update_panel_positions()
        
    def draw(self, surface):
        print(f"[DEBUG] DockArea.draw() called for {self.position} with {len(self.panels)} panels")
        
        # Draw all panels in the dock area
        for i, panel in enumerate(self.panels):
            if i == self.active_panel_index:
                panel.visible = True
                print(f"[DEBUG] Drawing panel '{panel.title}' in position {self.position}")
            else:
                panel.visible = False
            
            if panel.visible:
                panel.draw(surface)
        
        # If there are multiple panels, draw tabs
        if len(self.panels) > 1:
            tab_width = min(100, self.width / len(self.panels))
            tab_height = 25
            
            for i, panel in enumerate(self.panels):
                tab_x = self.x + i * tab_width
                tab_y = self.y - tab_height
                
                # Draw tab background
                if i == self.active_panel_index:
                    pygame.draw.rect(surface, (60, 60, 60), (tab_x, tab_y, tab_width, tab_height))
                else:
                    pygame.draw.rect(surface, (40, 40, 40), (tab_x, tab_y, tab_width, tab_height))
                
                # Draw tab border
                pygame.draw.rect(surface, (70, 70, 70), (tab_x, tab_y, tab_width, tab_height), 1)
                
                # Draw tab title
                if panel.title:
                    font = pygame.font.SysFont(None, 18)
                    # Truncate title if too long
                    truncated_title = panel.title if len(panel.title) < 10 else panel.title[:8] + ".."
                    text_surf = font.render(truncated_title, True, (220, 220, 220))
                    surface.blit(text_surf, (tab_x + 5, tab_y + 5))
    
    def handle_event(self, event):
        # Check if any panel in this dock area was clicked
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_x, mouse_y = event.pos
            
            # Check if click is on tabs (if we have multiple panels)
            if len(self.panels) > 1:
                tab_width = min(100, self.width / len(self.panels))
                tab_height = 25
                
                for i, panel in enumerate(self.panels):
                    tab_x = self.x + i * tab_width
                    tab_y = self.y - tab_height
                    tab_rect = pygame.Rect(tab_x, tab_y, tab_width, tab_height)
                    
                    if tab_rect.collidepoint(mouse_x, mouse_y):
                        self.active_panel_index = i
                        return True
            
            # Pass event to active panel
            if self.panels and self.active_panel_index < len(self.panels):
                active_panel = self.panels[self.active_panel_index]
                if active_panel.handle_event(event):
                    return True
        
        # For other events, only pass to active panel
        elif self.panels and self.active_panel_index < len(self.panels):
            active_panel = self.panels[self.active_panel_index]
            if active_panel.handle_event(event):
                return True
        
        return False

class DockManager:
    def __init__(self, screen_width, screen_height, toolbar_height=40, status_bar_height=20):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.toolbar_height = toolbar_height
        self.status_bar_height = status_bar_height
        
        # Default dock area proportions
        self.left_width = int(screen_width * 0.2)
        self.right_width = int(screen_width * 0.25)
        self.bottom_height = int(screen_height * 0.25)
        
        # Initialize dock areas
        self._init_dock_areas()
        
        # Dragging state
        self.is_dragging_divider = False
        self.dragging_divider = None  # 'left', 'right', 'bottom'
        self.divider_drag_pos = 0
        
    def _init_dock_areas(self):
        # Create dock areas with initial positions and sizes
        main_y = self.toolbar_height
        main_height = self.screen_height - self.toolbar_height - self.bottom_height - self.status_bar_height
        
        self.dock_areas = {
            'left': DockArea(0, main_y, self.left_width, main_height, 'left'),
            'center': DockArea(self.left_width, main_y, 
                              self.screen_width - self.left_width - self.right_width, 
                              main_height, 'center'),
            'right': DockArea(self.screen_width - self.right_width, main_y, 
                             self.right_width, main_height, 'right'),
            'bottom': DockArea(0, main_y + main_height, 
                              self.screen_width, self.bottom_height, 'bottom'),
            'top': DockArea(0, 0, self.screen_width, self.toolbar_height, 'top')
        }
        
    def add_panel(self, panel, position):
        if position in self.dock_areas:
            # First remove from any current dock area
            self.undock_panel(panel)
            # Then add to the new dock area
            self.dock_areas[position].add_panel(panel)
            # Make sure panel has a reference to the dock manager
            panel.set_dock_manager(self)
            print(f"[DEBUG] Added panel '{panel.title}' to position '{position}'")
            
    def remove_panel(self, panel):
        for area in self.dock_areas.values():
            if panel in area.panels:
                area.remove_panel(panel)
                print(f"[DEBUG] Removed panel '{panel.title}' from dock area")
            
    def undock_panel(self, panel):
        for area in self.dock_areas.values():
            if panel in area.panels:
                area.remove_panel(panel)
                break
                
    def try_dock(self, panel):
        """Check if panel is near a dock area and dock it if appropriate"""
        panel_center_x = panel.x + panel.width // 2
        panel_center_y = panel.y + panel.height // 2
        
        # Check if panel is near left edge
        if panel_center_x < self.left_width + 50:
            self.add_panel(panel, 'left')
            return True
            
        # Check if panel is near right edge
        if panel_center_x > self.screen_width - self.right_width - 50:
            self.add_panel(panel, 'right')
            return True
            
        # Check if panel is near bottom
        bottom_y = self.screen_height - self.bottom_height - self.status_bar_height
        if panel_center_y > bottom_y - 50:
            self.add_panel(panel, 'bottom')
            return True
            
        # Check if panel is near top
        if panel_center_y < self.toolbar_height + 50:
            self.add_panel(panel, 'top')
            return True
            
        # Check if panel is in center area
        center_area = self.dock_areas['center']
        if (center_area.x < panel_center_x < center_area.x + center_area.width and
            center_area.y < panel_center_y < center_area.y + center_area.height):
            self.add_panel(panel, 'center')
            return True
            
        return False
        
    def handle_event(self, event):
        # Check for divider dragging
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_x, mouse_y = event.pos
            
            # Check if we're clicking on a divider
            divider_width = 5
            
            # Left divider
            left_divider_x = self.left_width
            left_divider_rect = pygame.Rect(left_divider_x - divider_width//2, 
                                          self.toolbar_height, 
                                          divider_width, 
                                          self.screen_height - self.toolbar_height - self.bottom_height - self.status_bar_height)
            
            # Right divider
            right_divider_x = self.screen_width - self.right_width
            right_divider_rect = pygame.Rect(right_divider_x - divider_width//2, 
                                           self.toolbar_height, 
                                           divider_width, 
                                           self.screen_height - self.toolbar_height - self.bottom_height - self.status_bar_height)
            
            # Bottom divider
            bottom_divider_y = self.screen_height - self.bottom_height - self.status_bar_height
            bottom_divider_rect = pygame.Rect(0, 
                                            bottom_divider_y - divider_width//2, 
                                            self.screen_width, 
                                            divider_width)
            
            if left_divider_rect.collidepoint(mouse_x, mouse_y):
                self.is_dragging_divider = True
                self.dragging_divider = 'left'
                self.divider_drag_pos = mouse_x
                return True
                
            elif right_divider_rect.collidepoint(mouse_x, mouse_y):
                self.is_dragging_divider = True
                self.dragging_divider = 'right'
                self.divider_drag_pos = mouse_x
                return True
                
            elif bottom_divider_rect.collidepoint(mouse_x, mouse_y):
                self.is_dragging_divider = True
                self.dragging_divider = 'bottom'
                self.divider_drag_pos = mouse_y
                return True
                
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            if self.is_dragging_divider:
                self.is_dragging_divider = False
                self.dragging_divider = None
                return True
                
        elif event.type == pygame.MOUSEMOTION:
            mouse_x, mouse_y = event.pos
            
            # Handle divider dragging
            if self.is_dragging_divider:
                if self.dragging_divider == 'left':
                    # Update left panel width (min 100px, max screen_width - right_width - 200px)
                    min_width = 100
                    max_width = self.screen_width - self.right_width - 200
                    self.left_width = max(min_width, min(max_width, mouse_x))
                    
                elif self.dragging_divider == 'right':
                    # Update right panel width
                    min_width = 100
                    max_width = self.screen_width - self.left_width - 200
                    self.right_width = max(min_width, min(max_width, self.screen_width - mouse_x))
                    
                elif self.dragging_divider == 'bottom':
                    # Update bottom panel height
                    min_height = 80
                    max_height = self.screen_height - self.toolbar_height - 200
                    self.bottom_height = max(min_height, min(max_height, self.screen_height - mouse_y - self.status_bar_height))
                
                # Recalculate dock areas
                self._update_dock_areas()
                return True
                
            # Update cursor when hovering over dividers
            divider_width = 5
            
            # Left divider
            left_divider_x = self.left_width
            left_divider_rect = pygame.Rect(left_divider_x - divider_width//2, 
                                          self.toolbar_height, 
                                          divider_width, 
                                          self.screen_height - self.toolbar_height - self.bottom_height - self.status_bar_height)
            
            # Right divider
            right_divider_x = self.screen_width - self.right_width
            right_divider_rect = pygame.Rect(right_divider_x - divider_width//2, 
                                           self.toolbar_height, 
                                           divider_width, 
                                           self.screen_height - self.toolbar_height - self.bottom_height - self.status_bar_height)
            
            # Bottom divider
            bottom_divider_y = self.screen_height - self.bottom_height - self.status_bar_height
            bottom_divider_rect = pygame.Rect(0, 
                                            bottom_divider_y - divider_width//2, 
                                            self.screen_width, 
                                            divider_width)
                                            
            if left_divider_rect.collidepoint(mouse_x, mouse_y) or right_divider_rect.collidepoint(mouse_x, mouse_y):
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_SIZEWE)
            elif bottom_divider_rect.collidepoint(mouse_x, mouse_y):
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_SIZENS)
            else:
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
        
        # Pass events to dock areas
        for area in self.dock_areas.values():
            if area.handle_event(event):
                return True
                
        return False
        
    def _update_dock_areas(self):
        # Recalculate and resize all dock areas based on current divider positions
        main_y = self.toolbar_height
        main_height = self.screen_height - self.toolbar_height - self.bottom_height - self.status_bar_height
        
        # Update all dock areas with new positions and sizes
        self.dock_areas['left'].resize(
            0, main_y, 
            self.left_width, main_height
        )
        
        self.dock_areas['center'].resize(
            self.left_width, main_y, 
            self.screen_width - self.left_width - self.right_width, 
            main_height
        )
        
        self.dock_areas['right'].resize(
            self.screen_width - self.right_width, main_y, 
            self.right_width, main_height
        )
        
        self.dock_areas['bottom'].resize(
            0, main_y + main_height, 
            self.screen_width, self.bottom_height
        )
        
        self.dock_areas['top'].resize(
            0, 0, 
            self.screen_width, self.toolbar_height
        )
        
        print(f"[DEBUG] Updated dock areas: left={self.left_width}, right={self.right_width}, bottom={self.bottom_height}")
        
    def draw(self, surface):
        print(f"[DEBUG] DockManager.draw() called with {len(self.dock_areas)} dock areas")
        
        # Draw all dock areas
        for position, area in self.dock_areas.items():
            print(f"[DEBUG] Drawing dock area '{position}' with {len(area.panels)} panels")
            area.draw(surface)
            
        # Draw dividers
        divider_width = 5
        divider_color = (80, 80, 90)
        
        # Left divider
        left_divider_rect = pygame.Rect(
            self.left_width - divider_width//2, 
            self.toolbar_height, 
            divider_width, 
            self.screen_height - self.toolbar_height - self.bottom_height - self.status_bar_height
        )
        pygame.draw.rect(surface, divider_color, left_divider_rect)
        
        # Right divider
        right_divider_rect = pygame.Rect(
            self.screen_width - self.right_width - divider_width//2, 
            self.toolbar_height, 
            divider_width, 
            self.screen_height - self.toolbar_height - self.bottom_height - self.status_bar_height
        )
        pygame.draw.rect(surface, divider_color, right_divider_rect)
        
        # Bottom divider
        bottom_divider_rect = pygame.Rect(
            0, 
            self.screen_height - self.bottom_height - self.status_bar_height - divider_width//2, 
            self.screen_width, 
            divider_width
        )
        pygame.draw.rect(surface, divider_color, bottom_divider_rect)
