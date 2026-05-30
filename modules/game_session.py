import os
import subprocess
import psutil
from pathlib import Path

class GameSession:
    def __init__(self, config, logger=print):
        self.config = config.get("game_session", {})
        self.logger = logger

    def _close_process(self, name):
        for proc in psutil.process_iter(["name"]):
            try:
                if proc.info["name"] and proc.info["name"].lower() == name.lower():
                    proc.terminate()
                    self.logger(f"Closed: {name}")
            except Exception:
                pass

    def start_session(self):
        for name in self.config.get("apps_to_close", []):
            self._close_process(name)
        for app in self.config.get("apps_to_open", []):
            try:
                subprocess.Popen(app, shell=True)
                self.logger(f"Opened: {app}")
            except Exception:
                pass
        for folder in self.config.get("folders_to_open", []):
            try:
                os.startfile(Path(os.path.expandvars(folder)))
            except Exception:
                pass

    def end_session(self):
        self.logger("Game session ended. Add custom behavior in config.json.")
