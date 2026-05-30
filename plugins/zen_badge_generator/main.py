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

def make_badge(label, message, color, logo=""):
    logo_part = f"&logo={logo}" if logo else ""
    return f"![{label}](https://img.shields.io/badge/{label}-{message}-{color}?style=for-the-badge{logo_part})"

def main():
    if tk is None:
        print("Tkinter unavailable.")
        return
    root = tk.Tk()
    root.title("ZEN Badge Generator")
    root.geometry("650x380")
    entries = {}
    for name, default in [("Label","Python"),("Message","3.11"),("Color","white"),("Logo","python")]:
        tk.Label(root, text=name).pack(anchor="w", padx=16)
        e = tk.Entry(root)
        e.insert(0, default)
        e.pack(fill="x", padx=16, pady=3)
        entries[name] = e
    out = tk.Text(root, height=6)
    out.pack(fill="both", expand=True, padx=16, pady=10)
    def gen():
        md = make_badge(entries["Label"].get(), entries["Message"].get(), entries["Color"].get(), entries["Logo"].get())
        out.delete("1.0", "end")
        out.insert("end", md)
    tk.Button(root, text="Generate Badge", command=gen).pack(fill="x", padx=16, pady=6)
    root.mainloop()

if __name__ == "__main__":
    main()
