<div align="center">

# 🔴 ZEN ULTIMATE MENU

### Windows QOL toolbox with cleanup, automation, gaming tools, Discord status and creator utilities.

![Python](https://img.shields.io/badge/Python-3.10+-red?style=for-the-badge&logo=python&logoColor=white)
![Platform](https://img.shields.io/badge/platform-Windows-black?style=for-the-badge&logo=windows&logoColor=white)
![Status](https://img.shields.io/badge/status-active-red?style=for-the-badge)

</div>

---

## About

**ZEN ULTIMATE MENU** is a desktop toolbox made for Windows.  
It combines multiple QOL tools in one red/black interface.

## Included modules

- Junk cleaner
- Screenshot organizer
- Smart file search
- Discord auto status
- Spotify currently-playing sync for Discord status
- Synced lyrics if available, timer fallback if not
- Hotkeys
- Text expander
- Safe auto clicker
- App volume list
- Game session manager
- README generator
- Desktop notes overlay
- Credits/contact page

## Contact

- Discord: `7mey`
- GitHub: https://github.com/superstandarts
- Instagram: https://www.instagram.com/xyphanctinusultrazaliextremus/
- Steam: https://steamcommunity.com/id/hokurary
- Roblox: https://www.roblox.com/users/5583806069/profile

## Discord + Spotify setup

In `config.json`, set:

```json
"discord": {
  "client_id": "YOUR_DISCORD_APPLICATION_ID",
  "spotify": {
    "enabled": true,
    "client_id": "YOUR_SPOTIFY_CLIENT_ID",
    "client_secret": "YOUR_SPOTIFY_CLIENT_SECRET",
    "redirect_uri": "http://127.0.0.1:8888/callback"
  }
}
```

If Spotify is playing, the Discord status shows the current song and synced lyrics.  
If no lyrics are found, it shows the music timer.  
If Spotify is not playing, the app detector takes over.

## Run

```bash
pip install -r requirements.txt
python main.py
```

## Manual EXE build

```bash
python -m pip install pyinstaller
python -m PyInstaller --noconfirm --clean --onefile --windowed --name "ZEN ULTIMATE MENU" --add-data "config.json;." --add-data "modules;modules" main.py
```

The output will be inside:

```txt
dist/ZEN ULTIMATE MENU.exe
```
