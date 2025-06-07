import os
import webbrowser
import pygame
from koisrgui.widgets.button import Button
from koisrgui.widgets.label import Label
from koisrgui.widgets.panel import Panel
from koisrgui.themes.dark import DARK_THEME

class HomeScreen(Panel):
    def __init__(self, width, height, project_manager, on_create, on_open, on_resume, style=None):
        super().__init__(
            x=0, y=0, width=width, height=height, title=None, style=style or DARK_THEME
        )
        self.width = width
        self.height = height
        self.project_manager = project_manager
        self.on_create = on_create
        self.on_open = on_open
        self.on_resume = on_resume
        self.recent_projects = self.project_manager.get_recent_projects()
        self._build_ui()

    def _build_ui(self):
        self.children.clear()
        
        # Background gradient
        # Will be drawn in the draw method
        
        # Center panel for main content
        center_panel_width = 500
        center_panel_height = 450
        center_panel_x = (self.width - center_panel_width) // 2
        center_panel_y = (self.height - center_panel_height) // 2
        
        # Create center panel
        center_panel = Panel(
            center_panel_x, center_panel_y, 
            center_panel_width, center_panel_height, 
            title=None, 
            style={**DARK_THEME, 'bg': (35, 35, 40), 'border_radius': 16}
        )
        
        # Logo/Title
        center_panel.add_child(Label(
            center_panel_width // 2 - 120, 30, 
            240, 50, 
            "KoisrEngine", 
            style={**DARK_THEME, 'font_size': 36, 'fg': (220, 220, 240)}
        ))
        
        # Version label
        center_panel.add_child(Label(
            center_panel_width // 2 - 40, 80, 
            80, 20, 
            "v0.1.0", 
            style={**DARK_THEME, 'font_size': 16, 'fg': (150, 150, 170)}
        ))
        
        # Main buttons
        btn_y = 120
        btn_w, btn_h = 240, 48
        btn_x = (center_panel_width - btn_w) // 2
        
        # Create New Project
        create_btn = Button(
            btn_x, btn_y, 
            btn_w, btn_h, 
            "Create New Project", 
            on_click=self.on_create, 
            style={
                **DARK_THEME, 
                'border_radius': 8, 
                'bg': (60, 100, 180), 
                'hover_bg': (80, 120, 200),
                'font_size': 18
            }
        )
        center_panel.add_child(create_btn)
        
        # Open Existing Project
        open_btn = Button(
            btn_x, btn_y + 60, 
            btn_w, btn_h, 
            "Open Existing Project", 
            on_click=self.on_open, 
            style={
                **DARK_THEME, 
                'border_radius': 8, 
                'bg': (60, 100, 150), 
                'hover_bg': (80, 120, 170),
                'font_size': 18
            }
        )
        center_panel.add_child(open_btn)
        
        # Resume Last Project
        resume_enabled = bool(self.project_manager.get_last_project())
        resume_btn = Button(
            btn_x, btn_y + 120, 
            btn_w, btn_h, 
            "Resume Last Project", 
            on_click=self.on_resume if resume_enabled else None, 
            style={
                **DARK_THEME, 
                'border_radius': 8, 
                'bg': (60, 100, 120) if resume_enabled else (40, 50, 60),
                'hover_bg': (80, 120, 140) if resume_enabled else (40, 50, 60),
                'font_size': 18
            }
        )
        center_panel.add_child(resume_btn)
        
        # Recent projects section
        recent_y = btn_y + 180
        center_panel.add_child(Label(
            30, recent_y, 
            200, 24, 
            "Recent Projects:", 
            style={**DARK_THEME, 'font_size': 20, 'fg': (200, 200, 220)}
        ))
        
        # List of recent projects
        for i, proj in enumerate(self.recent_projects[:5]):
            project_name = os.path.basename(proj['path']).replace('.koisrproj', '')
            project_dir = os.path.dirname(proj['path'])
            
            # Project name
            center_panel.add_child(Label(
                50, recent_y + 34 + i*30, 
                300, 20, 
                project_name, 
                style={**DARK_THEME, 'font_size': 16, 'fg': (200, 200, 220)}
            ))
            
            # Project path
            center_panel.add_child(Label(
                50, recent_y + 34 + i*30 + 20, 
                400, 16, 
                f"Path: {project_dir}", 
                style={**DARK_THEME, 'font_size': 12, 'fg': (150, 150, 170)}
            ))
            
            # Open button for this project
            open_this_btn = Button(
                center_panel_width - 100, recent_y + 34 + i*30 + 5, 
                80, 26, 
                "Open", 
                on_click=lambda p=proj['path']: self.on_open(p), 
                style={**DARK_THEME, 'border_radius': 4, 'bg': (50, 80, 120)}
            )
            center_panel.add_child(open_this_btn)
        
        if self.recent_projects:
            clear_btn = Button(
                center_panel_width - 160, recent_y, 
                140, 28, 
                "Clear Recent Projects", 
                on_click=self._clear_recent, 
                style={**DARK_THEME, 'font_size': 14, 'border_radius': 4, 'bg': (60, 40, 40)}
            )
            center_panel.add_child(clear_btn)
        
        # GitHub button at bottom
        github_btn = Button(
            center_panel_width//2 - 60, center_panel_height - 48, 
            120, 36, 
            "GitHub", 
            on_click=self._open_github, 
            style={
                **DARK_THEME, 
                'border_radius': 16, 
                'font_size': 16, 
                'bg': (40, 40, 45),
                'hover_bg': (50, 50, 55)
            }
        )
        center_panel.add_child(github_btn)
        
        # Add center panel to the main screen
        self.add_child(center_panel)
        
        # "Opensource" button at top-right (outside the center panel)
        self.btn_opensource = Button(
            self.width - 140, 20, 
            120, 36, 
            "Opensource", 
            on_click=self._open_github, 
            style={
                **DARK_THEME, 
                'border_radius': 8, 
                'bg': (60, 100, 160), 
                'hover_bg': (80, 120, 180),
                'font_size': 16
            }
        )
        self.add_child(self.btn_opensource)

    def _open_github(self):
        webbrowser.open_new_tab("https://github.com/NaveenSingh9999/KoisrEngine")

    def _clear_recent(self):
        self.project_manager.clear_recent_projects()
        self.recent_projects = []
        self._build_ui()

    def handle_event(self, event):
        for child in self.children:
            child.handle_event(event)

    def update(self, dt):
        for child in self.children:
            child.update(dt)

    def draw(self, surface):
        # Draw background gradient
        rect = pygame.Rect(0, 0, self.width, self.height)
        
        # Create gradient from top to bottom
        for y in range(0, self.height, 2):
            progress = y / self.height
            color = (
                int(30 + progress * 10),  # R
                int(30 + progress * 5),   # G
                int(40 + progress * 10)   # B
            )
            pygame.draw.rect(surface, color, (0, y, self.width, 2))
        
        # Draw all children
        for child in self.children:
            child.draw(surface)
