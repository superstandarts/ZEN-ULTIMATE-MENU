import os
import sys
import json
import shutil
import subprocess
import webbrowser
from pathlib import Path
from datetime import datetime

try:
    import tkinter as tk
    from tkinter import filedialog, messagebox, simpledialog
except Exception:
    tk = None

APP_DIR = Path(__file__).resolve().parent

TEMPLATE = """import tkinter as tk
from tkinter import messagebox

def main():
    root = tk.Tk()
    root.title("{name}")
    root.geometry("420x220")
    tk.Label(root, text="{name}", font=("Segoe UI", 18, "bold")).pack(pady=20)
    tk.Button(root, text="Run", command=lambda: messagebox.showinfo("{name}", "Plugin running!")).pack(pady=10)
    root.mainloop()

if __name__ == "__main__":
    main()
"""

def main():
    if tk is None:
        print("Tkinter unavailable.")
        return
    root = tk.Tk()
    root.withdraw()
    app_dir = Path(__file__).resolve().parents[2]
    plugins = app_dir / "plugins"
    plugins.mkdir(exist_ok=True)
    name = simpledialog.askstring("Plugin Creator", "Plugin name:", initialvalue="ZEN My Plugin")
    if not name:
        return
    folder_name = name.lower().replace(" ", "_").replace("-", "_")
    folder = plugins / folder_name
    folder.mkdir(exist_ok=True)
    manifest = {
        "name": name,
        "entry": "main.py",
        "description": "Created with ZEN Plugin Creator.",
        "version": "1.0.0",
        "author": "Zen"
    }
    (folder / "plugin.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    (folder / "main.py").write_text(TEMPLATE.format(name=name), encoding="utf-8")
    (folder / "README.md").write_text(f"# {name}\\n\\nCreated with ZEN Plugin Creator.\\n", encoding="utf-8")
    messagebox.showinfo("Plugin Creator", f"Created:\n{folder}")

if __name__ == "__main__":
    main()
