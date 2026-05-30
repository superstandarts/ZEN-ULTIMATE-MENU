
import os
import psutil
import subprocess
from pathlib import Path

class ProcessManager:
    def list_processes(self):
        rows = []
        for proc in psutil.process_iter(["pid", "name", "memory_info", "cpu_percent", "exe", "status", "username"]):
            try:
                info = proc.info
                mem = (info.get("memory_info").rss / 1024 / 1024) if info.get("memory_info") else 0
                rows.append({
                    "pid": info.get("pid"),
                    "name": info.get("name") or "",
                    "memory_mb": mem,
                    "cpu": info.get("cpu_percent") or 0,
                    "exe": info.get("exe") or "",
                    "status": info.get("status") or "",
                    "username": info.get("username") or ""
                })
            except Exception:
                continue
        rows.sort(key=lambda x: x["memory_mb"], reverse=True)
        return rows

    def terminate(self, pid, force=False):
        proc = psutil.Process(int(pid))
        if force:
            proc.kill()
        else:
            proc.terminate()

    def open_location(self, pid):
        exe = psutil.Process(int(pid)).exe()
        if exe:
            subprocess.Popen(f'explorer /select,"{exe}"', shell=True)
            return exe
        return None
