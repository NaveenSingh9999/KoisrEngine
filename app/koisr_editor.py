# app/koisr_editor.py
import os
import sys
import pygame
from gui_engine.core.gui_engine import GuiEngine

# Ensure project root is in sys.path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# App settings
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 800
FPS = 60


def main():
    pygame.init()
    pygame.display.set_caption("KoisrEditor")
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.DOUBLEBUF | pygame.OPENGL)

    # Splash/loading screen (optional, can be expanded in startup/loader.py)
    screen.fill((30, 32, 36))
    font = pygame.font.SysFont("Arial", 32)
    text = font.render("Loading KoisrEditor...", True, (220, 220, 220))
    screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, SCREEN_HEIGHT // 2 - text.get_height() // 2))
    pygame.display.flip()

    # Load config/settings (theme, layout, last project, etc.)
    # For now, use defaults. Later: load from app/config/settings.json
    # config = ...

    # Initialize GUI engine
    gui_engine = GuiEngine(screen)

    # TODO: Project manager integration (open/create project)
    # TODO: Load previous project or show project selection dialog

    clock = pygame.time.Clock()
    running = True
    while running:
        dt = clock.tick(FPS) / 1000.0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            gui_engine.handle_event(event)
        # TODO: Game engine update (if running game in editor)
        gui_engine.update(dt)
        screen.fill((30, 32, 36))  # Editor background
        gui_engine.draw()
        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()
