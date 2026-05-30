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

from PIL import Image, ImageDraw

def create_banner(text, dst, w=1800, h=600):
    img = Image.new("RGB", (w, h), "#050507")
    d = ImageDraw.Draw(img)
    d.rounded_rectangle((30, 30, w-30, h-30), radius=40, fill="#101115", outline="#34343a", width=3)
    d.line((0, h//2, w, h//2), fill="#20222a", width=2)
    d.text((w//2 - len(text)*12, h//2 - 28), text, fill="#f4f4f4")
    d.text((w//2 - 150, h//2 + 35), "ULTIMATE MENU", fill="#bdbdc4")
    img.save(dst)

def main():
    if tk is None:
        print("Tkinter unavailable.")
        return
    root = tk.Tk()
    root.withdraw()
    text = simpledialog.askstring("Banner", "Main text:", initialvalue="ZEN")
    dst = filedialog.asksaveasfilename(defaultextension=".png", initialfile="zen_banner.png")
    if dst:
        create_banner(text or "ZEN", dst)
        messagebox.showinfo("ZEN Banner Maker", f"Created:\n{dst}")

if __name__ == "__main__":
    main()
