
import subprocess, sys, os
from pathlib import Path

class MiniTerminal:
    def run_cmd(self, command, cwd=None):
        if not command.strip():
            return ""
        result = subprocess.run(command, cwd=cwd or None, shell=True, capture_output=True, text=True)
        return result.stdout + result.stderr

    def run_python(self, code, cwd=None):
        result = subprocess.run([sys.executable, "-c", code], cwd=cwd or None, capture_output=True, text=True)
        return result.stdout + result.stderr
