import uuid
from engine.transform import Transform

class GameObject:
    def __init__(self, name="GameObject"):
        self.id = str(uuid.uuid4())
        self.name = name
        self.components = []
        self.transform = Transform(self)
        self.add_component(self.transform)
        self.mesh = None
        self.type = None
    def add_component(self, component):
        component.game_object = self
        self.components.append(component)
    def get_component(self, comp_type):
        for c in self.components:
            if isinstance(c, comp_type):
                return c
        return None
    def remove_component(self, comp_type):
        self.components = [c for c in self.components if not isinstance(c, comp_type)]
    def update(self, dt):
        for c in self.components:
            if c.enabled:
                c.update(dt)
    def set_mesh(self, mesh_type):
        self.mesh = mesh_type
        self.type = mesh_type
