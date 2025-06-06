# app/startup/loader.py
import pygame

def show_splash(screen):
    screen.fill((30, 32, 36))
    font = pygame.font.SysFont("Arial", 32)
    text = font.render("Loading KoisrEditor...", True, (220, 220, 220))
    screen.blit(text, (screen.get_width() // 2 - text.get_width() // 2, screen.get_height() // 2 - text.get_height() // 2))
    pygame.display.flip()
