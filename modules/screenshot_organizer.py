import os
import shutil
from pathlib import Path
from datetime import datetime

class ScreenshotOrganizer:
    def __init__(self, config):
        cfg = config.get("screenshot_organizer", {})
        self.source = Path(os.path.expandvars(cfg.get("source", "%USERPROFILE%\\Pictures\\Screenshots")))
        self.destination = Path(os.path.expandvars(cfg.get("destination", "%USERPROFILE%\\Pictures\\CRX Screenshots")))
        self.extensions = {".png", ".jpg", ".jpeg", ".webp", ".bmp"}

    def organize(self):
        if not self.source.exists():
            return 0
        moved = 0
        self.destination.mkdir(parents=True, exist_ok=True)
        for file in self.source.iterdir():
            if file.is_file() and file.suffix.lower() in self.extensions:
                date_folder = datetime.fromtimestamp(file.stat().st_mtime).strftime("%Y-%m")
                target_dir = self.destination / date_folder
                target_dir.mkdir(parents=True, exist_ok=True)
                target = target_dir / file.name
                n = 1
                while target.exists():
                    target = target_dir / f"{file.stem}_{n}{file.suffix}"
                    n += 1
                try:
                    shutil.move(str(file), str(target))
                    moved += 1
                except Exception:
                    pass
        return moved
