
import os, re, subprocess, winreg
from pathlib import Path
from send2trash import send2trash

UNINSTALL_KEYS = [
    (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall"),
    (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall"),
    (winreg.HKEY_CURRENT_USER, r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall"),
]

class UltimateUninstaller:
    def installed_apps(self):
        apps = []
        for hive, path in UNINSTALL_KEYS:
            try:
                with winreg.OpenKey(hive, path) as key:
                    i = 0
                    while True:
                        try:
                            sub = winreg.EnumKey(key, i)
                            with winreg.OpenKey(key, sub) as appkey:
                                name = self._get(appkey, "DisplayName")
                                if name:
                                    apps.append({
                                        "name": name,
                                        "publisher": self._get(appkey, "Publisher"),
                                        "version": self._get(appkey, "DisplayVersion"),
                                        "uninstall": self._get(appkey, "UninstallString"),
                                        "install_location": self._get(appkey, "InstallLocation")
                                    })
                            i += 1
                        except OSError:
                            break
            except Exception:
                pass
        apps.sort(key=lambda x: x["name"].lower())
        return apps

    def _get(self, key, name):
        try:
            return winreg.QueryValueEx(key, name)[0]
        except Exception:
            return ""

    def run_uninstaller(self, app):
        cmd = app.get("uninstall")
        if not cmd:
            return "No uninstall command found."
        subprocess.Popen(cmd, shell=True)
        return "Uninstaller launched. Finish the official uninstaller first, then scan leftovers."

    def scan_leftovers(self, app_name, roots):
        safe_name = re.sub(r"[^a-zA-Z0-9 _.-]", "", app_name).strip()
        if len(safe_name) < 3:
            return []
        terms = [t.lower() for t in safe_name.split() if len(t) >= 3]
        if not terms:
            terms = [safe_name.lower()]
        found = []
        for raw_root in roots:
            root = Path(os.path.expandvars(raw_root))
            if not root.exists():
                continue
            try:
                for p in root.rglob("*"):
                    try:
                        name = p.name.lower()
                        if any(term in name for term in terms):
                            found.append(str(p))
                            if len(found) >= 500:
                                return found
                    except Exception:
                        pass
            except Exception:
                pass
        return found

    def remove_leftovers_safe(self, paths):
        moved, failed = 0, 0
        for p in paths:
            try:
                send2trash(p)
                moved += 1
            except Exception:
                failed += 1
        return f"Moved to Recycle Bin: {moved} | Failed: {failed}"
