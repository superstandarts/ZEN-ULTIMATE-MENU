
class Notifier:
    def __init__(self, app_name="ZEN ULTIMATE MENU"):
        self.app_name = app_name

    def notify(self, title, message):
        try:
            from winotify import Notification
            toast = Notification(app_id=self.app_name, title=title, msg=message)
            toast.show()
            return True
        except Exception:
            return False
