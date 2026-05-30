
import threading

class TrayManager:
    def __init__(self, app, icon_path=None):
        self.app = app
        self.icon_path = icon_path
        self.icon = None
        self.thread = None

    def start(self):
        try:
            import pystray
            from PIL import Image

            def show():
                self.app.after(0, self.app.deiconify)

            def quit_app():
                self.app.after(0, self.app.destroy)
                if self.icon:
                    self.icon.stop()

            image = Image.new("RGB", (64, 64), "black")
            menu = pystray.Menu(
                pystray.MenuItem("Open ZEN", lambda: show()),
                pystray.MenuItem("Exit", lambda: quit_app())
            )
            self.icon = pystray.Icon("ZEN ULTIMATE MENU", image, "ZEN ULTIMATE MENU", menu)
            self.thread = threading.Thread(target=self.icon.run, daemon=True)
            self.thread.start()
            return True
        except Exception:
            return False
