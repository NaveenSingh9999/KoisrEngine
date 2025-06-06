# koisrgui/widgets/panel.py
import pygame
from koisrgui.core.widget import Widget

class Panel(Widget):
    def __init__(self, x, y, width, height, style=None):
        super().__init__(x, y, width, height)
        if style:
            self.set_style(style)

    def draw(self, surface):
        if not self.visible:
            return
        color = self.style.get('bg', (50, 50, 50))
        border_radius = self.style.get('border_radius', 4)
        pygame.draw.rect(surface, color, (self.x, self.y, self.width, self.height), border_radius=border_radius)
        for child in sorted(self.children, key=lambda w: w.z_index):
            child.draw(surface)
