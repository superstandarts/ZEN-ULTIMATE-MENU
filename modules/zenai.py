
import json
import urllib.request
import urllib.error
from pathlib import Path


class ZENAI:
    def __init__(self, config_path):
        self.config_path = Path(config_path)

    def _load_config(self):
        try:
            return json.loads(self.config_path.read_text(encoding="utf-8"))
        except Exception:
            return {}

    def _ask_ollama(self, message, cfg):
        zenai_cfg = cfg.get("zenai", {})
        model = zenai_cfg.get("model", "llama3.1")
        url = zenai_cfg.get("ollama_url", "http://127.0.0.1:11434/api/generate")

        system_prompt = zenai_cfg.get(
            "system_prompt",
            "You are ZENAI, the assistant inside ZEN ULTIMATE MENU. Help with Windows tools, config, errors and automation."
        )

        context = (
            "You are running locally through Ollama. "
            "Answer in the user's language. "
            "Be practical and concise. "
            "Never ask to run destructive commands without confirmation. "
            "The app name is ZEN ULTIMATE MENU."
        )

        payload = {
            "model": model,
            "prompt": f"{system_prompt}\n\n{context}\n\nUser: {message}\nZENAI:",
            "stream": False
        }

        data = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(url, data=data, headers={"Content-Type": "application/json"}, method="POST")

        with urllib.request.urlopen(req, timeout=60) as response:
            raw = response.read().decode("utf-8", errors="replace")
            parsed = json.loads(raw)
            return parsed.get("response", "").strip() or "ZENAI did not return a response."

    def _offline_answer(self, message):
        msg = message.lower().strip()

        if not msg:
            return "Ask me something about ZEN ULTIMATE MENU."

        if "erro" in msg or "error" in msg:
            return (
                "ZENAI local fallback:\n"
                "1. Run the app with python main.py to see the real traceback.\n"
                "2. Check if config.json and assets are next to the .exe.\n"
                "3. If it is a PyInstaller issue, rebuild with --clean.\n"
                "4. If a module is missing, run install_requirements.bat."
            )

        if "ollama" in msg or "local" in msg or "ia" in msg or "ai" in msg:
            return (
                "ZENAI can run as a real local AI using Ollama.\n\n"
                "Setup:\n"
                "1. Install Ollama.\n"
                "2. Run: ollama pull llama3.1\n"
                "3. In config.json set zenai.provider to ollama and zenai.enabled to true.\n"
                "4. Keep model as llama3.1 or change it to another installed model.\n\n"
                "If Ollama is not open, I use this offline fallback."
            )

        if "config" in msg:
            return (
                "ZENAI config help:\n"
                "Open Settings > Config Editor. You can edit Discord, Spotify, hotkeys, text expander, profiles and theme there.\n"
                "Always save valid JSON."
            )

        if "spotify" in msg:
            return (
                "ZENAI Spotify help:\n"
                "Make sure discord.spotify.enabled is true, client_id/client_secret are set, and redirect_uri is exactly http://127.0.0.1:8888/callback."
            )

        if "discord" in msg:
            return (
                "ZENAI Discord help:\n"
                "Make sure Discord desktop is open and discord.client_id is your Discord Application ID."
            )

        if "senha" in msg or "password" in msg:
            return "Use the Passwords tab to generate strong passwords and copy them safely."

        if "profile" in msg or "mode" in msg:
            return "Use Profiles to create Gaming, Coding or Study modes. Profiles can open apps, close apps and open folders."

        if "clean" in msg or "limpar" in msg:
            return "Use Cleaner for temp files and Privacy for clipboard, recent files and Run history."

        return (
            "ZENAI is currently using local fallback mode.\n"
            "For real local AI, install Ollama and set zenai.provider to ollama in config.json.\n"
            "I can help with errors, config, Spotify, Discord, profiles, cleaning and passwords."
        )

    def ask(self, message):
        cfg = self._load_config()
        zenai_cfg = cfg.get("zenai", {})

        provider = str(zenai_cfg.get("provider", "offline_rules")).lower()
        enabled = bool(zenai_cfg.get("enabled", True))

        if enabled and provider == "ollama":
            try:
                return self._ask_ollama(message, cfg)
            except urllib.error.URLError:
                return (
                    "ZENAI tried to connect to Ollama, but it is not running.\n\n"
                    "Fix:\n"
                    "1. Install/open Ollama.\n"
                    "2. Run: ollama pull llama3.1\n"
                    "3. Start this app again.\n\n"
                    "Fallback answer:\n\n" + self._offline_answer(message)
                )
            except Exception as error:
                return (
                    f"ZENAI Ollama error: {error}\n\n"
                    "Fallback answer:\n\n" + self._offline_answer(message)
                )

        return self._offline_answer(message)
