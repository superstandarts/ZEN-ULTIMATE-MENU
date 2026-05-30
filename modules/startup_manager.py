
import os, sys, winreg
from pathlib import Path

RUN_KEY = r"Software\Microsoft\Windows\CurrentVersion\Run"

class StartupManager:
    def list_items(self):
        rows = []
        try:
            with winreg.OpenKey(winreg.HKEY_CURRENT_USER, RUN_KEY, 0, winreg.KEY_READ) as key:
                i = 0
                while True:
                    try:
                        name, value, _ = winreg.EnumValue(key, i)
                        rows.append({"scope": "Current User", "name": name, "command": value})
                        i += 1
                    except OSError:
                        break
        except Exception:
            pass
        return rows

    def add_zen_startup(self, app_name="ZEN ULTIMATE MENU"):
        exe = sys.executable if getattr(sys, "frozen", False) else str(Path(__file__).resolve())
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, RUN_KEY, 0, winreg.KEY_SET_VALUE) as key:
            winreg.SetValueEx(key, app_name, 0, winreg.REG_SZ, f'"{exe}"')
        return f"Added {app_name} to startup."

    def remove_item(self, name):
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, RUN_KEY, 0, winreg.KEY_SET_VALUE) as key:
            winreg.DeleteValue(key, name)
        return f"Removed startup item: {name}"
