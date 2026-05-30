
import os, subprocess, webbrowser
from pathlib import Path
import pyperclip

class QuickLauncher:
    def __init__(self, config):
        self.items = config.get("quick_launcher", [])

    def run(self, item):
        typ = item.get("type", "url")
        value = os.path.expandvars(item.get("value", ""))
        if typ == "url":
            webbrowser.open(value)
        elif typ == "folder":
            os.startfile(Path(value))
        elif typ == "app":
            subprocess.Popen(value, shell=True)
        elif typ == "copy":
            pyperclip.copy(value)
        return f"Executed: {item.get('name', value)}"
