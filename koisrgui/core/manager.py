# koisrgui/core/manager.py
import pygame
from .widget import Widget

class GUIManager:
    def __init__(self, surface):
        self.surface = surface
        self.widgets = []
        self.focused_widget = None
        self.mouse_pos = (0, 0)

    def add_widget(self, widget):
        self.widgets.append(widget)

    def draw(self):
        for widget in sorted(self.widgets, key=lambda w: w.z_index):
            widget.draw(self.surface)

    def update(self, dt=0):
        for widget in self.widgets:
            widget.update(dt)

    def handle_event(self, event):
        if event.type in (pygame.MOUSEBUTTONDOWN, pygame.MOUSEMOTION):
            self.mouse_pos = event.pos
        for widget in reversed(sorted(self.widgets, key=lambda w: w.z_index)):
            widget.handle_event(event)
            # Focus logic can be added here

    def set_focus(self, widget):
        if self.focused_widget:
            self.focused_widget.set_focus(False)
        self.focused_widget = widget
        widget.set_focus(True)
