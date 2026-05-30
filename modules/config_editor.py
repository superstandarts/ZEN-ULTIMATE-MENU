
import json
from pathlib import Path

class ConfigEditor:
    def __init__(self, path):
        self.path = Path(path)

    def load_text(self):
        return self.path.read_text(encoding="utf-8")

    def load_json(self):
        return json.loads(self.load_text())

    def save_text(self, text):
        json.loads(text)  # validate
        self.path.write_text(text, encoding="utf-8")

    def update_path(self, keys, value):
        data = self.load_json()
        cur = data
        for key in keys[:-1]:
            cur = cur.setdefault(key, {})
        cur[keys[-1]] = value
        self.path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
        return data
