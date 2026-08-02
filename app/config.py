from pathlib import Path
import json
import sys

APP_NAME = "Training Manager"

RESOURCE_ROOT = Path(getattr(sys, "_MEIPASS", Path(__file__).parent.parent))
ROOT = Path(sys.executable).parent if getattr(sys, "frozen", False) else RESOURCE_ROOT

CONFIG_DIR = ROOT / "data"
CONFIG_DIR.mkdir(parents=True, exist_ok=True)

BACKUP_DIR = ROOT / "backups"
BACKUP_DIR.mkdir(parents=True, exist_ok=True)

CONFIG_FILE = CONFIG_DIR / "config.json"


DEFAULT_CONFIG = {
    "theme": "dark",
    "last_workbook": "",
    "window_width": 1400,
    "window_height": 900
}


class ConfigManager:

    def __init__(self):
        self.data = DEFAULT_CONFIG.copy()
        self.load()

    def load(self):
        if CONFIG_FILE.exists():
            with open(CONFIG_FILE, "r") as f:
                self.data.update(json.load(f))

    def save(self):
        with open(CONFIG_FILE, "w") as f:
            json.dump(self.data, f, indent=4)
