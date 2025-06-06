class GlobalState:
    def __init__(self):
        self.selected_object = None
        self.log_messages = []
        self.assets = []
        self.scene_tree = None
        # Add more shared state as needed

    def select_object(self, obj):
        self.selected_object = obj

    def add_log(self, msg):
        self.log_messages.append(msg)

    def set_assets(self, assets):
        self.assets = assets

    def set_scene_tree(self, tree):
        self.scene_tree = tree
