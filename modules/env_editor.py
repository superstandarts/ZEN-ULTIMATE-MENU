
import os, subprocess, winreg

class EnvEditor:
    REG_PATH = r"Environment"

    def list_user_env(self):
        rows = []
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, self.REG_PATH, 0, winreg.KEY_READ) as key:
            i = 0
            while True:
                try:
                    name, value, _ = winreg.EnumValue(key, i)
                    rows.append((name, value))
                    i += 1
                except OSError:
                    break
        return rows

    def set_user_env(self, name, value):
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, self.REG_PATH, 0, winreg.KEY_SET_VALUE) as key:
            winreg.SetValueEx(key, name, 0, winreg.REG_EXPAND_SZ, value)
        subprocess.run('setx "{}" "{}"'.format(name, value), shell=True, capture_output=True)
        return f"Set user env: {name}"

    def add_to_path(self, folder):
        folder = os.path.expandvars(folder)
        rows = dict(self.list_user_env())
        path = rows.get("Path") or rows.get("PATH") or ""
        parts = [p.strip() for p in path.split(";") if p.strip()]
        if folder.lower() not in [p.lower() for p in parts]:
            parts.append(folder)
        return self.set_user_env("Path", ";".join(parts))
