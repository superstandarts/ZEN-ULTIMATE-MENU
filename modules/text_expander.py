import time
import threading
import keyboard
import pyperclip

class TextExpander:
    def __init__(self, config, logger=print):
        self.map = config.get("text_expander", {})
        self.logger = logger
        self.running = False
        self.thread = None
        self.buffer = ""

    def _loop(self):
        while self.running:
            event = keyboard.read_event()
            if not self.running:
                break
            if event.event_type != keyboard.KEY_DOWN:
                continue
            name = event.name
            if len(name) == 1:
                self.buffer += name
                self.buffer = self.buffer[-30:]
                for trigger, text in self.map.items():
                    if self.buffer.endswith(trigger):
                        keyboard.write("\b" * len(trigger))
                        pyperclip.copy(text)
                        keyboard.press_and_release("ctrl+v")
                        self.logger(f"Expanded {trigger}")
                        self.buffer = ""
            elif name == "space":
                self.buffer += " "
            elif name == "backspace":
                self.buffer = self.buffer[:-1]
            elif name == "enter":
                self.buffer = ""

    def start(self):
        if self.running:
            return
        self.running = True
        self.thread = threading.Thread(target=self._loop, daemon=True)
        self.thread.start()

    def stop(self):
        self.running = False
        keyboard.press_and_release("esc")
