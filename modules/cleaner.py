import os
import tempfile
from pathlib import Path
from send2trash import send2trash

class Cleaner:
    def __init__(self):
        self.targets = [
            ("User Temp", Path(tempfile.gettempdir())),
            ("Windows Temp", Path(os.getenv("WINDIR", "C:/Windows")) / "Temp"),
            ("Prefetch", Path(os.getenv("WINDIR", "C:/Windows")) / "Prefetch"),
            ("Discord Cache", Path(os.getenv("APPDATA", "")) / "discord" / "Cache"),
            ("Chrome Cache", Path(os.getenv("LOCALAPPDATA", "")) / "Google" / "Chrome" / "User Data" / "Default" / "Cache"),
            ("Edge Cache", Path(os.getenv("LOCALAPPDATA", "")) / "Microsoft" / "Edge" / "User Data" / "Default" / "Cache"),
            ("VS Code Cache", Path(os.getenv("APPDATA", "")) / "Code" / "Cache"),
            ("Roblox Logs", Path(os.getenv("LOCALAPPDATA", "")) / "Roblox" / "logs"),
        ]
        self.last_scan = []

    def _scan_path(self, path):
        size = 0
        items = []
        if not path.exists():
            return size, items
        try:
            for p in path.rglob("*"):
                try:
                    if p.is_file():
                        size += p.stat().st_size
                        items.append(p)
                except Exception:
                    continue
        except Exception:
            pass
        return size, items

    def scan(self):
        results = []
        self.last_scan = []
        for name, path in self.targets:
            size, items = self._scan_path(path)
            results.append({"name": name, "path": path, "items": len(items), "size_mb": size / 1024 / 1024})
            self.last_scan.extend(items)
        return results

    def clean_safe(self):
        if not self.last_scan:
            self.scan()
        summary = []
        cleaned = 0
        failed = 0
        for item in list(self.last_scan):
            try:
                if item.exists() and item.is_file():
                    send2trash(str(item))
                    cleaned += 1
            except Exception:
                failed += 1
        summary.append(f"Moved to Recycle Bin: {cleaned}")
        summary.append(f"Failed: {failed}")
        return summary
