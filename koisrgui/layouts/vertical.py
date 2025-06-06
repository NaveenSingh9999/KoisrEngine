# koisrgui/layouts/vertical.py
from koisrgui.core.widget import Widget

class VerticalLayout(Widget):
    def __init__(self, x, y, spacing=8):
        super().__init__(x, y, 0, 0)
        self.spacing = spacing

    def add_child(self, widget):
        widget.parent = self
        widget.x = self.x
        widget.y = self.y + sum(child.height + self.spacing for child in self.children)
        self.children.append(widget)
