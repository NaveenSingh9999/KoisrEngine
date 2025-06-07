from koisrgui.widgets.panel import Panel
from koisrgui.widgets.label import Label
from koisrgui.widgets.button import Button

class InspectorPanel(Panel):
    def __init__(self, *args, engine=None, style=None, **kwargs):
        super().__init__(*args, title="Inspector", style=style, **kwargs)
        self.engine = engine
        self.editing_values = {}  # Store fields being edited
        self._build_ui()
        
    def _build_ui(self):
        self.children.clear()
        
        # Get selected object from engine
        obj = getattr(self.engine, 'selected_object', None)
        
        if obj:
            # Object name and header
            self.add_child(Label(self.x + 8, self.y + 32, 180, 24, f"Name: {obj.name}", 
                               style={'font_size': 16, 'fg': (220, 220, 220)}))
            
            # Add button to add components
            self.add_child(Button(self.x + self.width - 100, self.y + 32, 90, 24, 
                                "Add Component", 
                                on_click=self._show_component_menu))
            
            # Transform component UI
            if hasattr(obj, 'transform'):
                t = obj.transform
                y_pos = self.y + 64
                
                # Transform header with collapsible UI
                self.add_child(Label(self.x + 8, y_pos, self.width - 16, 24, 
                                   "Transform", 
                                   style={'bg': (60, 60, 70), 'fg': (220, 220, 220)}))
                y_pos += 32
                
                # Position values
                self.add_child(Label(self.x + 8, y_pos, 60, 24, "Position:"))
                for i, axis in enumerate(['X', 'Y', 'Z']):
                    # Label for axis
                    self.add_child(Label(self.x + 70, y_pos + i*28, 15, 24, axis))
                    
                    # Editable value field (using a button as a basic input field)
                    value_btn = Button(self.x + 90, y_pos + i*28, 60, 24, 
                                    f"{t.position[i]:.2f}", 
                                    on_click=lambda idx=i: self._edit_position(idx))
                    self.add_child(value_btn)
                    
                y_pos += 90
                
                # Rotation values
                self.add_child(Label(self.x + 8, y_pos, 60, 24, "Rotation:"))
                for i, axis in enumerate(['X', 'Y', 'Z']):
                    self.add_child(Label(self.x + 70, y_pos + i*28, 15, 24, axis))
                    value_btn = Button(self.x + 90, y_pos + i*28, 60, 24, 
                                    f"{t.rotation[i]:.2f}", 
                                    on_click=lambda idx=i: self._edit_rotation(idx))
                    self.add_child(value_btn)
                
                y_pos += 90
                
                # Scale values
                self.add_child(Label(self.x + 8, y_pos, 60, 24, "Scale:"))
                for i, axis in enumerate(['X', 'Y', 'Z']):
                    self.add_child(Label(self.x + 70, y_pos + i*28, 15, 24, axis))
                    value_btn = Button(self.x + 90, y_pos + i*28, 60, 24, 
                                    f"{t.scale[i]:.2f}", 
                                    on_click=lambda idx=i: self._edit_scale(idx))
                    self.add_child(value_btn)
                
                # Display any other components
                y_pos += 90
                for comp in obj.components:
                    if comp != obj.transform:  # Skip transform, already shown above
                        comp_name = comp.__class__.__name__
                        self.add_child(Label(self.x + 8, y_pos, self.width - 16, 24, 
                                          comp_name, 
                                          style={'bg': (60, 60, 70), 'fg': (220, 220, 220)}))
                        y_pos += 32
        else:
            self.add_child(Label(self.x + 8, self.y + 32, 180, 24, "No object selected", 
                               style={'fg': (180, 180, 180)}))
            
            # Show a help message
            self.add_child(Label(self.x + 8, self.y + 64, self.width - 16, 24, 
                               "Select an object in the Scene Hierarchy", 
                               style={'fg': (160, 160, 160), 'font_size': 14}))
    
    def _show_component_menu(self):
        # In a real implementation, this would show a dropdown of available components
        # For now, we'll just print a message
        print("Add Component menu would appear here")
    
    def _edit_position(self, index):
        obj = getattr(self.engine, 'selected_object', None)
        if obj and hasattr(obj, 'transform'):
            # In a real implementation, this would open an input field
            # For now, we'll just increment the value
            obj.transform.position[index] += 0.5
            self._build_ui()
    
    def _edit_rotation(self, index):
        obj = getattr(self.engine, 'selected_object', None)
        if obj and hasattr(obj, 'transform'):
            obj.transform.rotation[index] += 15.0  # Rotate by 15 degrees
            self._build_ui()
    
    def _edit_scale(self, index):
        obj = getattr(self.engine, 'selected_object', None)
        if obj and hasattr(obj, 'transform'):
            obj.transform.scale[index] += 0.1
            self._build_ui()
            
    def update(self, dt):
        # Rebuild UI only when selection changes, not every frame
        for child in self.children:
            child.update(dt)
    
    def draw(self, surface):
        super().draw(surface)
