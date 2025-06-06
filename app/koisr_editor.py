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
    # Use SW surface for HomeScreen (no OPENGL flag)
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.DOUBLEBUF)
    # Splash/loading screen
    from app.startup.loader import show_splash
    show_splash(screen)

    project_manager = ProjectManager()
    app_state = {'mode': 'home', 'project_path': None}
    gui_engine = None
    home_screen = None

    # Store project path in a global state
    global_state = {'project_path': None}

    def enter_editor(project_path):
        global_state['project_path'] = project_path
        # Switch to OpenGL surface for editor
        nonlocal screen, gui_engine, home_screen
        screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.DOUBLEBUF | pygame.OPENGL)
        gui_engine = GuiEngine(screen, layout_config_path=None)  # Can load from config/layout.json if needed
        home_screen = None
        app_state['mode'] = 'editor'
        print(f"[INFO] Entered editor with project: {project_path}")

    def on_create():
        # Open a file dialog to select a directory for the new project
        import tkinter as tk
        from tkinter import filedialog, simpledialog
        root = tk.Tk()
        root.withdraw()
        project_dir = filedialog.askdirectory(title="Select New Project Directory")
        if project_dir:
            project_name = simpledialog.askstring("Project Name", "Enter project name:")
            if project_name:
                project_path = os.path.join(project_dir, project_name + ".koisrproj")
                with open(project_path, 'w') as f:
                    f.write('{"name": "%s", "created": "%s"}' % (project_name, pygame.time.get_ticks()))
                project_manager.add_recent_project(project_path)
                project_manager.set_last_project(project_path)
                print(f"Created new project at {project_path}")
                enter_editor(project_path)
            else:
                print("Project creation cancelled (no name)")
        else:
            print("Project creation cancelled (no directory)")

    def on_open():
        # Open a file dialog to select an existing .koisrproj file
        import tkinter as tk
        from tkinter import filedialog
        root = tk.Tk()
        root.withdraw()
        file_path = filedialog.askopenfilename(title="Open Koisr Project", filetypes=[("Koisr Project", "*.koisrproj")])
        if file_path:
            project_manager.add_recent_project(file_path)
            project_manager.set_last_project(file_path)
            print(f"Opened project: {file_path}")
            enter_editor(file_path)
        else:
            print("Open project cancelled")

    def on_resume():
        last = project_manager.get_last_project()
        if last and os.path.exists(last):
            print(f"Resuming last project: {last}")
            project_manager.set_last_project(last)
            enter_editor(last)
        else:
            print("No last project to resume or file missing.")
            app_state['mode'] = 'home'
            app_state['project_path'] = None

    # Show HomeScreen first
    home_screen = HomeScreen(
        SCREEN_WIDTH, SCREEN_HEIGHT, project_manager,
        on_create=on_create, on_open=on_open, on_resume=on_resume
    )

    clock = pygame.time.Clock()
    running = True
    while running:
        dt = clock.tick(FPS) / 1000.0
        pygame.display.set_caption(f"KoisrEditor - FPS: {int(clock.get_fps())}")
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if app_state['mode'] == 'home' and home_screen:
                home_screen.handle_event(event)
            elif app_state['mode'] == 'editor' and gui_engine:
                gui_engine.handle_event(event)
        screen.fill((30, 32, 36))
        if app_state['mode'] == 'home' and home_screen:
            home_screen.update(dt)
            home_screen.draw(screen)
        elif app_state['mode'] == 'editor' and gui_engine:
            gui_engine.update(dt)
            gui_engine.draw()
        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()
