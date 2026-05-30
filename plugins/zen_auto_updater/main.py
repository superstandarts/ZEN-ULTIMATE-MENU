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

def backup_current():
    app_dir = Path(__file__).resolve().parents[2]
    backups = app_dir / "update_backups"
    backups.mkdir(exist_ok=True)
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    dst = backups / f"zen_backup_{stamp}"
    shutil.copytree(app_dir, dst, ignore=shutil.ignore_patterns("update_backups", "__pycache__", "*.pyc"))
    return dst

def main():
    if tk is None:
        print("Tkinter unavailable.")
        return
    root = tk.Tk()
    root.withdraw()
    if messagebox.askyesno("ZEN Auto Updater", "Create a backup of current app folder?"):
        dst = backup_current()
        messagebox.showinfo("ZEN Auto Updater", f"Backup created:\n{dst}\n\nFuture version can download releases from GitHub.")

if __name__ == "__main__":
    main()
