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

HTML = """<!doctype html>
<html>
<head>
<meta charset="utf-8">
<title>{name}</title>
<style>
body{{margin:0;background:#070709;color:#fff;font-family:Segoe UI,Arial}}
main{{max-width:900px;margin:80px auto;padding:32px;background:#15161b;border:1px solid #333640;border-radius:24px}}
a{{color:#fff}}
.card{{padding:18px;border:1px solid #333640;border-radius:18px;margin:12px 0;background:#0f1014}}
</style>
</head>
<body>
<main>
<h1>{name}</h1>
<p>{bio}</p>
<h2>Links</h2>
<div class="card"><a href="{github}">GitHub</a></div>
<div class="card"><a href="{instagram}">Instagram</a></div>
</main>
</body>
</html>
"""

def main():
    if tk is None:
        print("Tkinter unavailable.")
        return
    root = tk.Tk()
    root.withdraw()
    name = simpledialog.askstring("Portfolio", "Name:", initialvalue="Zen")
    bio = simpledialog.askstring("Portfolio", "Bio:", initialvalue="Developer and creator.")
    github = simpledialog.askstring("Portfolio", "GitHub URL:", initialvalue="https://github.com/superstandarts")
    instagram = simpledialog.askstring("Portfolio", "Instagram URL:", initialvalue="")
    dst = filedialog.asksaveasfilename(defaultextension=".html", initialfile="portfolio.html")
    if dst:
        Path(dst).write_text(HTML.format(name=name, bio=bio, github=github, instagram=instagram), encoding="utf-8")
        messagebox.showinfo("Portfolio", f"Created:\n{dst}")

if __name__ == "__main__":
    main()
