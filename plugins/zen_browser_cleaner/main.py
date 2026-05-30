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

BROWSERS = {
    "Chrome": r"%LOCALAPPDATA%\Google\Chrome\User Data\Default\Cache",
    "Edge": r"%LOCALAPPDATA%\Microsoft\Edge\User Data\Default\Cache",
    "Opera GX": r"%APPDATA%\Opera Software\Opera GX Stable\Cache",
    "Opera": r"%APPDATA%\Opera Software\Opera Stable\Cache",
}

def clean(path):
    p = Path(os.path.expandvars(path))
    count = 0
    if p.exists():
        for item in p.iterdir():
            try:
                if item.is_dir():
                    shutil.rmtree(item, ignore_errors=True)
                else:
                    item.unlink(missing_ok=True)
                count += 1
            except Exception:
                pass
    return count

def main():
    if tk is None:
        print("Tkinter unavailable.")
        return
    root = tk.Tk()
    root.title("ZEN Browser Cleaner")
    root.geometry("460x320")
    tk.Label(root, text="Close browsers before cleaning.").pack(pady=10)
    for name, path in BROWSERS.items():
        tk.Button(root, text=f"Clean {name} Cache", command=lambda n=name,p=path: messagebox.showinfo(n, f"Removed items: {clean(p)}")).pack(fill="x", padx=20, pady=5)
    root.mainloop()

if __name__ == "__main__":
    main()
