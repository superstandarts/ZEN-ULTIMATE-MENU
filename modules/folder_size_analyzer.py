
from pathlib import Path

class FolderSizeAnalyzer:
    def folder_size(self, folder):
        total = 0
        for p in Path(folder).rglob("*"):
            try:
                if p.is_file():
                    total += p.stat().st_size
            except Exception:
                pass
        return total / 1024 / 1024

    def analyze_children(self, folder, limit=100):
        rows = []
        for child in Path(folder).iterdir():
            try:
                if child.is_dir():
                    rows.append((str(child), self.folder_size(child)))
                elif child.is_file():
                    rows.append((str(child), child.stat().st_size / 1024 / 1024))
            except Exception:
                pass
        rows.sort(key=lambda x: x[1], reverse=True)
        return rows[:limit]
