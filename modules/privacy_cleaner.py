
import os
import subprocess
import winreg
import pyperclip
from pathlib import Path
from send2trash import send2trash

class PrivacyCleaner:
    def clear_clipboard(self):
        pyperclip.copy("")
        return "Clipboard cleared."

    def clear_recent_files(self):
        recent = Path(os.path.expandvars(r"%APPDATA%\Microsoft\Windows\Recent"))
        count = 0
        if recent.exists():
            for item in recent.iterdir():
                try:
                    if item.is_file():
                        send2trash(str(item))
                        count += 1
                except Exception:
                    pass
        return f"Recent files moved to Recycle Bin: {count}"

    def clear_run_history(self):
        try:
            key_path = r"Software\Microsoft\Windows\CurrentVersion\Explorer\RunMRU"
            with winreg.OpenKey(winreg.HKEY_CURRENT_USER, key_path, 0, winreg.KEY_ALL_ACCESS) as key:
                values = []
                i = 0
                while True:
                    try:
                        values.append(winreg.EnumValue(key, i)[0])
                        i += 1
                    except OSError:
                        break
                for name in values:
                    try:
                        winreg.DeleteValue(key, name)
                    except Exception:
                        pass
            return "Run history cleared."
        except Exception as e:
            return f"Could not clear Run history: {e}"

    def clear_explorer_history(self):
        try:
            subprocess.run(["RunDll32.exe", "InetCpl.cpl,ClearMyTracksByProcess", "1"], shell=True)
            return "Explorer/Windows recent history command executed."
        except Exception as e:
            return f"Could not clear Explorer history: {e}"
