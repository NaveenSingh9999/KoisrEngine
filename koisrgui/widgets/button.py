# koisrgui/widgets/button.py
import pygame
from koisrgui.core.widget import Widget

class Button(Widget):
    def __init__(self, x, y, width, height, text, on_click=None, style=None):
        super().__init__(x, y, width, height)
        self.text = text
        self.on_click = on_click
        self.hovered = False
        self.pressed = False
        if style:
            self.set_style(style)

    def draw(self, surface):
        color = self.style.get('bg', (60, 60, 60))
        if self.hovered:
            color = self.style.get('bg_hover', (80, 80, 80))
        pygame.draw.rect(surface, color, (self.x, self.y, self.width, self.height), border_radius=self.style.get('border_radius', 4))
        # Draw text (simple, using pygame font)
        font = pygame.font.SysFont(self.style.get('font', 'Arial'), self.style.get('font_size', 18))
        text_surf = font.render(self.text, True, self.style.get('fg', (220, 220, 220)))
        text_rect = text_surf.get_rect(center=(self.x + self.width//2, self.y + self.height//2))
        surface.blit(text_surf, text_rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            self.hovered = self.x <= event.pos[0] <= self.x + self.width and self.y <= event.pos[1] <= self.y + self.height
        elif event.type == pygame.MOUSEBUTTONDOWN and self.hovered:
            self.pressed = True
        elif event.type == pygame.MOUSEBUTTONUP:
            if self.pressed and self.hovered and self.on_click:
                self.on_click()
            self.pressed = False
