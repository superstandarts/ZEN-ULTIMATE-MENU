import customtkinter as ctk

class NotesOverlay(ctk.CTkToplevel):
    def __init__(self, text):
        super().__init__()
        self.title("ZEN Notes")
        self.geometry("330x300+60+60")
        self.attributes("-topmost", True)
        self.configure(fg_color="#09090d")

        label = ctk.CTkLabel(self, text="CRX NOTES", text_color="#ff003c", font=("Consolas", 20, "bold"))
        label.pack(padx=12, pady=(12, 4), anchor="w")

        box = ctk.CTkTextbox(self, fg_color="#11111a", text_color="#f1f1f1", font=("Consolas", 13))
        box.pack(fill="both", expand=True, padx=12, pady=12)
        box.insert("end", text)
