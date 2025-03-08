import json
import os

CONFIG_FILE = "paths_config.json"  # Updated JSON file name

class PathManager:
    """Handles loading and saving paths from a JSON configuration file."""
    
    def __init__(self):
        self.paths = self.load_paths()

    def load_paths(self):
        """Load paths from the JSON file, or create a default one if missing."""
        if not os.path.exists(CONFIG_FILE):
            self.save_paths({})  # Create an empty JSON file if not found
        try:
            with open(CONFIG_FILE, "r") as file:
                return json.load(file)
        except json.JSONDecodeError:
            return {}

    def save_paths(self, paths):
        """Save paths to the JSON file."""
        with open(CONFIG_FILE, "w") as file:
            json.dump(paths, file, indent=4)

    def get_path(self, key):
        """Retrieve a path from the JSON."""
        return self.paths.get(key, "")

    def set_path(self, key, value):
        """Set a new path and save it."""
        self.paths[key] = value
        self.save_paths(self.paths)
