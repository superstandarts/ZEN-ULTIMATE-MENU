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
    if shutil.which("ffmpeg") is None:
        messagebox.showerror("FFmpeg", "FFmpeg not found in PATH.")
        return
    root = tk.Tk()
    root.withdraw()
    src = filedialog.askopenfilename(title="Choose audio", filetypes=[("Audio", "*.mp3;*.wav;*.ogg;*.flac;*.m4a")])
    if not src:
        return
    dst = filedialog.asksaveasfilename(defaultextension=".wav", initialfile="converted.wav")
    if not dst:
        return
    subprocess.run(["ffmpeg", "-y", "-i", src, dst])
    messagebox.showinfo("ZEN Audio Converter", f"Saved:\n{dst}")

if __name__ == "__main__":
    main()
