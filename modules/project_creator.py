
from pathlib import Path
import json

class ProjectCreator:
    def create(self, base_folder, name, template="Python GUI", author="superstandarts"):
        root = Path(base_folder) / name
        root.mkdir(parents=True, exist_ok=True)
        (root/"assets").mkdir(exist_ok=True)
        (root/"src").mkdir(exist_ok=True)

        if template == "HTML/CSS/JS":
            (root/"index.html").write_text("<!DOCTYPE html><html><head><title>"+name+"</title><link rel='stylesheet' href='style.css'></head><body><h1>"+name+"</h1><script src='script.js'></script></body></html>", encoding="utf-8")
            (root/"style.css").write_text("body{font-family:Arial;background:#111;color:white;}", encoding="utf-8")
            (root/"script.js").write_text("console.log('"+name+"');", encoding="utf-8")
        else:
            (root/"main.py").write_text("print('"+name+"')\n", encoding="utf-8")
            (root/"requirements.txt").write_text("", encoding="utf-8")

        (root/"README.md").write_text(f"# {name}\n\nMade by {author}.\n", encoding="utf-8")
        (root/".gitignore").write_text("__pycache__/\n.venv/\ndist/\nbuild/\n*.spec\n", encoding="utf-8")
        (root/"LICENSE").write_text("MIT License\n", encoding="utf-8")
        return str(root)
