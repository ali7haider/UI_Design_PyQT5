import json
import os

CONFIG_FILE = "paths_config.json"

DEFAULT_PATHS = {
    "Zoek_Afscheiding": None,
    "Zoek_Meting": None,
    "Zoek_SVO": None,
    "Zoek_Plan": None,
    "Sjablonen": None,
    "Installatie": None,
    "Opleiding": None,
    "WinCC": None,
    "Vragen": None,
    "E_Learning": None,
    "Foto":None,
    "password_wincc": "KBT.REG.APP",
    "password_education": "intranerd"
}

class PathManager:
    """Handles loading and saving paths from a JSON configuration file."""

    def __init__(self):
        self.paths = self.load_paths()

    def load_paths(self):
        """Load paths from the JSON file, or create it with default values if missing."""
        if not os.path.exists(CONFIG_FILE):
            self.save_paths(DEFAULT_PATHS)  # Create with default structure

        try:
            with open(CONFIG_FILE, "r") as file:
                paths = json.load(file)
        except json.JSONDecodeError:
            paths = {}

        # Ensure all keys exist in the loaded JSON
        for key in DEFAULT_PATHS:
            if key not in paths:
                paths[key] = None

        self.save_paths(paths)  # Save any missing keys back to the file
        return paths

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
