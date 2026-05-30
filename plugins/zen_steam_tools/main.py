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

def find_steam():
    candidates = [
        Path(os.environ.get("PROGRAMFILES(X86)", "")) / "Steam",
        Path(os.environ.get("PROGRAMFILES", "")) / "Steam",
        Path("C:/Program Files (x86)/Steam"),
    ]
    for c in candidates:
        if c.exists():
            return c
    return None

def open_folder(path):
    if path and Path(path).exists():
        os.startfile(path)
    else:
        messagebox.showwarning("Steam", "Folder not found.")

def clear_web_cache(steam):
    count = 0
    if steam:
        for rel in ["config/htmlcache", "appcache/httpcache"]:
            p = steam / rel
            if p.exists():
                shutil.rmtree(p, ignore_errors=True)
                count += 1
    return count

def main():
    if tk is None:
        print("Tkinter unavailable.")
        return
    steam = find_steam()
    root = tk.Tk()
    root.title("ZEN Steam Tools")
    root.geometry("440x260")
    tk.Label(root, text=f"Steam folder: {steam or 'Not found'}").pack(padx=12, pady=8)
    tk.Button(root, text="Open Steam Folder", command=lambda: open_folder(steam)).pack(fill="x", padx=20, pady=6)
    tk.Button(root, text="Open Screenshots Folder", command=lambda: open_folder(steam / "userdata" if steam else None)).pack(fill="x", padx=20, pady=6)
    tk.Button(root, text="Clear Steam Web Cache", command=lambda: messagebox.showinfo("Steam", f"Cache folders removed: {clear_web_cache(steam)}")).pack(fill="x", padx=20, pady=6)
    tk.Button(root, text="Open Steam", command=lambda: subprocess.Popen("steam", shell=True)).pack(fill="x", padx=20, pady=6)
    root.mainloop()

if __name__ == "__main__":
    main()
