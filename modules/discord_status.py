import re
import time
import threading
from typing import Dict, List, Optional, Tuple, Any

import psutil
from pypresence import Presence

try:
    import spotipy
    from spotipy.oauth2 import SpotifyOAuth
except Exception:
    spotipy = None
    SpotifyOAuth = None

try:
    import syncedlyrics
except Exception:
    syncedlyrics = None


class DiscordStatus:
    def __init__(self, config):
        self.config = config.get("discord", {})
        self.rpc = None
        self.spotify = None
        self.running = False
        self.thread = None
        self.lyrics_cache: Dict[str, List[Tuple[int, str]]] = {}
        self.last_payload = None
        self.last_update = 0

    def _truncate(self, text: str, limit: int = 120) -> str:
        text = str(text).strip()
        return text if len(text) <= limit else text[:limit - 3].rstrip() + "..."

    def _ms_to_time(self, ms: int) -> str:
        seconds = max(0, int(ms / 1000))
        return f"{seconds // 60:02d}:{seconds % 60:02d}"

    def _clean_text(self, text: str) -> str:
        return re.sub(r"\s+", " ", str(text)).replace("\n", " ").strip()

    def _parse_lrc_timestamp(self, timestamp: str) -> int:
        match = re.match(r"(\d+):(\d+)(?:\.(\d+))?", timestamp)
        if not match:
            return 0
        minutes = int(match.group(1))
        seconds = int(match.group(2))
        fraction = match.group(3) or "0"
        milliseconds = int(fraction.ljust(3, "0")[:3])
        return minutes * 60 * 1000 + seconds * 1000 + milliseconds

    def _parse_lrc(self, lrc_text: str) -> List[Tuple[int, str]]:
        lines = []
        for raw_line in lrc_text.splitlines():
            timestamps = re.findall(r"\[(\d+:\d+(?:\.\d+)?)\]", raw_line)
            lyric = re.sub(r"\[\d+:\d+(?:\.\d+)?\]", "", raw_line).strip()
            if not timestamps or not lyric:
                continue
            lyric = self._clean_text(lyric)
            for timestamp in timestamps:
                lines.append((self._parse_lrc_timestamp(timestamp), lyric))
        lines.sort(key=lambda item: item[0])
        return lines

    def _get_lyrics(self, song_name: str, artist_name: str) -> List[Tuple[int, str]]:
        if syncedlyrics is None:
            return []

        key = f"{artist_name} - {song_name}".lower()
        if key in self.lyrics_cache:
            return self.lyrics_cache[key]

        try:
            result = syncedlyrics.search(f"{song_name} {artist_name}", enhanced=True)
            if not result:
                self.lyrics_cache[key] = []
                return []
            parsed = self._parse_lrc(result)
            self.lyrics_cache[key] = parsed
            return parsed
        except Exception:
            self.lyrics_cache[key] = []
            return []

    def _current_lyric(self, lyrics: List[Tuple[int, str]], progress_ms: int) -> Optional[str]:
        current = None
        for timestamp, line in lyrics:
            if timestamp <= progress_ms:
                current = line
            else:
                break
        return current

    def _connect_spotify(self):
        spotify_cfg = self.config.get("spotify", {})
        if not spotify_cfg.get("enabled", False):
            return None

        if spotipy is None or SpotifyOAuth is None:
            return None

        cid = str(spotify_cfg.get("client_id", "")).strip()
        secret = str(spotify_cfg.get("client_secret", "")).strip()
        redirect = str(spotify_cfg.get("redirect_uri", "http://127.0.0.1:8888/callback")).strip()

        if not cid or not secret or "YOUR_" in cid or "YOUR_" in secret:
            return None

        try:
            auth = SpotifyOAuth(
                client_id=cid,
                client_secret=secret,
                redirect_uri=redirect,
                scope="user-read-currently-playing user-read-playback-state",
                cache_path=".spotify_cache"
            )
            return spotipy.Spotify(auth_manager=auth)
        except Exception:
            return None

    def _get_current_track(self) -> Optional[Dict[str, Any]]:
        if self.spotify is None:
            return None

        try:
            playback = self.spotify.current_playback()
            if not playback:
                return None

            item = playback.get("item")
            if not item or item.get("type") != "track":
                return None

            if not playback.get("is_playing", False):
                return None

            song = item.get("name", "Unknown Song")
            artists = item.get("artists", [])
            artist = ", ".join(a.get("name", "Unknown Artist") for a in artists)

            return {
                "song_name": song,
                "artist_name": artist,
                "progress_ms": playback.get("progress_ms") or 0,
                "duration_ms": item.get("duration_ms") or 0
            }
        except Exception:
            return None

    def _spotify_payload(self, track: Dict[str, Any]) -> Dict[str, Any]:
        spotify_cfg = self.config.get("spotify", {})
        show_lyrics = bool(spotify_cfg.get("show_lyrics", True))

        lyric = None
        if show_lyrics:
            lyrics = self._get_lyrics(track["song_name"], track["artist_name"])
            lyric = self._current_lyric(lyrics, track["progress_ms"])

        details = f"{track['song_name']} - {track['artist_name']}"
        if lyric:
            state = f"♪ {lyric}"
        else:
            state = f"{self._ms_to_time(track['progress_ms'])} / {self._ms_to_time(track['duration_ms'])}"

        payload = {
            "details": self._truncate(details),
            "state": self._truncate(state)
        }

        remaining = max(0, int((track["duration_ms"] - track["progress_ms"]) / 1000))
        payload["end"] = int(time.time()) + remaining
        return payload

    def _processes(self):
        names = set()
        for proc in psutil.process_iter(["name"]):
            try:
                if proc.info["name"]:
                    names.add(proc.info["name"].lower())
            except Exception:
                pass
        return names

    def _detect_app(self):
        running = self._processes()
        for app in self.config.get("apps", []):
            for p in app.get("processes", []):
                if p.lower() in running:
                    return app
        return None

    def _app_payload(self):
        app = self._detect_app()
        if app:
            return {
                "details": self._truncate(app.get("details", app.get("name", "App detected"))),
                "state": self._truncate(app.get("state", "Active")),
                "start": int(time.time())
            }

        idle = self.config.get("idle", {})
        return {
            "details": self._truncate(idle.get("details", "ZEN ULTIMATE MENU")),
            "state": self._truncate(idle.get("state", "System online")),
            "start": int(time.time())
        }

    def _loop(self):
        interval = int(self.config.get("update_interval", 8))
        min_interval = int(self.config.get("min_update_interval", 5))
        spotify_priority = bool(self.config.get("spotify_priority", True))

        while self.running:
            try:
                payload = None

                if spotify_priority and self.spotify is not None:
                    track = self._get_current_track()
                    if track:
                        payload = self._spotify_payload(track)

                if payload is None:
                    payload = self._app_payload()

                now = time.time()
                if payload != self.last_payload and now - self.last_update >= min_interval:
                    self.rpc.update(**payload)
                    self.last_payload = payload
                    self.last_update = now
            except Exception:
                pass

            time.sleep(interval)

    def start(self):
        if self.running:
            return

        client_id = str(self.config.get("client_id", "")).strip()
        if not client_id or "YOUR_" in client_id:
            raise ValueError("Set discord.client_id in config.json first.")

        self.rpc = Presence(client_id)
        self.rpc.connect()

        self.spotify = self._connect_spotify()

        self.running = True
        self.thread = threading.Thread(target=self._loop, daemon=True)
        self.thread.start()

    def stop(self):
        self.running = False
        try:
            if self.rpc:
                self.rpc.clear()
                self.rpc.close()
        except Exception:
            pass
