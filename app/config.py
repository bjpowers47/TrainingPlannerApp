from pathlib import Path
import json
import os
import sys

from app.services.atomic_json import write_json_atomic

APP_NAME = "Wildcat Training Planner"
WINDOW_TITLE = "Training Planner"
APP_VERSION = "0.4.0"

RESOURCE_ROOT = Path(getattr(sys, "_MEIPASS", Path(__file__).parent.parent))
ROOT = (
    Path(os.environ.get("LOCALAPPDATA", Path.home() / "AppData" / "Local"))
    / "TrainingPlannerAp"
    if getattr(sys, "frozen", False)
    else RESOURCE_ROOT
)
ROOT.mkdir(parents=True, exist_ok=True)

CONFIG_DIR = ROOT / "data"
CONFIG_DIR.mkdir(parents=True, exist_ok=True)

BACKUP_DIR = ROOT / "backups"
BACKUP_DIR.mkdir(parents=True, exist_ok=True)

PRACTICES_DIR = ROOT / "practices"
PRACTICES_DIR.mkdir(parents=True, exist_ok=True)
AUTOSAVE_FILE = CONFIG_DIR / "practice_autosave.json"

CONFIG_FILE = CONFIG_DIR / "config.json"


DEFAULT_CONFIG = {
    "theme": "dark",
    "last_workbook": "",
    "window_width": 1400,
    "window_height": 900,
    "sport": "",
    "head_coach": "",
    "assistant_coaches": [],
    "recent_practices": [],
    "last_practice_folder": str(PRACTICES_DIR),
}


def training_manager_name(sport=""):
    """Build the configurable user-facing Training Manager name."""
    clean_sport = str(sport or "").strip()[:15]
    return f"{clean_sport} Training Manager" if clean_sport else "Training Manager"


class ConfigManager:

    def __init__(self):
        self.data = DEFAULT_CONFIG.copy()
        self.load()

    def load(self):
        if CONFIG_FILE.exists():
            try:
                with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                    self.data.update(json.load(f))
            except (OSError, json.JSONDecodeError):
                # A damaged preference file should never prevent startup.
                self.data = DEFAULT_CONFIG.copy()

    def save(self):
        write_json_atomic(CONFIG_FILE, self.data)

    def remember_practice(self, filename):
        """Keep a short most-recently-used list for the dashboard."""
        path = str(Path(filename).resolve())
        recent = [item for item in self.data.get("recent_practices", []) if item != path]
        self.data["recent_practices"] = [path, *recent][:8]
        self.data["last_practice_folder"] = str(Path(path).parent)
        self.save()

    def forget_practice(self, filename):
        """Remove a practice from history without deleting its file."""
        path = str(Path(filename).resolve())
        self.data["recent_practices"] = [
            item for item in self.data.get("recent_practices", []) if item != path
        ]
        self.save()
