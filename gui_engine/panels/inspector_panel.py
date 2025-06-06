from koisrgui.widgets.panel import Panel
from koisrgui.widgets.label import Label
from koisrgui.widgets.button import Button
from gui_engine.state.global_state import GlobalState
import pygame

class InspectorPanel(Panel):
    def __init__(self, engine, *args, **kwargs):
        super().__init__(title="Inspector", *args, **kwargs)
        self.engine = engine
        self._build_ui()
    def _build_ui(self):
        self.children.clear()
        obj = self.engine.get_selected_object()
        y = self.y + 32
        if obj:
            self.add_child(Label(self.x + 8, y, self.width - 16, 28, f"Name: {obj.name}"))
            y += 36
            t = obj.transform
            for i, axis in enumerate(['X', 'Y', 'Z']):
                self.add_child(Label(self.x + 8, y, 40, 28, f"Pos {axis}:"))
                self.add_child(Button(self.x + 56, y, 60, 28, str(round(t.position[i], 2)), on_click=lambda idx=i: self.edit_value(obj, 'position', idx)))
                y += 32
            for i, axis in enumerate(['X', 'Y', 'Z']):
                self.add_child(Label(self.x + 8, y, 40, 28, f"Rot {axis}:"))
                self.add_child(Button(self.x + 56, y, 60, 28, str(round(t.rotation[i], 2)), on_click=lambda idx=i: self.edit_value(obj, 'rotation', idx)))
                y += 32
            for i, axis in enumerate(['X', 'Y', 'Z']):
                self.add_child(Label(self.x + 8, y, 40, 28, f"Scale {axis}:"))
                self.add_child(Button(self.x + 56, y, 60, 28, str(round(t.scale[i], 2)), on_click=lambda idx=i: self.edit_value(obj, 'scale', idx)))
                y += 32
    def edit_value(self, obj, attr, idx):
        import tkinter as tk
        from tkinter import simpledialog
        root = tk.Tk()
        root.withdraw()
        val = simpledialog.askfloat(f"Edit {attr}", f"Enter new value for {attr}[{idx}]:", initialvalue=getattr(obj.transform, attr)[idx])
        if val is not None:
            getattr(obj.transform, attr)[idx] = val
            self._build_ui()
    def update(self, dt):
        self._build_ui()
        super().update(dt)
