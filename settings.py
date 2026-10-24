import json, os
from pathlib import Path

CONFIG_DIR = Path(os.environ.get("APPDATA", ".")) / "NovaCleaner"
CONFIG_FILE = CONFIG_DIR / "settings.json"

DEFAULTS = {
    "theme": "system",
    "first_run": True,
    "run_on_startup": False,
    "shredder_passes": 1,
    "auto_check_updates": False,
    "temp_user": True,
    "temp_windows": True,
    "temp_localappdata": True,
}

class Settings:
    def __init__(self):
        CONFIG_DIR.mkdir(parents=True, exist_ok=True)
        self._data = dict(DEFAULTS)
        if CONFIG_FILE.exists():
            try:
                self._data.update(json.loads(CONFIG_FILE.read_text()))
            except Exception:
                pass

    def get(self, key, default=None):
        return self._data.get(key, DEFAULTS.get(key, default))

    def set(self, key, value):
        self._data[key] = value
        CONFIG_FILE.write_text(json.dumps(self._data, indent=2))

    @property
    def theme(self): return self.get("theme")
    @theme.setter
    def theme(self, v): self.set("theme", v)

    @property
    def first_run(self): return self.get("first_run")
    @first_run.setter
    def first_run(self, v): self.set("first_run", v)

    @property
    def shredder_passes(self): return self.get("shredder_passes")
    @shredder_passes.setter
    def shredder_passes(self, v): self.set("shredder_passes", v)

    @property
    def run_on_startup(self): return self.get("run_on_startup")
    @run_on_startup.setter
    def run_on_startup(self, v): self.set("run_on_startup", v)

    @property
    def auto_check_updates(self): return self.get("auto_check_updates")
    @auto_check_updates.setter
    def auto_check_updates(self, v): self.set("auto_check_updates", v)

    @property
    def temp_user(self): return self.get("temp_user")
    @temp_user.setter
    def temp_user(self, v): self.set("temp_user", v)

    @property
    def temp_windows(self): return self.get("temp_windows")
    @temp_windows.setter
    def temp_windows(self, v): self.set("temp_windows", v)

    @property
    def temp_localappdata(self): return self.get("temp_localappdata")
    @temp_localappdata.setter
    def temp_localappdata(self, v): self.set("temp_localappdata", v)

settings = Settings()