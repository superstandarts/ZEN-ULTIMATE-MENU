
import socket
import subprocess
import platform
import webbrowser

class InternetTools:
    def local_ip(self):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            ip = s.getsockname()[0]
            s.close()
            return ip
        except Exception:
            return "Unavailable"

    def hostname(self):
        return socket.gethostname()

    def ping(self, host="google.com"):
        count_flag = "-n" if platform.system().lower() == "windows" else "-c"
        result = subprocess.run(["ping", count_flag, "4", host], capture_output=True, text=True, shell=False)
        return result.stdout or result.stderr

    def flush_dns(self):
        result = subprocess.run(["ipconfig", "/flushdns"], capture_output=True, text=True, shell=True)
        return result.stdout or result.stderr

    def renew_ip(self):
        release = subprocess.run(["ipconfig", "/release"], capture_output=True, text=True, shell=True)
        renew = subprocess.run(["ipconfig", "/renew"], capture_output=True, text=True, shell=True)
        return (release.stdout or release.stderr) + "\n" + (renew.stdout or renew.stderr)

    def open_network_settings(self):
        webbrowser.open("ms-settings:network")
