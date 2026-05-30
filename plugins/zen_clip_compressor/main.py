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
    src = filedialog.askopenfilename(title="Choose video", filetypes=[("Videos", "*.mp4;*.mov;*.mkv;*.avi")])
    if not src:
        return
    dst = filedialog.asksaveasfilename(defaultextension=".mp4", initialfile="compressed.mp4")
    if not dst:
        return
    cmd = ["ffmpeg", "-y", "-i", src, "-vcodec", "libx264", "-crf", "28", "-preset", "medium", "-acodec", "aac", "-b:a", "128k", dst]
    subprocess.run(cmd)
    messagebox.showinfo("ZEN Clip Compressor", f"Saved:\n{dst}")

if __name__ == "__main__":
    main()
