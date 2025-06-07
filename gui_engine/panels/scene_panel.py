from koisrgui.widgets.panel import Panel
from koisrgui.widgets.label import Label
from koisrgui.widgets.button import Button

class ScenePanel(Panel):
    def __init__(self, *args, engine=None, style=None, **kwargs):
        super().__init__(*args, title="Scene Hierarchy", style=style, **kwargs)
        self.engine = engine
        self.selected_id = None
        self.objects_expanded = {}  # Track expanded/collapsed state
        self._build_ui()
        
    def _build_ui(self):
        self.children.clear()
        
        # Add "Create" button at top
        self.add_child(Button(self.x + 8, self.y + 32, 80, 24, "+ Create", on_click=self._show_create_menu))
        
        # Add search box placeholder
        self.add_child(Label(self.x + 100, self.y + 32, 140, 24, "Search (coming soon)"))
        
        # Scene objects list
        if self.engine:
            y_offset = self.y + 64
            for obj in self.engine.get_game_objects():
                # Object entry with icon
                expanded = self.objects_expanded.get(obj.id, False)
                icon = "▼ " if expanded else "► "
                btn = Button(self.x + 8, y_offset, self.width - 16, 28, 
                           f"{icon}{obj.name}", 
                           on_click=lambda o=obj: self.select_object(o))
                
                # Highlight selected object
                if self.selected_id == obj.id:
                    btn.style.update({'bg': (70, 100, 160)})
                    
                self.add_child(btn)
                y_offset += 36
                
                # Show components if expanded
                if expanded:
                    for component in obj.components:
                        comp_name = component.__class__.__name__
                        comp_btn = Button(self.x + 24, y_offset, self.width - 32, 24, 
                                       f"   {comp_name}", 
                                       on_click=lambda o=obj: self.select_object(o))
                        comp_btn.style.update({'bg': (50, 50, 55), 'font_size': 14})
                        self.add_child(comp_btn)
                        y_offset += 28

    def _show_create_menu(self):
        # This would show a dropdown menu in a full implementation
        if self.engine:
            from engine.game_object import GameObject
            new_obj = GameObject(f"New Object {len(self.engine.get_game_objects())}")
            self.engine.add_game_object(new_obj)
            self._build_ui()

    def select_object(self, obj):
        # Toggle expanded state if same object clicked again
        if self.selected_id == obj.id:
            self.objects_expanded[obj.id] = not self.objects_expanded.get(obj.id, False)
        
        self.selected_id = obj.id
        
        # Notify engine about selection
        if hasattr(self.engine, 'selected_object'):
            self.engine.selected_object = obj
            
        self._build_ui()

    def update(self, dt):
        # Only rebuild UI when objects change, not every frame
        for child in self.children:
            child.update(dt)

    def draw(self, surface):
        super().draw(surface)
