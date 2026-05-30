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

def run_cmd(cmd, cwd):
    result = subprocess.run(cmd, cwd=cwd, shell=True, capture_output=True, text=True)
    return result.stdout + result.stderr

def main():
    if tk is None:
        print("Tkinter unavailable.")
        return
    root = tk.Tk()
    root.withdraw()
    folder = filedialog.askdirectory(title="Choose project folder")
    if not folder:
        return
    commands = {
        "vercel --version": "vercel --version",
        "vercel login": "vercel login",
        "vercel dev": "vercel dev",
        "vercel deploy": "vercel",
        "vercel production": "vercel --prod",
    }
    win = tk.Tk()
    win.title("ZEN Vercel Helper")
    win.geometry("700x500")
    output = tk.Text(win)
    output.pack(fill="both", expand=True, padx=10, pady=10)
    for label, cmd in commands.items():
        tk.Button(win, text=label, command=lambda c=cmd: output.insert("end", f"> {c}\n{run_cmd(c, folder)}\n")).pack(fill="x", padx=10, pady=3)
    win.mainloop()

if __name__ == "__main__":
    main()
