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

def copy_asset(kind):
    app_dir = Path(__file__).resolve().parents[2]
    paths = {
        "Logo": (app_dir / "assets" / "images" / "zen.png", "*.png"),
        "Icon": (app_dir / "assets" / "icons" / "app.ico", "*.ico"),
        "Banner": (app_dir / "assets" / "banners" / "zen_banner.png", "*.png"),
        "Startup Sound": (app_dir / "assets" / "sounds" / "startup.wav", "*.wav"),
    }
    dst, pattern = paths[kind]
    dst.parent.mkdir(parents=True, exist_ok=True)
    src = filedialog.askopenfilename(title=f"Choose {kind}", filetypes=[(kind, pattern)])
    if src:
        shutil.copy2(src, dst)
        messagebox.showinfo("ZEN Skin Manager", f"{kind} installed:\n{dst}")

def main():
    if tk is None:
        print("Tkinter unavailable.")
        return
    root = tk.Tk()
    root.title("ZEN App Skin Manager")
    root.geometry("420x260")
    for kind in ["Logo", "Icon", "Banner", "Startup Sound"]:
        tk.Button(root, text=f"Replace {kind}", command=lambda k=kind: copy_asset(k)).pack(fill="x", padx=20, pady=8)
    root.mainloop()

if __name__ == "__main__":
    main()
