from engine.game_object import GameObject

class Scene:
    def __init__(self, name="Scene"):
        self.name = name
        self.game_objects = []
    def add_game_object(self, obj):
        self.game_objects.append(obj)
    def remove_game_object(self, obj):
        self.game_objects = [go for go in self.game_objects if go != obj]
    def find_by_name(self, name):
        for go in self.game_objects:
            if go.name == name:
                return go
        return None
    def update(self, dt):
        for go in self.game_objects:
            go.update(dt)
