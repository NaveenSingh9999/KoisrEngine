import pygame
from gui_engine.core.gui_engine import GuiEngine

pygame.init()
screen = pygame.display.set_mode((1280, 800), pygame.DOUBLEBUF | pygame.OPENGL)
engine = GuiEngine(screen)
clock = pygame.time.Clock()
running = True
while running:
    dt = clock.tick(60) / 1000.0
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        engine.handle_event(event)
    engine.update(dt)
    screen.fill((30, 32, 36))
    engine.draw()
    pygame.display.flip()
pygame.quit()
