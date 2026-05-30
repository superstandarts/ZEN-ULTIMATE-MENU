
import subprocess, sys
from pathlib import Path

class DependencyDoctor:
    def run(self, args, cwd=None):
        result = subprocess.run(args, cwd=cwd, capture_output=True, text=True, shell=False)
        return result.stdout + result.stderr

    def upgrade_pip(self):
        return self.run([sys.executable, "-m", "pip", "install", "--upgrade", "pip", "setuptools", "wheel"])

    def install_requirements(self, app_dir):
        req = Path(app_dir) / "requirements.txt"
        if not req.exists():
            return "requirements.txt not found."
        return self.run([sys.executable, "-m", "pip", "install", "-r", str(req)])

    def pip_check(self):
        return self.run([sys.executable, "-m", "pip", "check"])

    def pip_list(self):
        return self.run([sys.executable, "-m", "pip", "list"])

    def clear_cache(self):
        return self.run([sys.executable, "-m", "pip", "cache", "purge"])

    def export_requirements(self, app_dir):
        out = self.run([sys.executable, "-m", "pip", "freeze"])
        path = Path(app_dir) / "requirements_exported.txt"
        path.write_text(out, encoding="utf-8")
        return f"Exported to {path}\n\n{out}"
