
import psutil, time

class PerformanceMonitor:
    def snapshot(self):
        boot = psutil.boot_time()
        uptime = int(time.time() - boot)
        return {
            "cpu": psutil.cpu_percent(),
            "ram": psutil.virtual_memory().percent,
            "disk": psutil.disk_usage("/").percent,
            "battery": psutil.sensors_battery().percent if psutil.sensors_battery() else None,
            "uptime_seconds": uptime
        }

    def top_processes(self, limit=5):
        rows = []
        for p in psutil.process_iter(["pid","name","memory_info","cpu_percent"]):
            try:
                mem = p.info["memory_info"].rss / 1024 / 1024 if p.info.get("memory_info") else 0
                rows.append((p.info["name"], p.info["pid"], mem, p.info.get("cpu_percent") or 0))
            except Exception:
                pass
        rows.sort(key=lambda x: x[2], reverse=True)
        return rows[:limit]
