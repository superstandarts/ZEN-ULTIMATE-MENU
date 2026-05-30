
from pathlib import Path
from send2trash import send2trash

class LargeFileFinder:
    def scan(self, folder, min_mb=100, limit=500):
        folder = Path(folder)
        rows = []
        for p in folder.rglob("*"):
            try:
                if p.is_file():
                    mb = p.stat().st_size / 1024 / 1024
                    if mb >= float(min_mb):
                        rows.append((str(p), mb))
            except Exception:
                pass
        rows.sort(key=lambda x: x[1], reverse=True)
        return rows[:limit]

    def recycle(self, paths):
        moved = 0
        for p in paths:
            try:
                send2trash(p); moved += 1
            except Exception:
                pass
        return f"Moved large files to Recycle Bin: {moved}"
