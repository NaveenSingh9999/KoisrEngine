from koisrgui.widgets.panel import Panel
from gui_engine.state.global_state import GlobalState

class ScenePanel(Panel):
    def __init__(self, *args, **kwargs):
        super().__init__(title="Scene", *args, **kwargs)
        # Add tree widget for scene hierarchy here

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
