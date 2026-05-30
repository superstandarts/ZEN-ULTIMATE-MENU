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

SECRET_WORDS = ["api_key", "client_secret", "token", "password", "private_key", "discord token"]

def scan(folder):
    folder = Path(folder)
    files = []
    total = 0
    secrets = []
    for p in folder.rglob("*"):
        try:
            if p.is_file():
                files.append(p)
                total += p.stat().st_size
                if p.suffix.lower() in [".py", ".js", ".ts", ".json", ".env", ".txt", ".md"]:
                    txt = p.read_text(encoding="utf-8", errors="ignore").lower()
                    if any(w in txt for w in SECRET_WORDS):
                        secrets.append(str(p))
        except Exception:
            pass
    return files, total, secrets

def main():
    if tk is None:
        print("Tkinter unavailable.")
        return
    root = tk.Tk()
    root.withdraw()
    folder = filedialog.askdirectory(title="Choose project")
    if not folder:
        return
    files, total, secrets = scan(folder)
    report = Path(folder) / "zen_project_scan.txt"
    report.write_text(
        f"Files: {len(files)}\nSize MB: {total/1024/1024:.2f}\nREADME: {(Path(folder)/'README.md').exists()}\n.gitignore: {(Path(folder)/'.gitignore').exists()}\n\nPossible secrets:\n" + "\n".join(secrets),
        encoding="utf-8"
    )
    messagebox.showinfo("ZEN Project Scanner", f"Report created:\n{report}")

if __name__ == "__main__":
    main()
