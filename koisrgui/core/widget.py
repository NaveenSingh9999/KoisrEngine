# koisrgui/core/widget.py
import pygame

class Widget:
    def __init__(self, x, y, width, height, visible=True, z_index=0):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.visible = visible
        self.z_index = z_index
        self.focused = False
        self.parent = None
        self.children = []
        self.style = {}

    def draw(self, surface):
        if not self.visible:
            return
        for child in sorted(self.children, key=lambda w: w.z_index):
            child.draw(surface)

    def update(self, dt):
        for child in self.children:
            child.update(dt)

    def handle_event(self, event):
        for child in self.children:
            child.handle_event(event)

    def add_child(self, widget):
        widget.parent = self
        self.children.append(widget)

    def set_style(self, style_dict):
        self.style.update(style_dict)

    def set_focus(self, focused):
        self.focused = focused
