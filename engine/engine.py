from engine.scene_manager import SceneManager
from engine.renderer import Renderer

# Core engine logic placeholder

class Engine:
    def __init__(self):
        self.scene_manager = SceneManager()
        self.renderer = Renderer(self.scene_manager)
        self.running = False

    def start(self):
        self.running = True

    def stop(self):
        self.running = False

    def run(self):
        print("Engine running...")
        while self.running:
            dt = self.get_delta_time()
            self.update(dt)
            self.render()

    def update(self, dt):
        if self.running:
            self.scene_manager.update(dt)

    def render(self):
        self.renderer.render()

    def add_game_object(self, obj):
        self.scene_manager.add_game_object(obj)

    def get_game_objects(self):
        return self.scene_manager.get_game_objects()

    def get_delta_time(self):
        # Placeholder for delta time calculation
        return 1/60

    def set_selected_object(self, obj):
        self.selected_object = obj

    def get_selected_object(self):
        return getattr(self, 'selected_object', None)

    def play(self):
        self.start()

    def stop_runtime(self):
        self.stop()
