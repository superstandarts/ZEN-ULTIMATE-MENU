import os
import sys
import json
import shutil
import subprocess
import webbrowser
from pathlib import Path
from datetime import datetime

try:
    import tkinter as tk
    from tkinter import filedialog, messagebox, simpledialog
except Exception:
    tk = None

APP_DIR = Path(__file__).resolve().parent

def main():
    if tk is None:
        print("Tkinter unavailable.")
        return
    root = tk.Tk()
    root.withdraw()
    app_dir = Path(__file__).resolve().parents[2]
    sound_dir = app_dir / "assets" / "sounds"
    sound_dir.mkdir(parents=True, exist_ok=True)
    src = filedialog.askopenfilename(title="Choose startup sound", filetypes=[("Audio", "*.wav;*.mp3")])
    if not src:
        return
    ext = Path(src).suffix.lower()
    dst = sound_dir / f"startup{ext}"
    shutil.copy2(src, dst)
    messagebox.showinfo("ZEN Sound Pack", f"Installed:\n{dst}\nRestart app to use it.")

if __name__ == "__main__":
    main()
