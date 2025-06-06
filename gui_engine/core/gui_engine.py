import json
from koisrgui.core.manager import GUIManager
from gui_engine.layout.layout_manager import LayoutManager
from gui_engine.state.global_state import GlobalState
from engine.engine import Engine

class GuiEngine:
    def __init__(self, screen, layout_config_path=None, engine=None):
        self.screen = screen
        self.engine = engine or Engine()
        self.gui = GUIManager(screen)
        self.state = GlobalState()
        self.layout_manager = LayoutManager(self.gui, self.state, self.engine)
        self.layout_manager.load_default_layout()

    def update(self, dt):
        self.engine.update(dt)
        self.layout_manager.update(dt)
        self.gui.update(dt)

    def draw(self):
        self.engine.render()
        self.layout_manager.draw(self.screen)
        self.gui.draw()

    def handle_event(self, event):
        self.layout_manager.handle_event(event)
        self.gui.handle_event(event)
