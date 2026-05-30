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

import psutil

def close_processes(names):
    closed = 0
    for p in psutil.process_iter(["name"]):
        try:
            if p.info["name"] in names:
                p.terminate()
                closed += 1
        except Exception:
            pass
    return closed

def open_path(path):
    path = Path(os.path.expandvars(path))
    path.mkdir(parents=True, exist_ok=True)
    os.startfile(path)

def clear_folder(path):
    path = Path(os.path.expandvars(path))
    count = 0
    if path.exists():
        for item in path.iterdir():
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
    root.title("ZEN Roblox Tools")
    root.geometry("420x260")
    tk.Button(root, text="Open Roblox Logs", command=lambda: open_path(r"%LOCALAPPDATA%\Roblox\logs")).pack(fill="x", padx=20, pady=6)
    tk.Button(root, text="Open Roblox Folder", command=lambda: open_path(r"%LOCALAPPDATA%\Roblox")).pack(fill="x", padx=20, pady=6)
    tk.Button(root, text="Clear Roblox Logs", command=lambda: messagebox.showinfo("Done", f"Removed items: {clear_folder(r'%LOCALAPPDATA%\Roblox\logs')}")).pack(fill="x", padx=20, pady=6)
    tk.Button(root, text="Close Roblox", command=lambda: messagebox.showinfo("Done", f"Closed processes: {close_processes(['RobloxPlayerBeta.exe', 'RobloxStudioBeta.exe'])}")).pack(fill="x", padx=20, pady=6)
    root.mainloop()

if __name__ == "__main__":
    main()
