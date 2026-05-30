
import re
import time
from typing import List, Tuple, Optional


class MusicWidget:
    def __init__(self, config):
        self.config = config
        self.spotify = None
        self.lyrics_cache = {}
        self.last_track_key = None

    def connect(self):
        try:
            import spotipy
            from spotipy.oauth2 import SpotifyOAuth

            spotify_cfg = self.config.get("discord", {}).get("spotify", {})
            if not spotify_cfg.get("enabled"):
                return False

            auth = SpotifyOAuth(
                client_id=spotify_cfg.get("client_id"),
                client_secret=spotify_cfg.get("client_secret"),
                redirect_uri=spotify_cfg.get("redirect_uri", "http://127.0.0.1:8888/callback"),
                scope="user-read-currently-playing user-read-playback-state",
                cache_path=".spotify_cache"
            )
            self.spotify = spotipy.Spotify(auth_manager=auth)
            return True
        except Exception:
            return False

    def current_track(self):
        if self.spotify is None and not self.connect():
            return None, "Spotify not connected."

        try:
            pb = self.spotify.current_playback()
            if not pb or not pb.get("item"):
                return None, "No song playing."

            item = pb["item"]
            artists = ", ".join(a["name"] for a in item.get("artists", []))
            track = {
                "name": item.get("name", "Unknown Song"),
                "artists": artists,
                "progress_ms": pb.get("progress_ms") or 0,
                "duration_ms": item.get("duration_ms") or 0,
                "is_playing": pb.get("is_playing", False),
                "url": item.get("external_urls", {}).get("spotify", "")
            }
            return track, None
        except Exception as e:
            return None, f"Spotify error: {e}"

    def _parse_ts(self, ts):
        m = re.match(r"(\d+):(\d+)(?:\.(\d+))?", ts)
        if not m:
            return 0
        minutes = int(m.group(1))
        seconds = int(m.group(2))
        frac = (m.group(3) or "0").ljust(3, "0")[:3]
        return minutes * 60000 + seconds * 1000 + int(frac)

    def _parse_lrc(self, text) -> List[Tuple[int, str]]:
        rows = []
        for line in text.splitlines():
            stamps = re.findall(r"\[(\d+:\d+(?:\.\d+)?)\]", line)
            lyric = re.sub(r"\[\d+:\d+(?:\.\d+)?\]", "", line).strip()
            if not stamps or not lyric:
                continue
            for stamp in stamps:
                rows.append((self._parse_ts(stamp), lyric))
        rows.sort(key=lambda x: x[0])
        return rows

    def lyrics_for(self, name, artists):
        key = f"{artists} - {name}".lower()
        if key in self.lyrics_cache:
            return self.lyrics_cache[key]

        try:
            import syncedlyrics
            raw = syncedlyrics.search(f"{name} {artists}", enhanced=True)
            if not raw:
                self.lyrics_cache[key] = []
            else:
                self.lyrics_cache[key] = self._parse_lrc(raw)
        except Exception:
            self.lyrics_cache[key] = []

        return self.lyrics_cache[key]

    def _time(self, ms):
        s = int(ms / 1000)
        return f"{s//60:02d}:{s%60:02d}"

    def current_with_lyrics(self, window=8):
        track, error = self.current_track()
        if error:
            return error, None

        lyrics = self.lyrics_for(track["name"], track["artists"])
        progress = track["progress_ms"]
        current_index = -1

        for i, (ts, _) in enumerate(lyrics):
            if ts <= progress:
                current_index = i
            else:
                break

        header = (
            f"{track['name']} - {track['artists']}\n"
            f"{self._time(track['progress_ms'])} / {self._time(track['duration_ms'])}"
            f"{'  •  PLAYING' if track['is_playing'] else '  •  PAUSED'}\n"
            + "-" * 70 + "\n"
        )

        if not lyrics:
            return header + "No synced lyrics found for this song.", track

        start = max(0, current_index - window)
        end = min(len(lyrics), current_index + window + 1)

        lines = [header]
        for i in range(start, end):
            ts, line = lyrics[i]
            stamp = self._time(ts)
            if i == current_index:
                lines.append(f">>> {stamp}  {line}  <<<")
            else:
                lines.append(f"    {stamp}  {line}")

        return "\n".join(lines), track

    def current(self):
        text, _ = self.current_with_lyrics()
        return text
