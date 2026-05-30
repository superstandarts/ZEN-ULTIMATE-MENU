
import customtkinter as ctk
import psutil
import time

class FloatingWidget:
    def __init__(self, parent):
        self.parent = parent
        self.window = None

    def show(self):
        if self.window and self.window.winfo_exists():
            self.window.lift()
            return
        self.window = ctk.CTkToplevel(self.parent)
        self.window.title("ZEN Widget")
        self.window.geometry("260x170+40+40")
        self.window.attributes("-topmost", True)
        self.window.configure(fg_color="#08080a")
        frame = ctk.CTkFrame(self.window, fg_color="#15161b", corner_radius=22, border_width=1, border_color="#34343a")
        frame.pack(fill="both", expand=True, padx=10, pady=10)
        self.label = ctk.CTkLabel(frame, text="ZEN Widget", font=("Segoe UI Variable", 17, "bold"), justify="left")
        self.label.pack(anchor="w", padx=16, pady=14)
        self.update()

    def update(self):
        if not self.window or not self.window.winfo_exists():
            return
        text = f"ZEN Widget\nCPU: {psutil.cpu_percent()}%\nRAM: {psutil.virtual_memory().percent}%\n{time.strftime('%H:%M:%S')}"
        self.label.configure(text=text)
        self.window.after(1000, self.update)
