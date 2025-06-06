# koisrgui/widgets/label.py
import pygame
from koisrgui.core.widget import Widget

class Label(Widget):
    def __init__(self, x, y, width, height, text, style=None):
        super().__init__(x, y, width, height)
        self.text = text
        if style:
            self.set_style(style)

    def draw(self, surface):
        font = pygame.font.SysFont(self.style.get('font', 'Arial'), self.style.get('font_size', 16))
        text_surf = font.render(self.text, True, self.style.get('fg', (220, 220, 220)))
        surface.blit(text_surf, (self.x, self.y))
