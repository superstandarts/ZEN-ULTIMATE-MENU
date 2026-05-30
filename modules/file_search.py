from pathlib import Path
from datetime import datetime

class SmartFileSearch:
    def search(self, folder, query, limit=200):
        root = Path(folder)
        query = (query or "").lower().strip()
        results = []
        if not root.exists():
            return results

        for p in root.rglob("*"):
            if len(results) >= limit:
                break
            try:
                if not p.is_file():
                    continue
                text = str(p).lower()
                if not query or query in text or (query.startswith(".") and p.suffix.lower() == query):
                    results.append(p)
            except Exception:
                continue
        return results
