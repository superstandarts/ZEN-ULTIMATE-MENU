
import subprocess, webbrowser, os

class WindowsRepair:
    def run(self, command_name):
        commands = {
            "Flush DNS": ["ipconfig", "/flushdns"],
            "Reset Winsock": ["netsh", "winsock", "reset"],
            "SFC Scan": ["sfc", "/scannow"],
            "DISM RestoreHealth": ["DISM", "/Online", "/Cleanup-Image", "/RestoreHealth"],
            "Clear Icon Cache": ["cmd", "/c", "ie4uinit.exe -show"],
            "Restart Explorer": ["cmd", "/c", "taskkill /f /im explorer.exe && start explorer.exe"]
        }
        cmd = commands.get(command_name)
        if not cmd:
            return "Unknown command."
        result = subprocess.run(cmd, capture_output=True, text=True, shell=False)
        return (result.stdout or "") + (result.stderr or "")

    def open_settings(self):
        webbrowser.open("ms-settings:")
