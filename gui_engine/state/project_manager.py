# gui_engine/state/project_manager.py
import os
import json
import time

SETTINGS_PATH = os.path.join(os.path.dirname(__file__), '../../app/config/settings.json')

class ProjectManager:
    def __init__(self):
        self.settings = self._load_settings()

    def _load_settings(self):
        if os.path.exists(SETTINGS_PATH):
            with open(SETTINGS_PATH, 'r') as f:
                return json.load(f)
        return {}

    def _save_settings(self):
        os.makedirs(os.path.dirname(SETTINGS_PATH), exist_ok=True)
        with open(SETTINGS_PATH, 'w') as f:
            json.dump(self.settings, f, indent=2)

    def get_recent_projects(self):
        return self.settings.get('recent_projects', [])

    def add_recent_project(self, path):
        recent = self.settings.get('recent_projects', [])
        # Remove if already exists
        recent = [p for p in recent if p['path'] != path]
        recent.insert(0, {'path': path, 'timestamp': time.strftime('%Y-%m-%d %H:%M:%S')})
        self.settings['recent_projects'] = recent[:10]
        self._save_settings()

    def clear_recent_projects(self):
        self.settings['recent_projects'] = []
        self._save_settings()

    def get_last_project(self):
        recent = self.get_recent_projects()
        return recent[0]['path'] if recent else None

    def set_last_project(self, path):
        self.add_recent_project(path)
        self._save_settings()
