import json
from koisrgui.core.manager import GUIManager
from gui_engine.layout.layout_manager import LayoutManager
from gui_engine.state.global_state import GlobalState

class GuiEngine:
    def __init__(self, screen, layout_config_path=None):
        self.screen = screen
        self.gui = GUIManager(screen)
        self.state = GlobalState()
        self.layout_manager = LayoutManager(self.gui, self.state)
        if layout_config_path:
            self.layout_manager.load_layout(layout_config_path)
        else:
            self.layout_manager.load_default_layout()

    def update(self, dt):
        self.layout_manager.update(dt)
        self.gui.update(dt)

    def draw(self):
        self.layout_manager.draw()
        self.gui.draw()

    def handle_event(self, event):
        self.layout_manager.handle_event(event)
        self.gui.handle_event(event)
