# app/koisr_editor.py
import os
import sys
import json
import datetime
import pygame
import tkinter as tk
from tkinter import filedialog, simpledialog, messagebox
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

    engine_backend = None
    def enter_editor(project_path):
        nonlocal screen, gui_engine, home_screen, engine_backend
        global_state['project_path'] = project_path
        
        # Load project data
        try:
            with open(project_path, 'r') as f:
                project_data = json.load(f)
                
            # Use Pygame 2D surface for editor UI (no OPENGL flag)
            screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.DOUBLEBUF)
            pygame.font.quit()
            pygame.font.init()
            
            if engine_backend is None:
                from engine.engine import Engine
                engine_backend = Engine()
                # Set project name in engine for display in UI
                engine_backend.project_name = project_data.get("name", "Untitled")
                
                # Load any saved scene if available
                active_scene = project_data.get("active_scene")
                if active_scene and os.path.exists(active_scene):
                    print(f"Loading scene: {active_scene}")
                    # Here you would load the scene data
            
            # Initialize GUI with engine backend
            gui_engine = GuiEngine(screen, layout_config_path=None, engine=engine_backend)
            
            # Close home screen and switch to editor mode
            home_screen = None
            app_state['mode'] = 'editor'
            print(f"[INFO] Entered editor with project: {project_path}")
            
            # Update last_opened time
            project_data["last_opened"] = datetime.datetime.now().isoformat()
            with open(project_path, 'w') as f:
                json.dump(project_data, f, indent=4)
                
        except Exception as e:
            messagebox.showerror("Error", f"Failed to open project: {str(e)}")
            print(f"[ERROR] Failed to enter editor: {e}")
            app_state['mode'] = 'home'

    def on_create():
        # Open a file dialog to select a directory for the new project
        root = tk.Tk()
        root.withdraw()
        project_dir = filedialog.askdirectory(title="Select New Project Directory")
        if project_dir:
            project_name = simpledialog.askstring("Project Name", "Enter project name:")
            if project_name:
                # Create project structure
                project_folder = os.path.join(project_dir, project_name)
                os.makedirs(project_folder, exist_ok=True)
                
                # Create subdirectories
                os.makedirs(os.path.join(project_folder, "scenes"), exist_ok=True)
                os.makedirs(os.path.join(project_folder, "assets"), exist_ok=True)
                os.makedirs(os.path.join(project_folder, "scripts"), exist_ok=True)
                
                # Create project file
                project_path = os.path.join(project_dir, project_name + ".koisrproj")
                
                # Create project metadata
                project_data = {
                    "name": project_name,
                    "created": datetime.datetime.now().isoformat(),
                    "last_opened": datetime.datetime.now().isoformat(),
                    "version": "1.0.0",
                    "assets": [],
                    "active_scene": os.path.join(project_folder, "scenes", "main.scene"),
                    "description": "",
                    "author": ""
                }
                
                # Create empty main scene file
                with open(os.path.join(project_folder, "scenes", "main.scene"), 'w') as f:
                    json.dump({"name": "Main Scene", "objects": []}, f, indent=4)
                
                # Write project file
                with open(project_path, 'w') as f:
                    json.dump(project_data, f, indent=4)
                
                # Add to recent projects and set as last project
                project_manager.add_recent_project(project_path)
                project_manager.set_last_project(project_path)
                print(f"Created new project at {project_path}")
                
                # Enter editor with new project
                enter_editor(project_path)
            else:
                print("Project creation cancelled (no name)")
        else:
            print("Project creation cancelled (no directory)")

    def on_open():
        # Open a file dialog to select an existing .koisrproj file
        import tkinter as tk
        from tkinter import filedialog, messagebox
        root = tk.Tk()
        root.withdraw()
        file_path = filedialog.askopenfilename(title="Open Koisr Project", filetypes=[("Koisr Project", "*.koisrproj")])
        if file_path:
            # Validate project file
            try:
                with open(file_path, 'r') as f:
                    project_data = json.load(f)
                # Check required fields
                required_fields = ["name", "created", "version"]
                if not all(field in project_data for field in required_fields):
                    raise ValueError("Missing required fields in project file")
                    
                # Update last_opened time
                project_data["last_opened"] = datetime.datetime.now().isoformat()
                with open(file_path, 'w') as f:
                    json.dump(project_data, f, indent=4)
                    
                project_manager.add_recent_project(file_path)
                project_manager.set_last_project(file_path)
                print(f"Opened project: {file_path}")
                enter_editor(file_path)
            except (json.JSONDecodeError, ValueError) as e:
                messagebox.showerror("Invalid Project File", 
                                     f"Could not open project file: {str(e)}\n\nThe file might be corrupted or in an invalid format.")
                print(f"Failed to open project: {e}")
        else:
            print("Open project cancelled")

    def on_resume():
        last = project_manager.get_last_project()
        if last and os.path.exists(last):
            print(f"Resuming last project: {last}")
            try:
                with open(last, 'r') as f:
                    project_data = json.load(f)
                
                # Update last_opened time
                project_data["last_opened"] = datetime.datetime.now().isoformat()
                with open(last, 'w') as f:
                    json.dump(project_data, f, indent=4)
                    
                project_manager.set_last_project(last)
                enter_editor(last)
            except (json.JSONDecodeError, ValueError) as e:
                import tkinter as tk
                from tkinter import messagebox
                root = tk.Tk()
                root.withdraw()
                messagebox.showerror("Invalid Project File", 
                                     f"Could not open last project: {str(e)}\n\nThe file might be corrupted or in an invalid format.")
                print(f"Failed to resume project: {e}")
                app_state['mode'] = 'home'
                app_state['project_path'] = None
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
            print('[DEBUG] Calling gui_engine.update(dt)')
            gui_engine.update(dt)
            print('[DEBUG] Calling gui_engine.draw()')
            gui_engine.draw()
            try:
                import OpenGL.GL as gl
                err = gl.glGetError()
                if err != 0:
                    print(f'[OpenGL ERROR] glGetError() returned: {err}')
            except Exception as e:
                print(f'[OpenGL DEBUG] Exception during glGetError: {e}')
        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()
