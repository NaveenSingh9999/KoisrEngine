# koisrgui/layouts/horizontal.py
from koisrgui.core.widget import Widget

class HorizontalLayout(Widget):
    def __init__(self, x, y, spacing=8):
        super().__init__(x, y, 0, 0)
        self.spacing = spacing

    def add_child(self, widget):
        widget.parent = self
        widget.x = self.x + sum(child.width + self.spacing for child in self.children)
        widget.y = self.y
        self.children.append(widget)
