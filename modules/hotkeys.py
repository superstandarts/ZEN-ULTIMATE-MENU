import os
import subprocess
import webbrowser
import keyboard
import pyperclip

class HotkeyManager:
    def __init__(self, config, logger=print):
        self.hotkeys = config.get("hotkeys", [])
        self.logger = logger
        self.active = False

    def _run_action(self, action, value):
        if action == "open_url":
            webbrowser.open(value)
        elif action == "open_app":
            try:
                subprocess.Popen(value, shell=True)
            except Exception:
                pass
        elif action == "copy_text":
            pyperclip.copy(value)
        self.logger(f"Hotkey action: {action} -> {value}")

    def start(self):
        if self.active:
            return
        for hk in self.hotkeys:
            keyboard.add_hotkey(hk["combo"], lambda h=hk: self._run_action(h.get("action"), h.get("value")))
            self.logger(f"Registered hotkey: {hk['combo']}")
        self.active = True

    def stop(self):
        keyboard.clear_all_hotkeys()
        self.active = False
        self.logger("All hotkeys stopped.")
