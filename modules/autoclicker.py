import time
import threading
import pyautogui

class AutoClicker:
    def __init__(self, logger=print):
        self.logger = logger
        self.running = False
        pyautogui.FAILSAFE = True

    def start(self, interval=0.1, max_clicks=500):
        if self.running:
            return
        self.running = True

        def loop():
            clicks = 0
            self.logger("AutoClicker started. Failsafe: move mouse to top-left corner.")
            while self.running and clicks < max_clicks:
                try:
                    pyautogui.click()
                    clicks += 1
                    time.sleep(max(0.03, interval))
                except pyautogui.FailSafeException:
                    self.running = False
                    self.logger("AutoClicker stopped by failsafe.")
                    break
            self.running = False
            self.logger(f"AutoClicker finished. Clicks: {clicks}")

        threading.Thread(target=loop, daemon=True).start()

    def stop(self):
        self.running = False
        self.logger("AutoClicker stopped.")
