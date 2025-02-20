import json
import os

class UserPreferences:
    def __init__(self):
        self.config_file = 'user_prefs.json'
        self.defaults = {
            'bpm_tolerance': 5,
            'key_tolerance': 'compatible',
            'transition_style': 'smooth'
        }
        self.prefs = self._load_prefs()

    def _load_prefs(self):
        if os.path.exists(self.config_file):
            with open(self.config_file) as f:
                return json.load(f)
        return self.defaults.copy()

    def save_prefs(self):
        with open(self.config_file, 'w') as f:
            json.dump(self.prefs, f)

    def get_preference(self, key):
        return self.prefs.get(key, self.defaults.get(key))

    def set_preference(self, key, value):
        if key in self.defaults:
            self.prefs[key] = value
            self.save_prefs()