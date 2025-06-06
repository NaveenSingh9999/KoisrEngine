# app/koisr_editor.py
import os
import sys
import pygame
from gui_engine.core.gui_engine import GuiEngine
from gui_engine.screens.home_screen import HomeScreen
from gui_engine.state.project_manager import ProjectManager

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

    # Splash/loading screen
    from app.startup.loader import show_splash
    show_splash(screen)

    project_manager = ProjectManager()
    app_state = {'mode': 'home', 'project_path': None}
    gui_engine = None
    home_screen = None

    def on_create():
        # TODO: Show project creation dialog
        print("Create New Project clicked")
        # For now, just switch to editor
        app_state['mode'] = 'editor'
        app_state['project_path'] = None

    def on_open():
        # TODO: Show file dialog to select .koisrproj
        print("Open Existing Project clicked")
        # For now, just switch to editor
        app_state['mode'] = 'editor'
        app_state['project_path'] = None

    def on_resume():
        last = project_manager.get_last_project()
        print(f"Resume Last Project: {last}")
        app_state['mode'] = 'editor'
        app_state['project_path'] = last

    # Show HomeScreen first
    home_screen = HomeScreen(
        SCREEN_WIDTH, SCREEN_HEIGHT, project_manager,
        on_create=on_create, on_open=on_open, on_resume=on_resume
    )

    clock = pygame.time.Clock()
    running = True
    while running:
        dt = clock.tick(FPS) / 1000.0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if app_state['mode'] == 'home':
                home_screen.handle_event(event)
            elif app_state['mode'] == 'editor' and gui_engine:
                gui_engine.handle_event(event)
        # TODO: Game engine update (if running game in editor)
        screen.fill((30, 32, 36))
        if app_state['mode'] == 'home':
            home_screen.update(dt)
            home_screen.draw(screen)
            # If mode switched, initialize editor
            if app_state['mode'] == 'editor' and gui_engine is None:
                gui_engine = GuiEngine(screen)
        elif app_state['mode'] == 'editor' and gui_engine:
            gui_engine.update(dt)
            gui_engine.draw()
        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()
