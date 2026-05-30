
import subprocess, os
from pathlib import Path

class GitHubTools:
    def run_git(self, folder, args):
        result = subprocess.run(["git"] + args, cwd=folder, capture_output=True, text=True, shell=False)
        return result.stdout + result.stderr

    def init_repo(self, folder):
        return self.run_git(folder, ["init"])

    def status(self, folder):
        return self.run_git(folder, ["status"])

    def add_all(self, folder):
        return self.run_git(folder, ["add", "."])

    def commit(self, folder, message):
        return self.run_git(folder, ["commit", "-m", message])

    def push(self, folder):
        return self.run_git(folder, ["push"])

    def create_gitignore(self, folder, language="python"):
        content = "__pycache__/\n*.pyc\n.venv/\ndist/\nbuild/\n*.spec\n.env\n"
        Path(folder, ".gitignore").write_text(content, encoding="utf-8")
        return "Created .gitignore"
