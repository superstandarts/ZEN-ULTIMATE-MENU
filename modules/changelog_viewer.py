
from pathlib import Path
from datetime import datetime

class ChangelogViewer:
    def __init__(self, app_dir):
        self.path = Path(app_dir) / "CHANGELOG.md"
        if not self.path.exists():
            self.path.write_text("# Changelog\n\n## v1.0.0\n- Initial local build.\n", encoding="utf-8")

    def read(self):
        return self.path.read_text(encoding="utf-8")

    def append(self, version, text):
        content = self.read()
        entry = f"\n\n## {version} - {datetime.now().strftime('%Y-%m-%d')}\n{text}\n"
        self.path.write_text(content + entry, encoding="utf-8")
        return "Changelog updated."
