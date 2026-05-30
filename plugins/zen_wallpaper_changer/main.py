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

import ctypes

def set_wallpaper(path):
    SPI_SETDESKWALLPAPER = 20
    SPIF_UPDATEINIFILE = 1
    SPIF_SENDCHANGE = 2
    ctypes.windll.user32.SystemParametersInfoW(SPI_SETDESKWALLPAPER, 0, str(path), SPIF_UPDATEINIFILE | SPIF_SENDCHANGE)

def main():
    if tk is None:
        print("Tkinter unavailable.")
        return
    root = tk.Tk()
    root.withdraw()
    path = filedialog.askopenfilename(
        title="Choose wallpaper",
        filetypes=[("Images", "*.png;*.jpg;*.jpeg;*.bmp")]
    )
    if path:
        set_wallpaper(path)
        messagebox.showinfo("ZEN Wallpaper Changer", f"Wallpaper changed:\n{path}")
    root.destroy()

if __name__ == "__main__":
    main()
