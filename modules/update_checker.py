
import json, urllib.request

class UpdateChecker:
    def __init__(self, current_version="1.0.0", release_url=""):
        self.current_version = current_version
        self.release_url = release_url

    def check(self, url=""):
        target = url or self.release_url
        if not target:
            return "No update URL configured. Put a GitHub releases/latest API URL in config.json."
        try:
            with urllib.request.urlopen(target, timeout=10) as r:
                data = json.loads(r.read().decode("utf-8", errors="replace"))
            latest = data.get("tag_name") or data.get("name") or "unknown"
            html = data.get("html_url", "")
            return f"Current: {self.current_version}\nLatest: {latest}\nURL: {html}"
        except Exception as e:
            return f"Update check failed: {e}"
