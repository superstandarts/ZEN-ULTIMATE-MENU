import os
import sys
import json
import time
import shutil
import threading
import subprocess
import webbrowser
import math
import random
from pathlib import Path
from datetime import datetime
from tkinter import filedialog, messagebox

import customtkinter as ctk
import psutil
import pyperclip
from send2trash import send2trash

from modules.cleaner import Cleaner
from modules.screenshot_organizer import ScreenshotOrganizer
from modules.discord_status import DiscordStatus
from modules.hotkeys import HotkeyManager
from modules.text_expander import TextExpander
from modules.file_search import SmartFileSearch
from modules.readme_generator import generate_readme
from modules.volume_controller import VolumeController
from modules.autoclicker import AutoClicker
from modules.notes_overlay import NotesOverlay
from modules.game_session import GameSession


def get_app_dir():
    if getattr(sys, "frozen", False):
        return Path(sys.executable).resolve().parent
    return Path(__file__).resolve().parent


APP_DIR = get_app_dir()
CONFIG_PATH = APP_DIR / "config.json"


def load_config():
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


class ZenUltimateMenu(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.config_data = load_config()
        self.title("ZEN ULTIMATE MENU")
        self.geometry("1220x760")
        self.minsize(1080, 680)

        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("dark-blue")

        self.cleaner = Cleaner()
        self.screenshot_organizer = ScreenshotOrganizer(self.config_data)
        self.discord_status = DiscordStatus(self.config_data)
        self.hotkeys = HotkeyManager(self.config_data, self.log)
        self.text_expander = TextExpander(self.config_data, self.log)
        self.smart_search = SmartFileSearch()
        self.volume = VolumeController(self.log)
        self.autoclicker = AutoClicker(self.log)
        self.game_session = GameSession(self.config_data, self.log)
        self.notes_overlay = None

        self._build_layout()
        self.log("ZEN ULTIMATE MENU loaded.")
        self.after(500, self.refresh_dashboard)

    def _build_layout(self):
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.sidebar = ctk.CTkFrame(self, width=220, fg_color="#09090d")
        self.sidebar.grid(row=0, column=0, sticky="nsw")
        self.sidebar.grid_rowconfigure(20, weight=1)

        title = ctk.CTkLabel(
            self.sidebar,
            text="CRX\nTOOLBOX",
            font=("Consolas", 28, "bold"),
            text_color="#ff003c"
        )
        title.grid(row=0, column=0, padx=20, pady=(25, 10), sticky="ew")

        subtitle = ctk.CTkLabel(
            self.sidebar,
            text="Ultimate QOL Control Center",
            font=("Consolas", 13),
            text_color="#b6b6b6"
        )
        subtitle.grid(row=1, column=0, padx=20, pady=(0, 20))

        self.tabview = ctk.CTkTabview(self, fg_color="#101018", segmented_button_fg_color="#171722")
        self.tabview.grid(row=0, column=1, padx=12, pady=12, sticky="nsew")

        tabs = [
            "Dashboard", "Cleaner", "Files", "Discord",
            "Automation", "Gaming", "Creator", "Notes", "Credits", "Logs"
        ]

        for tab in tabs:
            self.tabview.add(tab)

        self._sidebar_button("Dashboard", 3)
        self._sidebar_button("Cleaner", 4)
        self._sidebar_button("Files", 5)
        self._sidebar_button("Discord", 6)
        self._sidebar_button("Automation", 7)
        self._sidebar_button("Gaming", 8)
        self._sidebar_button("Creator", 9)
        self._sidebar_button("Notes", 10)
        self._sidebar_button("Credits", 11)
        self._sidebar_button("Logs", 12)

        self._build_splash_overlay()

        self._build_dashboard_tab()
        self._build_cleaner_tab()
        self._build_files_tab()
        self._build_discord_tab()
        self._build_automation_tab()
        self._build_gaming_tab()
        self._build_creator_tab()
        self._build_notes_tab()
        self._build_credits_tab()
        self._build_logs_tab()

    def _sidebar_button(self, name, row):
        icons = {
            "Dashboard": "◆", "Cleaner": "◇", "Files": "▣", "Discord": "◉",
            "Automation": "⚡", "Gaming": "▶", "Creator": "✦",
            "Notes": "▤", "Credits": "★", "Logs": "▧"
        }
        btn = ctk.CTkButton(
            self.sidebar,
            text=f"{icons.get(name, '•')}  {name}",
            height=38,
            corner_radius=14,
            anchor="w",
            font=("Bahnschrift", 14, "bold"),
            fg_color="#14141f",
            hover_color="#ff003c",
            text_color="white",
            command=lambda n=name: self.tabview.set(n)
        )
        btn.grid(row=row, column=0, padx=16, pady=5, sticky="ew")

    def card(self, parent, title, text, row, col, command=None):
        frame = ctk.CTkFrame(parent, fg_color="#13131d", border_color="#2a2a35", border_width=1)
        frame.grid(row=row, column=col, padx=10, pady=10, sticky="nsew")
        frame.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(frame, text=title, font=("Bahnschrift", 19, "bold"), text_color="#ff003c").grid(
            row=0, column=0, padx=15, pady=(15, 5), sticky="w"
        )
        ctk.CTkLabel(frame, text=text, font=("Bahnschrift", 13), text_color="#d8d8d8", wraplength=250, justify="left").grid(
            row=1, column=0, padx=15, pady=5, sticky="w"
        )
        if command:
            ctk.CTkButton(frame, text="Open", fg_color="#ff003c", hover_color="#b0002a", command=command).grid(
                row=2, column=0, padx=15, pady=(10, 15), sticky="ew"
            )
        return frame

    def _animate_rec(self):
        try:
            current = self.rec_label.cget("text")
            self.rec_label.configure(text="● REC" if current == "○ REC" else "○ REC")
            self.after(650, self._animate_rec)
        except Exception:
            pass

    def _build_splash_overlay(self):
        self.splash = ctk.CTkFrame(self, fg_color="#050508", corner_radius=0)
        self.splash.place(relx=0, rely=0, relwidth=1, relheight=1)
        self.splash.lift()

        self.splash_title = ctk.CTkLabel(
            self.splash,
            text="ZEN ULTIMATE MENU",
            font=("Impact", 54),
            text_color="#ff003c"
        )
        self.splash_title.place(relx=0.5, rely=0.39, anchor="center")

        self.splash_subtitle = ctk.CTkLabel(
            self.splash,
            text="INITIALIZING QOL MODULES...",
            font=("Consolas", 16, "bold"),
            text_color="#e8e8e8"
        )
        self.splash_subtitle.place(relx=0.5, rely=0.48, anchor="center")

        self.splash_bar = ctk.CTkProgressBar(
            self.splash,
            width=430,
            height=14,
            progress_color="#ff003c",
            fg_color="#171722"
        )
        self.splash_bar.place(relx=0.5, rely=0.55, anchor="center")
        self.splash_bar.set(0)

        self.splash_status = ctk.CTkLabel(
            self.splash,
            text="[BOOT] Loading interface...",
            font=("Consolas", 13),
            text_color="#aaaaaa"
        )
        self.splash_status.place(relx=0.5, rely=0.60, anchor="center")

        self._splash_step = 0
        self.after(120, self._animate_splash)

    def _animate_splash(self):
        steps = [
            "[BOOT] Loading interface...",
            "[CORE] Registering modules...",
            "[UI] Rendering redline menu...",
            "[SYS] Starting monitors...",
            "[READY] Access granted."
        ]

        self._splash_step += 1
        progress = min(1, self._splash_step / 35)
        try:
            self.splash_bar.set(progress)
            self.splash_status.configure(text=steps[min(len(steps) - 1, int(progress * len(steps)))])
        except Exception:
            return

        if progress < 1:
            self.after(45, self._animate_splash)
        else:
            self.after(350, self._close_splash)

    def _close_splash(self):
        try:
            self.splash.destroy()
        except Exception:
            pass

    def _build_dashboard_tab(self):
        tab = self.tabview.tab("Dashboard")
        tab.grid_columnconfigure((0, 1, 2), weight=1)

        header = ctk.CTkLabel(tab, text="ACCESS GRANTED // ZEN ULTIMATE MENU", font=("Impact", 34), text_color="#ff003c")
        header.grid(row=0, column=0, columnspan=3, padx=15, pady=(20, 10), sticky="w")

        self.cpu_label = ctk.CTkLabel(tab, text="CPU: --", font=("Consolas", 15))
        self.ram_label = ctk.CTkLabel(tab, text="RAM: --", font=("Consolas", 15))
        self.disk_label = ctk.CTkLabel(tab, text="DISK: --", font=("Consolas", 15))
        self.cpu_label.grid(row=1, column=0, padx=15, pady=10, sticky="w")
        self.ram_label.grid(row=1, column=1, padx=15, pady=10, sticky="w")
        self.disk_label.grid(row=1, column=2, padx=15, pady=10, sticky="w")

        self.card(tab, "Cleaner", "Remove temporary files, caches and junk safely.", 2, 0, lambda: self.tabview.set("Cleaner"))
        self.card(tab, "Smart Search", "Search files by name, extension and date.", 2, 1, lambda: self.tabview.set("Files"))
        self.card(tab, "Discord Status", "Auto Rich Presence based on apps.", 2, 2, lambda: self.tabview.set("Discord"))
        self.card(tab, "Hotkeys", "Global shortcuts for apps, links and text.", 3, 0, lambda: self.tabview.set("Automation"))
        self.card(tab, "Game Session", "Prepare your PC before playing.", 3, 1, lambda: self.tabview.set("Gaming"))
        self.card(tab, "README Generator", "Create themed README.md files fast.", 3, 2, lambda: self.tabview.set("Creator"))

    def _build_cleaner_tab(self):
        tab = self.tabview.tab("Cleaner")
        tab.grid_columnconfigure(0, weight=1)
        ctk.CTkLabel(tab, text="Junk Cleaner", font=("Consolas", 25, "bold"), text_color="#ff003c").grid(row=0, column=0, padx=15, pady=15, sticky="w")

        self.cleaner_output = ctk.CTkTextbox(tab, height=380, fg_color="#08080c", text_color="#e8e8e8", font=("Consolas", 13))
        self.cleaner_output.grid(row=1, column=0, padx=15, pady=10, sticky="nsew")

        btns = ctk.CTkFrame(tab, fg_color="transparent")
        btns.grid(row=2, column=0, padx=15, pady=10, sticky="ew")
        ctk.CTkButton(btns, text="Scan", fg_color="#ff003c", command=self.run_cleaner_scan).pack(side="left", padx=5)
        ctk.CTkButton(btns, text="Clean Selected Safe", fg_color="#ff003c", command=self.run_cleaner_clean).pack(side="left", padx=5)
        ctk.CTkButton(btns, text="Open Temp Folder", command=lambda: os.startfile(os.getenv("TEMP"))).pack(side="left", padx=5)

    def _build_files_tab(self):
        tab = self.tabview.tab("Files")
        tab.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(tab, text="Files / Screenshots / Smart Search", font=("Consolas", 25, "bold"), text_color="#ff003c").grid(row=0, column=0, padx=15, pady=15, sticky="w")

        row = ctk.CTkFrame(tab, fg_color="transparent")
        row.grid(row=1, column=0, padx=15, pady=5, sticky="ew")
        row.grid_columnconfigure(0, weight=1)

        self.search_entry = ctk.CTkEntry(row, placeholder_text="Search files, example: .png, readme, roblox, .mp4")
        self.search_entry.grid(row=0, column=0, padx=(0, 8), sticky="ew")
        ctk.CTkButton(row, text="Search Folder", fg_color="#ff003c", command=self.search_files).grid(row=0, column=1)

        self.files_output = ctk.CTkTextbox(tab, height=360, fg_color="#08080c", font=("Consolas", 12))
        self.files_output.grid(row=2, column=0, padx=15, pady=10, sticky="nsew")

        actions = ctk.CTkFrame(tab, fg_color="transparent")
        actions.grid(row=3, column=0, padx=15, pady=10, sticky="ew")
        ctk.CTkButton(actions, text="Organize Screenshots", fg_color="#ff003c", command=self.organize_screenshots).pack(side="left", padx=5)
        ctk.CTkButton(actions, text="Open Downloads", command=lambda: os.startfile(Path.home() / "Downloads")).pack(side="left", padx=5)

    def _build_discord_tab(self):
        tab = self.tabview.tab("Discord")
        tab.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(tab, text="Discord Auto Status", font=("Consolas", 25, "bold"), text_color="#ff003c").grid(row=0, column=0, padx=15, pady=15, sticky="w")

        self.discord_status_label = ctk.CTkLabel(tab, text="Status: stopped", font=("Consolas", 15))
        self.discord_status_label.grid(row=1, column=0, padx=15, pady=5, sticky="w")

        row = ctk.CTkFrame(tab, fg_color="transparent")
        row.grid(row=2, column=0, padx=15, pady=10, sticky="w")
        ctk.CTkButton(row, text="Start Discord Status", fg_color="#ff003c", command=self.start_discord).pack(side="left", padx=5)
        ctk.CTkButton(row, text="Stop Discord Status", command=self.stop_discord).pack(side="left", padx=5)

        self.discord_output = ctk.CTkTextbox(tab, height=360, fg_color="#08080c", font=("Consolas", 13))
        self.discord_output.grid(row=3, column=0, padx=15, pady=10, sticky="nsew")
        self.discord_output.insert("end", "Edit config.json to add Discord + Spotify IDs. Spotify has priority when music is playing.\n")

    def _build_automation_tab(self):
        tab = self.tabview.tab("Automation")
        tab.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(tab, text="Automation / Hotkeys / Text Expander / Auto Clicker", font=("Consolas", 25, "bold"), text_color="#ff003c").grid(row=0, column=0, padx=15, pady=15, sticky="w")

        row1 = ctk.CTkFrame(tab, fg_color="#13131d")
        row1.grid(row=1, column=0, padx=15, pady=10, sticky="ew")
        ctk.CTkButton(row1, text="Start Hotkeys", fg_color="#ff003c", command=self.start_hotkeys).pack(side="left", padx=8, pady=10)
        ctk.CTkButton(row1, text="Stop Hotkeys", command=self.stop_hotkeys).pack(side="left", padx=8, pady=10)
        ctk.CTkButton(row1, text="Start Text Expander", fg_color="#ff003c", command=self.start_expander).pack(side="left", padx=8, pady=10)
        ctk.CTkButton(row1, text="Stop Text Expander", command=self.stop_expander).pack(side="left", padx=8, pady=10)

        row2 = ctk.CTkFrame(tab, fg_color="#13131d")
        row2.grid(row=2, column=0, padx=15, pady=10, sticky="ew")
        self.click_interval = ctk.CTkEntry(row2, width=90, placeholder_text="0.1")
        self.click_interval.pack(side="left", padx=8)
        ctk.CTkButton(row2, text="Start Safe Auto Clicker", fg_color="#ff003c", command=self.start_clicker).pack(side="left", padx=8, pady=10)
        ctk.CTkButton(row2, text="Stop Auto Clicker", command=self.stop_clicker).pack(side="left", padx=8, pady=10)

        self.automation_output = ctk.CTkTextbox(tab, height=300, fg_color="#08080c", font=("Consolas", 13))
        self.automation_output.grid(row=3, column=0, padx=15, pady=10, sticky="nsew")
        self.automation_output.insert("end", "Hotkeys and text expansions are configured in config.json.\n")

    def _build_gaming_tab(self):
        tab = self.tabview.tab("Gaming")
        tab.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(tab, text="Gaming Tools", font=("Consolas", 25, "bold"), text_color="#ff003c").grid(row=0, column=0, padx=15, pady=15, sticky="w")

        row = ctk.CTkFrame(tab, fg_color="#13131d")
        row.grid(row=1, column=0, padx=15, pady=10, sticky="ew")
        ctk.CTkButton(row, text="Start Game Session", fg_color="#ff003c", command=self.start_game_session).pack(side="left", padx=8, pady=10)
        ctk.CTkButton(row, text="End Game Session", command=self.end_game_session).pack(side="left", padx=8, pady=10)
        ctk.CTkButton(row, text="Refresh App Volumes", command=self.refresh_volumes).pack(side="left", padx=8, pady=10)

        self.volume_output = ctk.CTkTextbox(tab, height=400, fg_color="#08080c", font=("Consolas", 13))
        self.volume_output.grid(row=2, column=0, padx=15, pady=10, sticky="nsew")

    def _build_creator_tab(self):
        tab = self.tabview.tab("Creator")
        tab.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(tab, text="Creator Tools / README Generator", font=("Consolas", 25, "bold"), text_color="#ff003c").grid(row=0, column=0, columnspan=2, padx=15, pady=15, sticky="w")

        self.readme_name = ctk.CTkEntry(tab, placeholder_text="Project name")
        self.readme_desc = ctk.CTkEntry(tab, placeholder_text="Project description")
        self.readme_author = ctk.CTkEntry(tab, placeholder_text="Author/GitHub username")

        self.readme_name.grid(row=1, column=0, padx=15, pady=6, sticky="ew")
        self.readme_desc.grid(row=2, column=0, padx=15, pady=6, sticky="ew")
        self.readme_author.grid(row=3, column=0, padx=15, pady=6, sticky="ew")

        ctk.CTkButton(tab, text="Generate README.md", fg_color="#ff003c", command=self.generate_readme_file).grid(row=4, column=0, padx=15, pady=10, sticky="ew")

        self.creator_output = ctk.CTkTextbox(tab, height=430, fg_color="#08080c", font=("Consolas", 13))
        self.creator_output.grid(row=1, column=1, rowspan=5, padx=15, pady=10, sticky="nsew")

    def _build_notes_tab(self):
        tab = self.tabview.tab("Notes")
        tab.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(tab, text="Desktop Note Overlay", font=("Consolas", 25, "bold"), text_color="#ff003c").grid(row=0, column=0, padx=15, pady=15, sticky="w")

        self.notes_text = ctk.CTkTextbox(tab, height=360, fg_color="#08080c", font=("Consolas", 14))
        self.notes_text.grid(row=1, column=0, padx=15, pady=10, sticky="nsew")
        self.notes_text.insert("end", "Tasks:\n[ ] Study\n[ ] Code\n[ ] Push to GitHub\n")

        row = ctk.CTkFrame(tab, fg_color="transparent")
        row.grid(row=2, column=0, padx=15, pady=10, sticky="ew")
        ctk.CTkButton(row, text="Open Overlay", fg_color="#ff003c", command=self.open_notes_overlay).pack(side="left", padx=5)
        ctk.CTkButton(row, text="Close Overlay", command=self.close_notes_overlay).pack(side="left", padx=5)

    def _open_link(self, url):
        webbrowser.open(url)

    def _build_credits_tab(self):
        tab = self.tabview.tab("Credits")
        tab.grid_columnconfigure((0, 1), weight=1)

        ctk.CTkLabel(
            tab,
            text="CREDITS / CONTACT",
            font=("Impact", 34),
            text_color="#ff003c"
        ).grid(row=0, column=0, columnspan=2, padx=15, pady=(20, 5), sticky="w")

        info = ctk.CTkFrame(tab, fg_color="#13131d", border_width=1, border_color="#2a2a35")
        info.grid(row=1, column=0, padx=15, pady=15, sticky="nsew")

        ctk.CTkLabel(info, text="ZEN ULTIMATE MENU", font=("Impact", 30), text_color="#ff003c").pack(anchor="w", padx=18, pady=(18, 4))
        ctk.CTkLabel(info, text="A Windows QOL toolbox made for automation, cleanup, gaming sessions and creator tools.", font=("Bahnschrift", 14), text_color="#e8e8e8", wraplength=440, justify="left").pack(anchor="w", padx=18, pady=6)
        ctk.CTkLabel(info, text="Created by Zen / superstandarts", font=("Bahnschrift", 16, "bold"), text_color="#ffffff").pack(anchor="w", padx=18, pady=(14, 4))
        ctk.CTkLabel(info, text="Discord: 7mey", font=("Consolas", 14), text_color="#ffb3c3").pack(anchor="w", padx=18, pady=4)

        links = ctk.CTkFrame(tab, fg_color="#13131d", border_width=1, border_color="#2a2a35")
        links.grid(row=1, column=1, padx=15, pady=15, sticky="nsew")

        ctk.CTkLabel(links, text="SOCIAL LINKS", font=("Impact", 28), text_color="#ff003c").pack(anchor="w", padx=18, pady=(18, 10))

        social_buttons = [
            ("GitHub  / superstandarts", "https://github.com/superstandarts"),
            ("Instagram / xyphanctinusultrazaliextremus", "https://www.instagram.com/xyphanctinusultrazaliextremus/"),
            ("Steam / hokurary", "https://steamcommunity.com/id/hokurary"),
            ("Roblox / Profile", "https://www.roblox.com/users/5583806069/profile")
        ]

        for label, url in social_buttons:
            ctk.CTkButton(
                links,
                text=label,
                height=40,
                corner_radius=14,
                anchor="w",
                font=("Bahnschrift", 14, "bold"),
                fg_color="#181824",
                hover_color="#ff003c",
                command=lambda u=url: self._open_link(u)
            ).pack(fill="x", padx=18, pady=6)

        bottom = ctk.CTkFrame(tab, fg_color="#08080c", border_width=1, border_color="#2a2a35")
        bottom.grid(row=2, column=0, columnspan=2, padx=15, pady=15, sticky="ew")

        ctk.CTkLabel(
            bottom,
            text="SYSTEM STATUS: ONLINE     BUILD: COMMUNITY     ACCESS: GRANTED",
            font=("Consolas", 14, "bold"),
            text_color="#ff003c"
        ).pack(padx=15, pady=16)

    def _build_logs_tab(self):
        tab = self.tabview.tab("Logs")
        tab.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(tab, text="Logs", font=("Consolas", 25, "bold"), text_color="#ff003c").grid(row=0, column=0, padx=15, pady=15, sticky="w")
        self.logbox = ctk.CTkTextbox(tab, fg_color="#08080c", font=("Consolas", 13))
        self.logbox.grid(row=1, column=0, padx=15, pady=10, sticky="nsew")

    def log(self, msg):
        stamp = datetime.now().strftime("%H:%M:%S")
        line = f"[{stamp}] {msg}\n"
        print(line, end="")
        if hasattr(self, "logbox"):
            self.logbox.insert("end", line)
            self.logbox.see("end")

    def refresh_dashboard(self):
        try:
            self.cpu_label.configure(text=f"CPU: {psutil.cpu_percent()}%")
            self.ram_label.configure(text=f"RAM: {psutil.virtual_memory().percent}%")
            self.disk_label.configure(text=f"DISK: {psutil.disk_usage('/').percent}%")
        except Exception:
            pass
        self.after(2000, self.refresh_dashboard)

    def run_thread(self, func):
        threading.Thread(target=func, daemon=True).start()

    def run_cleaner_scan(self):
        def job():
            self.cleaner_output.delete("1.0", "end")
            results = self.cleaner.scan()
            for r in results:
                self.cleaner_output.insert("end", f"{r['name']}: {r['items']} files | {r['size_mb']:.2f} MB\n")
            self.log("Cleaner scan completed.")
        self.run_thread(job)

    def run_cleaner_clean(self):
        if not messagebox.askyesno("ZEN Cleaner", "Move detected junk files to Recycle Bin?"):
            return
        def job():
            summary = self.cleaner.clean_safe()
            self.cleaner_output.insert("end", "\nCLEAN SUMMARY:\n")
            for item in summary:
                self.cleaner_output.insert("end", f"{item}\n")
            self.log("Cleaner safe clean completed.")
        self.run_thread(job)

    def organize_screenshots(self):
        count = self.screenshot_organizer.organize()
        self.files_output.insert("end", f"Organized screenshots: {count}\n")
        self.log(f"Screenshot organizer moved {count} files.")

    def search_files(self):
        folder = filedialog.askdirectory(title="Select folder to search")
        if not folder:
            return
        query = self.search_entry.get().strip()
        results = self.smart_search.search(folder, query, limit=200)
        self.files_output.delete("1.0", "end")
        for path in results:
            self.files_output.insert("end", str(path) + "\n")
        self.log(f"Smart search found {len(results)} results.")

    def start_discord(self):
        self.discord_status.start()
        self.discord_status_label.configure(text="Status: running")
        self.discord_output.insert("end", "Discord status started.\n")
        self.log("Discord auto status started.")

    def stop_discord(self):
        self.discord_status.stop()
        self.discord_status_label.configure(text="Status: stopped")
        self.discord_output.insert("end", "Discord status stopped.\n")
        self.log("Discord auto status stopped.")

    def start_hotkeys(self):
        self.hotkeys.start()
        self.automation_output.insert("end", "Hotkeys started.\n")

    def stop_hotkeys(self):
        self.hotkeys.stop()
        self.automation_output.insert("end", "Hotkeys stopped.\n")

    def start_expander(self):
        self.text_expander.start()
        self.automation_output.insert("end", "Text expander started.\n")

    def stop_expander(self):
        self.text_expander.stop()
        self.automation_output.insert("end", "Text expander stopped.\n")

    def start_clicker(self):
        try:
            interval = float(self.click_interval.get() or "0.1")
        except ValueError:
            interval = 0.1
        self.autoclicker.start(interval=interval, max_clicks=500)
        self.automation_output.insert("end", "Safe auto clicker started. Move mouse to top-left corner to stop.\n")

    def stop_clicker(self):
        self.autoclicker.stop()
        self.automation_output.insert("end", "Auto clicker stopped.\n")

    def refresh_volumes(self):
        sessions = self.volume.list_sessions()
        self.volume_output.delete("1.0", "end")
        for item in sessions:
            self.volume_output.insert("end", f"{item}\n")
        self.log("Volume sessions refreshed.")

    def start_game_session(self):
        self.game_session.start_session()
        self.log("Game session started.")

    def end_game_session(self):
        self.game_session.end_session()
        self.log("Game session ended.")

    def generate_readme_file(self):
        name = self.readme_name.get().strip() or "ZEN Project"
        desc = self.readme_desc.get().strip() or "A ZEN-style project."
        author = self.readme_author.get().strip() or "superstandarts"
        content = generate_readme(name, desc, author)
        self.creator_output.delete("1.0", "end")
        self.creator_output.insert("end", content)
        save = filedialog.asksaveasfilename(defaultextension=".md", initialfile="README.md")
        if save:
            Path(save).write_text(content, encoding="utf-8")
            self.log(f"README generated: {save}")

    def open_notes_overlay(self):
        text = self.notes_text.get("1.0", "end").strip()
        if self.notes_overlay:
            self.notes_overlay.destroy()
        self.notes_overlay = NotesOverlay(text)
        self.log("Notes overlay opened.")

    def close_notes_overlay(self):
        if self.notes_overlay:
            self.notes_overlay.destroy()
            self.notes_overlay = None
            self.log("Notes overlay closed.")


if __name__ == "__main__":
    app = ZenUltimateMenu()
    app.mainloop()
