# gui_engine/screens/home_screen.py
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
            x=(width-480)//2, y=(height-420)//2, width=480, height=420, title=None, style=style or DARK_THEME
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
        # Logo/Title
        self.add_child(Label(self.x + 140, self.y + 30, 200, 40, "KoisrEngine", style={**DARK_THEME, 'font_size': 32}))
        # Main buttons
        btn_y = self.y + 100
        btn_w, btn_h = 200, 44
        btn_x = self.x + (self.width - btn_w) // 2
        self.btn_create = Button(btn_x, btn_y, btn_w, btn_h, "Create New Project", on_click=self.on_create, style={**DARK_THEME, 'border_radius': 8})
        self.btn_open = Button(btn_x, btn_y + 60, btn_w, btn_h, "Open Existing Project", on_click=self.on_open, style={**DARK_THEME, 'border_radius': 8})
        resume_enabled = bool(self.project_manager.get_last_project())
        self.btn_resume = Button(btn_x, btn_y + 120, btn_w, btn_h, "Resume Last Project", on_click=self.on_resume if resume_enabled else None, style={**DARK_THEME, 'border_radius': 8, 'bg': (60, 60, 60) if resume_enabled else (40, 40, 40)})
        self.add_child(self.btn_create)
        self.add_child(self.btn_open)
        self.add_child(self.btn_resume)
        # Recent projects list
        recent_y = btn_y + 180
        self.add_child(Label(self.x + 32, recent_y, 200, 24, "Recent Projects:", style={**DARK_THEME, 'font_size': 18}))
        for i, proj in enumerate(self.recent_projects[:5]):
            proj_str = f"{os.path.basename(proj['path'])}  —  {proj['path']}  ({proj['timestamp']})"
            self.add_child(Label(self.x + 48, recent_y + 32 + i*28, 380, 24, proj_str, style={**DARK_THEME, 'font_size': 14}))
        if self.recent_projects:
            self.btn_clear = Button(self.x + 320, recent_y, 120, 28, "Clear Recent Projects", on_click=self._clear_recent, style={**DARK_THEME, 'font_size': 14, 'border_radius': 6})
            self.add_child(self.btn_clear)
        # GitHub button at bottom
        self.btn_github = Button(self.x + self.width//2 - 60, self.y + self.height - 48, 120, 32, "GitHub", on_click=self._open_github, style={**DARK_THEME, 'border_radius': 16, 'font_size': 16, 'bg': (24, 24, 24)})
        self.add_child(self.btn_github)

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
        # Draw background panel with rounded corners
        pygame.draw.rect(surface, self.style.get('bg', (40, 40, 40)), (self.x, self.y, self.width, self.height), border_radius=16)
        # Draw all children
        for child in self.children:
            child.draw(surface)
