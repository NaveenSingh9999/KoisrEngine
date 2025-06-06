from koisrgui.widgets.panel import Panel
from koisrgui.widgets.button import Button
from koisrgui.widgets.label import Label
from gui_engine.state.global_state import GlobalState

class ScenePanel(Panel):
    def __init__(self, engine, *args, **kwargs):
        super().__init__(title="Scene", *args, **kwargs)
        self.engine = engine
        self.selected_id = None
        self._build_ui()
    def _build_ui(self):
        self.children.clear()
        y = self.y + 32
        for obj in self.engine.get_game_objects():
            btn = Button(self.x + 8, y, self.width - 16, 28, obj.name, on_click=lambda o=obj: self.select_object(o))
            if self.selected_id == obj.id:
                btn.set_style({'bg': (80, 120, 200)})
            self.add_child(btn)
            y += 36
    def select_object(self, obj):
        self.selected_id = obj.id
        self.engine.set_selected_object(obj)
        self._build_ui()
    def update(self, dt):
        # Rebuild UI if objects change
        self._build_ui()
        super().update(dt)

class InspectorPanel(Panel):
    def __init__(self, *args, **kwargs):
        super().__init__(title="Inspector", *args, **kwargs)
        # Add property widgets here

class AssetBrowserPanel(Panel):
    def __init__(self, *args, **kwargs):
        super().__init__(title="Assets", *args, **kwargs)
        # Add asset tree/list here

class ConsolePanel(Panel):
    def __init__(self, *args, **kwargs):
        super().__init__(title="Console", *args, **kwargs)
        # Add log output widget here

class GameViewportPanel(Panel):
    def __init__(self, *args, **kwargs):
        super().__init__(title="Game", *args, **kwargs)
        # Add OpenGL texture view here
