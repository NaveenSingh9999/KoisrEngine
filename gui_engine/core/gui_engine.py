import json
from koisrgui.core.manager import GUIManager
from gui_engine.layout.layout_manager import LayoutManager
from gui_engine.state.global_state import GlobalState

class GuiEngine:
    def __init__(self, screen, layout_config_path=None, engine=None):
        print('[DEBUG] GuiEngine.__init__ called')
        self.screen = screen
        self.engine = engine
        self.gui = GUIManager(screen)
        self.state = GlobalState()
        self.layout_manager = LayoutManager(self.gui, self.state, engine=self.engine)
        if layout_config_path:
            self.layout_manager.load_layout(layout_config_path)
        else:
            self.layout_manager.load_default_layout()
        print('[DEBUG] GuiEngine.__init__ finished')

    def update(self, dt):
        if self.engine:
            self.engine.update(dt)
        self.layout_manager.update(dt)
        self.gui.update(dt)

    def draw(self):
        self.layout_manager.draw(self.screen)
        self.gui.draw()
        if self.engine:
            self.engine.render()

    def handle_event(self, event):
        self.layout_manager.handle_event(event)
        self.gui.handle_event(event)
