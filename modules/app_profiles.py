
import os
import subprocess
import psutil
from pathlib import Path

class AppProfiles:
    def __init__(self, config, logger=print):
        self.config = config
        self.logger = logger

    def profiles(self):
        return self.config.get("profiles", {})

    def run_profile(self, name):
        profile = self.profiles().get(name)
        if not profile:
            return f"Profile not found: {name}"

        closed = []
        opened = []
        for proc_name in profile.get("apps_to_close", []):
            for proc in psutil.process_iter(["name"]):
                try:
                    if proc.info["name"] and proc.info["name"].lower() == proc_name.lower():
                        proc.terminate()
                        closed.append(proc_name)
                except Exception:
                    pass

        for app in profile.get("apps_to_open", []):
            try:
                subprocess.Popen(app, shell=True)
                opened.append(app)
            except Exception:
                pass

        for folder in profile.get("folders_to_open", []):
            try:
                os.startfile(Path(os.path.expandvars(folder)))
                opened.append(folder)
            except Exception:
                pass

        return f"Profile '{name}' executed. Opened: {len(opened)} | Closed: {len(closed)}"
