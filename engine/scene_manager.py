from engine.scene import Scene

# Scene manager placeholder

class SceneManager:
    def __init__(self):
        self.active_scene = Scene("MainScene")
    def add_game_object(self, obj):
        self.active_scene.add_game_object(obj)
    def remove_game_object(self, obj):
        self.active_scene.remove_game_object(obj)
    def update(self, dt):
        self.active_scene.update(dt)
    def get_game_objects(self):
        return self.active_scene.game_objects
