
import hashlib
from pathlib import Path
from send2trash import send2trash

class DuplicateFinder:
    def sha256(self, path):
        h = hashlib.sha256()
        with open(path, "rb") as f:
            for chunk in iter(lambda: f.read(1024 * 1024), b""):
                h.update(chunk)
        return h.hexdigest()

    def scan(self, folder, limit=5000):
        folder = Path(folder)
        seen = {}
        dups = []
        count = 0
        for p in folder.rglob("*"):
            if not p.is_file():
                continue
            try:
                key = (p.stat().st_size, self.sha256(p))
                if key in seen:
                    dups.append((str(seen[key]), str(p), p.stat().st_size))
                else:
                    seen[key] = p
                count += 1
                if count >= limit:
                    break
            except Exception:
                pass
        return dups

    def recycle(self, paths):
        moved = 0
        for p in paths:
            try:
                send2trash(p)
                moved += 1
            except Exception:
                pass
        return f"Moved duplicates to Recycle Bin: {moved}"
