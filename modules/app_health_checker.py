
import importlib.util, json, shutil, subprocess, sys
from pathlib import Path

class AppHealthChecker:
    def __init__(self, app_dir, config_path):
        self.app_dir = Path(app_dir)
        self.config_path = Path(config_path)

    def check(self):
        rows = []
        def add(name, ok, detail=""):
            rows.append(("OK" if ok else "FAIL", name, detail))

        add("config.json", self.config_path.exists(), str(self.config_path))
        try:
            data = json.loads(self.config_path.read_text(encoding="utf-8"))
            add("config.json valid JSON", True, "loaded")
        except Exception as e:
            data = {}
            add("config.json valid JSON", False, str(e))

        add("assets folder", (self.app_dir / "assets").exists(), str(self.app_dir / "assets"))
        add("ZEN loading image", (self.app_dir / "assets" / "images" / "zen.png").exists(), "assets/images/zen.png")
        add("startup sound WAV", (self.app_dir / "assets" / "sounds" / "startup.wav").exists(), "assets/sounds/startup.wav")

        for mod in ["customtkinter","psutil","PIL","pyperclip","send2trash","spotipy","syncedlyrics"]:
            add(f"python module: {mod}", importlib.util.find_spec(mod) is not None)

        add("Git installed", shutil.which("git") is not None, shutil.which("git") or "not found")
        add("FFmpeg installed", shutil.which("ffmpeg") is not None, shutil.which("ffmpeg") or "not found")
        add("Ollama installed", shutil.which("ollama") is not None, shutil.which("ollama") or "not found")

        discord = data.get("discord", {})
        spotify = discord.get("spotify", {})
        add("Discord Client ID", bool(discord.get("client_id")), discord.get("client_id", "missing"))
        add("Spotify Client ID", bool(spotify.get("client_id")), "set" if spotify.get("client_id") else "missing")
        add("Spotify Secret", bool(spotify.get("client_secret")), "set" if spotify.get("client_secret") else "missing")

        return rows
