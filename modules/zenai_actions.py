
import json
from pathlib import Path

class ZENAIConfigActions:
    def __init__(self, config_path):
        self.config_path = Path(config_path)

    def load(self):
        return json.loads(self.config_path.read_text(encoding="utf-8"))

    def save(self, data):
        self.config_path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")

    def add_hotkey(self, combo, action, value):
        data = self.load()
        data.setdefault("hotkeys", []).append({"combo": combo, "action": action, "value": value})
        self.save(data)
        return f"Added hotkey {combo} -> {action}: {value}"

    def add_profile(self, name, apps_to_open=None, apps_to_close=None, folders_to_open=None):
        data = self.load()
        data.setdefault("profiles", {})[name] = {
            "apps_to_open": apps_to_open or [],
            "apps_to_close": apps_to_close or [],
            "folders_to_open": folders_to_open or [],
            "notes": "Created by ZENAI Actions"
        }
        self.save(data)
        return f"Created profile: {name}"

    def set_theme(self, theme_name):
        data = self.load()
        data.setdefault("theme", {})["mode"] = theme_name
        self.save(data)
        return f"Theme mode set to {theme_name}"
