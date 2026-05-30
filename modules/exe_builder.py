
import subprocess, shlex
from pathlib import Path

class ExeBuilder:
    def build_command(self, script, name, icon="", windowed=True, onefile=True):
        cmd = ["python", "-m", "PyInstaller", "--noconfirm", "--clean"]
        if onefile:
            cmd.append("--onefile")
        if windowed:
            cmd.append("--windowed")
        if name:
            cmd += ["--name", name]
        if icon:
            cmd += ["--icon", icon]
        cmd.append(script)
        return cmd

    def build(self, script, name, icon="", windowed=True, onefile=True):
        cmd = self.build_command(script, name, icon, windowed, onefile)
        result = subprocess.run(cmd, capture_output=True, text=True)
        return " ".join(shlex.quote(x) for x in cmd) + "\n\n" + result.stdout + result.stderr
