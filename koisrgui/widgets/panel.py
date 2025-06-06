# koisrgui/widgets/panel.py
import pygame
from koisrgui.core.widget import Widget
# gre
class Panel(Widget):
    def __init__(self, x, y, width, height, title=None, style=None):
        super().__init__(x, y, width, height)
        self.title = title
        if style:
            self.set_style(style)

    def draw(self, surface):
        if not self.visible:
            return
        print(f'[DEBUG] Panel.draw: {self.title} at ({self.x},{self.y},{self.width},{self.height})')
        color = self.style.get('bg', (50, 50, 50))
        border_radius = self.style.get('border_radius', 4)
        pygame.draw.rect(surface, color, (self.x, self.y, self.width, self.height), border_radius=border_radius)
        # Draw title if present
        if self.title:
            font = pygame.font.SysFont(None, 20)
            text_surf = font.render(self.title, True, self.style.get('fg', (220, 220, 220)))
            surface.blit(text_surf, (self.x + 8, self.y + 6))
        for child in sorted(self.children, key=lambda w: w.z_index):
            child.draw(surface)
