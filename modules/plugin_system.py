
import json, subprocess, sys
from pathlib import Path

class PluginSystem:
    def __init__(self, app_dir):
        self.plugins_dir = Path(app_dir) / "plugins"
        self.plugins_dir.mkdir(exist_ok=True)

    def list_plugins(self):
        rows = []
        for folder in self.plugins_dir.iterdir():
            if not folder.is_dir():
                continue
            manifest = folder / "plugin.json"
            if manifest.exists():
                try:
                    data = json.loads(manifest.read_text(encoding="utf-8"))
                    data["_path"] = str(folder)
                    rows.append(data)
                except Exception:
                    pass
        return rows

    def create_example(self):
        folder = self.plugins_dir / "example_plugin"
        folder.mkdir(exist_ok=True)
        (folder / "plugin.json").write_text(json.dumps({
            "name": "Example Plugin",
            "entry": "main.py",
            "description": "Example external plugin."
        }, indent=2), encoding="utf-8")
        (folder / "main.py").write_text("print('Hello from ZEN plugin!')\ninput('Press enter...')\n", encoding="utf-8")
        return str(folder)

    def run_plugin(self, plugin):
        folder = Path(plugin["_path"])
        entry = plugin.get("entry", "main.py")
        subprocess.Popen([sys.executable, str(folder / entry)], cwd=str(folder))
        return f"Started plugin: {plugin.get('name')}"
