
import os
import sys
import json
import shutil
import time
import ctypes
import winsound
import threading
import subprocess
import webbrowser
from pathlib import Path
from datetime import datetime
from tkinter import filedialog, messagebox

import customtkinter as ctk
import psutil
import pyperclip
from PIL import Image

from modules.cleaner import Cleaner
from modules.screenshot_organizer import ScreenshotOrganizer
from modules.discord_status import DiscordStatus
from modules.hotkeys import HotkeyManager
from modules.text_expander import TextExpander
from modules.file_search import SmartFileSearch
from modules.readme_generator import generate_readme
from modules.volume_controller import VolumeController
from modules.autoclicker import AutoClicker
from modules.game_session import GameSession

from modules.config_editor import ConfigEditor
from modules.process_manager import ProcessManager
from modules.internet_tools import InternetTools
from modules.privacy_cleaner import PrivacyCleaner
from modules.theme_manager import ThemeManager
from modules.password_generator import PasswordGenerator
from modules.app_profiles import AppProfiles
from modules.notifier import Notifier
from modules.tray_manager import TrayManager
from modules.zenai import ZENAI
from modules.quick_launcher import QuickLauncher
from modules.startup_manager import StartupManager
from modules.windows_repair import WindowsRepair
from modules.performance_monitor import PerformanceMonitor
from modules.converters import Converters
from modules.image_tools import ImageTools
from modules.github_tools import GitHubTools
from modules.project_creator import ProjectCreator
from modules.error_analyzer import ErrorAnalyzer
from modules.exe_builder import ExeBuilder
from modules.zenai_actions import ZENAIConfigActions
from modules.music_widget import MusicWidget
from modules.ultimate_uninstaller import UltimateUninstaller
from modules.app_health_checker import AppHealthChecker
from modules.dependency_doctor import DependencyDoctor
from modules.safe_mode import SafeMode
from modules.mini_terminal import MiniTerminal
from modules.env_editor import EnvEditor
from modules.update_checker import UpdateChecker
from modules.changelog_viewer import ChangelogViewer
from modules.plugin_system import PluginSystem
from modules.duplicate_finder import DuplicateFinder
from modules.large_file_finder import LargeFileFinder
from modules.folder_size_analyzer import FolderSizeAnalyzer
from modules.fake_terminal_generator import FakeTerminalGenerator
from modules.floating_widget import FloatingWidget


def get_app_dir():
    if getattr(sys, "frozen", False):
        return Path(sys.executable).resolve().parent
    return Path(__file__).resolve().parent


APP_DIR = get_app_dir()
CONFIG_PATH = APP_DIR / "config.json"


def load_config():
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)

    # Easy top-level settings. These override nested values so users do not need
    # to hunt through config.json every time.
    quick = data.get("_quick_settings", {})
    if quick:
        discord = data.setdefault("discord", {})
        spotify = discord.setdefault("spotify", {})
        theme = data.setdefault("theme", {})
        zenai = data.setdefault("zenai", {})

        mapping = {
            "discord_enabled": (discord, "enabled"),
            "discord_client_id": (discord, "client_id"),
            "spotify_enabled": (spotify, "enabled"),
            "spotify_client_id": (spotify, "client_id"),
            "spotify_client_secret": (spotify, "client_secret"),
            "spotify_redirect_uri": (spotify, "redirect_uri"),
            "theme_mode": (theme, "mode"),
            "theme_accent": (theme, "accent"),
            "zenai_provider": (zenai, "provider"),
            "zenai_model": (zenai, "model"),
            "zenai_ollama_url": (zenai, "ollama_url")
        }

        for key, (target, target_key) in mapping.items():
            if key in quick:
                target[target_key] = quick[key]

    return data


class ZenUltimateMenu(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.config_data = load_config()
        self.title("ZEN MENU")
        try:
            icon_path = APP_DIR / "assets" / "icons" / "app.ico"
            if icon_path.exists():
                self.iconbitmap(str(icon_path))
        except Exception:
            pass

        screen_w = self.winfo_screenwidth()
        screen_h = self.winfo_screenheight()

        # Safe responsive window size.
        # Uses less height so buttons never go under the taskbar on 1366x768.
        usable_h = max(560, screen_h - 90)
        win_w = min(1440, max(920, int(screen_w * 0.90)))
        win_h = min(840, max(560, int(usable_h * 0.92)))
        pos_x = max(0, int((screen_w - win_w) / 2))
        pos_y = 20
        self.geometry(f"{win_w}x{win_h}+{pos_x}+{pos_y}")
        self.minsize(900, 560)

        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("dark-blue")

        self.colors = {
            "bg": "#020203",
            "panel": "#0a0b0e",
            "panel2": "#050609",
            "panel3": "#101116",
            "line": "#252730",
            "soft_line": "#17191f",
            "text": "#f8f8fa",
            "muted": "#9fa2ad",
            "button": "#171920",
            "button_hover": "#252833",
            "accent": "#ffffff"
        }

        self.cleaner = Cleaner()
        self.screenshot_organizer = ScreenshotOrganizer(self.config_data)
        self.discord_status = DiscordStatus(self.config_data)
        self.hotkeys = HotkeyManager(self.config_data, self.log)
        self.text_expander = TextExpander(self.config_data, self.log)
        self.smart_search = SmartFileSearch()
        self.volume = VolumeController(self.log)
        self.autoclicker = AutoClicker(self.log)
        self.game_session = GameSession(self.config_data, self.log)

        self.config_editor = ConfigEditor(CONFIG_PATH)
        self.process_manager = ProcessManager()
        self.internet_tools = InternetTools()
        self.privacy_cleaner = PrivacyCleaner()
        self.password_generator = PasswordGenerator()
        self.profiles_manager = AppProfiles(self.config_data, self.log)
        self.notifier = Notifier("ZEN MENU")
        self.tray_manager = TrayManager(self)
        self.zenai = ZENAI(CONFIG_PATH)
        self.quick_launcher = QuickLauncher(self.config_data)
        self.startup_manager = StartupManager()
        self.windows_repair = WindowsRepair()
        self.performance_monitor = PerformanceMonitor()
        self.converters = Converters()
        self.image_tools = ImageTools()
        self.github_tools = GitHubTools()
        self.project_creator = ProjectCreator()
        self.error_analyzer = ErrorAnalyzer()
        self.exe_builder = ExeBuilder()
        self.zenai_actions = ZENAIConfigActions(CONFIG_PATH)
        self.music_widget = MusicWidget(self.config_data)
        self.ultimate_uninstaller = UltimateUninstaller()
        self.safe_mode = SafeMode(sys.argv)
        self.app_health_checker = AppHealthChecker(APP_DIR, CONFIG_PATH)
        self.dependency_doctor = DependencyDoctor()
        self.mini_terminal = MiniTerminal()
        self.env_editor = EnvEditor()
        self.update_checker = UpdateChecker(self.config_data.get("app_version", "1.0.0"), self.config_data.get("update_url", ""))
        self.changelog_viewer = ChangelogViewer(APP_DIR)
        self.plugin_system = PluginSystem(APP_DIR)
        self.duplicate_finder = DuplicateFinder()
        self.large_file_finder = LargeFileFinder()
        self.folder_size_analyzer = FolderSizeAnalyzer()
        self.fake_terminal_generator = FakeTerminalGenerator()
        self.floating_widget = FloatingWidget(self)

        self.notes_overlay = None
        self.frames = {}
        self.active_page = None

        self._build_layout()
        self._play_startup_sound()
        self._show_splash()
        self.show_page("Dashboard")
        self.log("ZEN MENU loaded.")
        self.after(800, self.refresh_dashboard)

    def _play_startup_sound(self):
        def worker():
            wav_path = APP_DIR / "assets" / "sounds" / "startup.wav"
            mp3_path = APP_DIR / "assets" / "sounds" / "startup.mp3"

            try:
                if wav_path.exists():
                    winsound.PlaySound(str(wav_path), winsound.SND_FILENAME | winsound.SND_ASYNC)
                    return
            except Exception:
                pass

            try:
                if mp3_path.exists():
                    ps_path = str(mp3_path).replace("'", "''")
                    command = (
                        "Add-Type -AssemblyName PresentationCore; "
                        "$p=New-Object System.Windows.Media.MediaPlayer; "
                        f"$p.Open([Uri]'{ps_path}'); "
                        "$p.Volume=0.75; "
                        "$p.Play(); "
                        "Start-Sleep -Milliseconds 2500;"
                    )
                    subprocess.Popen(
                        ["powershell", "-NoProfile", "-STA", "-WindowStyle", "Hidden", "-Command", command],
                        stdout=subprocess.DEVNULL,
                        stderr=subprocess.DEVNULL,
                        creationflags=subprocess.CREATE_NO_WINDOW if os.name == "nt" else 0
                    )
                    return
            except Exception:
                pass

        threading.Thread(target=worker, daemon=True).start()

    def _show_splash(self):
        splash = ctk.CTkFrame(self, fg_color="#000000")
        splash.place(relx=0, rely=0, relwidth=1, relheight=1)
        splash.lift()

        intro = ctk.CTkFrame(
            splash,
            fg_color="#020203",
            border_width=2,
            border_color="#3a3a3a",
            corner_radius=0
        )
        intro.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.78, relheight=0.62)

        banner_path = APP_DIR / "assets" / "banners" / "zen_banner.png"
        self.intro_banner_img = None
        if banner_path.exists():
            try:
                img = Image.open(banner_path)
                self.intro_banner_img = ctk.CTkImage(light_image=img, dark_image=img, size=(820, 260))
                ctk.CTkLabel(intro, image=self.intro_banner_img, text="").place(relx=0.5, rely=0.38, anchor="center")
            except Exception:
                pass

        thanks = ctk.CTkLabel(
            intro,
            text="Thanks for using CRX!",
            font=("Consolas", 25, "bold"),
            text_color="#ffffff"
        )
        thanks.place(relx=0.5, rely=0.72, anchor="center")

        sub = ctk.CTkLabel(
            intro,
            text="[ ACCESS GRANTED ]  ZEN CORE INITIALIZING...",
            font=("Consolas", 13),
            text_color="#a8a8a8"
        )
        sub.place(relx=0.5, rely=0.79, anchor="center")

        # Fade-in effect for the terminal-style intro.
        fade_layers = []
        for i in range(9):
            layer = ctk.CTkFrame(intro, fg_color="#000000", corner_radius=0)
            layer.place(relx=0, rely=0, relwidth=1, relheight=1)
            fade_layers.append(layer)

        def fade(i=0):
            if i < len(fade_layers):
                try:
                    fade_layers[i].destroy()
                except Exception:
                    pass
                self.after(95, lambda: fade(i + 1))
            else:
                self.after(900, show_loading)

        def show_loading():
            for child in splash.winfo_children():
                child.destroy()

            card = ctk.CTkFrame(
                splash,
                fg_color="#050609",
                border_width=1,
                border_color="#2a2d36",
                corner_radius=0
            )
            card.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.72, relheight=0.70)

            ctk.CTkLabel(
                card,
                text="ZEN MENU",
                font=("Consolas", 42, "bold"),
                text_color="#ffffff"
            ).place(relx=0.5, rely=0.27, anchor="center")

            ctk.CTkLabel(
                card,
                text="Thanks for using CRX!",
                font=("Consolas", 19, "bold"),
                text_color="#d8d8d8"
            ).place(relx=0.5, rely=0.42, anchor="center")

            ctk.CTkLabel(
                card,
                text="Loading modules, profiles, tools and ZENAI...",
                font=("Consolas", 13),
                text_color="#9f9f9f"
            ).place(relx=0.5, rely=0.50, anchor="center")

            bar = ctk.CTkProgressBar(card, width=460, height=12, corner_radius=0, progress_color="#e7e7e7", fg_color="#171920")
            bar.place(relx=0.5, rely=0.66, anchor="center")
            bar.set(0)

            status = ctk.CTkLabel(card, text="[BOOT] Preparing interface...", font=("Consolas", 12), text_color="#8f8f8f")
            status.place(relx=0.5, rely=0.74, anchor="center")

            steps = ["[BOOT] Preparing interface...", "[CORE] Loading modules...", "[PLUGINS] Loading plugins...", "[ZENAI] Local assistant ready...", "[READY] Welcome."]

            def animate(j=0):
                progress = min(1, j / 58)
                bar.set(progress)
                status.configure(text=steps[min(len(steps)-1, int(progress * len(steps)))])
                if progress < 1:
                    self.after(28, lambda: animate(j + 1))
                else:
                    self.after(360, splash.destroy)

            animate()

        fade()


    def _scroll_sidebar_wheel(self, event):
        try:
            steps = int(-1 * (event.delta / 120) * 4)
            self.nav_frame._parent_canvas.yview_scroll(steps, "units")
            return "break"
        except Exception:
            return None

    def _bind_sidebar_scroll_recursive(self, widget):
        try:
            widget.bind("<MouseWheel>", self._scroll_sidebar_wheel)
            for child in widget.winfo_children():
                self._bind_sidebar_scroll_recursive(child)
        except Exception:
            pass

    def _build_layout(self):
        self.configure(fg_color=self.colors["bg"])
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.sidebar = ctk.CTkFrame(self, width=248, fg_color=self.colors["bg"], corner_radius=0)
        self.sidebar.grid(row=0, column=0, sticky="nsw")
        self.sidebar.grid_propagate(False)
        self.sidebar.grid_columnconfigure(0, weight=1)
        self.sidebar.grid_rowconfigure(3, weight=1)

        self.rec_label = ctk.CTkLabel(self.sidebar, text="● READY", font=("Segoe UI Variable", 13, "bold"), text_color="#ffffff")
        self.rec_label.grid(row=0, column=0, padx=22, pady=(20, 0), sticky="w")

        ctk.CTkLabel(
            self.sidebar,
            text="ZEN\nULTIMATE\nMENU",
            font=("Segoe UI Variable Display", 30, "bold"),
            text_color="#ffffff",
            justify="left"
        ).grid(row=1, column=0, padx=22, pady=(10, 6), sticky="w")

        ctk.CTkLabel(
            self.sidebar,
            text="QOL control center",
            font=("Segoe UI Variable", 13),
            text_color="#c9c9c9"
        ).grid(row=2, column=0, padx=22, pady=(0, 12), sticky="w")

        self.nav_frame = ctk.CTkScrollableFrame(
            self.sidebar,
            fg_color="#08080a",
            scrollbar_button_color="#2f2f35",
            scrollbar_button_hover_color="#44444b",
            corner_radius=0
        )
        self.nav_frame.grid(row=3, column=0, padx=0, pady=(0, 12), sticky="nsew")
        self.nav_frame.grid_columnconfigure(0, weight=1)

        def _nav_mousewheel(event):
            try:
                self.nav_frame._parent_canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
            except Exception:
                pass

        def _bind_nav_scroll(_event=None):
            self.nav_frame.bind_all("<MouseWheel>", _nav_mousewheel)

        def _unbind_nav_scroll(_event=None):
            self.nav_frame.unbind_all("<MouseWheel>")

        self.nav_frame.bind("<Enter>", _bind_nav_scroll)
        self.nav_frame.bind("<Leave>", _unbind_nav_scroll)

        self._animate_rec()

        def _global_mousewheel_router(event):
            try:
                x = self.winfo_pointerx() - self.winfo_rootx()
                if 0 <= x <= self.sidebar.winfo_width():
                    self._scroll_sidebar_wheel(event)
                    return "break"
            except Exception:
                pass

        self.bind_all("<MouseWheel>", _global_mousewheel_router)

        self.main_area = ctk.CTkFrame(self, fg_color=self.colors["panel2"], corner_radius=0)
        self.main_area.grid(row=0, column=1, padx=0, pady=0, sticky="nsew")
        self.main_area.grid_columnconfigure(0, weight=1)
        self.main_area.grid_rowconfigure(0, weight=1)

        pages = [
            ("Dashboard", "⌂"),
            ("Config Profiles", "♢"),
            ("Macro Builder", "⛓"),
            ("Flow Builder", "⌁"),
            ("Global Search", "⌕"),
            ("Mini Apps", "▱"),
            ("Game Overlay", "◫"),
            ("Theme Preview", "◐"),
            ("Soundboard", "♫"),
            ("Level System", "LVL"),
            ("Usage Heatmap", "▦"),
            ("Time Tracker", "◷"),
            ("Text Tools", "T"),
            ("Setup Wizard", "◇"),
            ("Command", "⌘"),
            ("Appearance", "◑"),
            ("Help", "?"),
            ("What's New", "≡"),
            ("Plugin Store", "☷"),
            ("Health", "✓"),
            ("Dependencies", "◇"),
            ("Safe Mode", "□"),
            ("Terminal", ">"),
            ("Environment", "PATH"),
            ("Updates", "↑"),
            ("Changelog", "≡"),
            ("Plugins", "☷"),
            ("Duplicates", "◆"),
            ("Large Files", "⬢"),
            ("Folder Sizes", "▨"),
            ("Fake Terminal", "▣"),
            ("Floating Widget", "◱"),
            ("Quick", "▤"),
            ("Startup", "↟"),
            ("Repair", "◧"),
            ("Performance", "▥"),
            ("Converters", "⇄"),
            ("Image Tools", "▧"),
            ("GitHub", "⌘"),
            ("Project Maker", "✚"),
            ("Error Analyzer", "!"),
            ("EXE Builder", "▣"),
            ("ZENAI Actions", "✦"),
            ("Music", "♪"),
            ("Uninstaller", "✕"),
            ("Settings", "⚙"),
            ("Profiles", "◈"),
            ("Processes", "▦"),
            ("Internet", "◎"),
            ("Privacy", "◌"),
            ("Themes", "◑"),
            ("Passwords", "◆"),
            ("ZENAI", "✦"),
            ("Cleaner", "🧹"),
            ("Files", "📁"),
            ("Discord", "●"),
            ("Automation", "⚡"),
            ("Gaming", "▶"),
            ("Creator", "✎"),
            ("Credits", "★"),
            ("Logs", "▣"),
        ]

        for idx, (name, icon) in enumerate(pages, start=0):
            self._sidebar_button(name, icon, idx)

        self.after(200, lambda: self._bind_sidebar_scroll_recursive(self.nav_frame))

        for name, _ in pages:
            frame = ctk.CTkFrame(self.main_area, fg_color=self.colors["panel2"], corner_radius=0)
            frame.grid(row=0, column=0, sticky="nsew")
            frame.grid_columnconfigure(0, weight=1)
            frame.grid_rowconfigure(99, weight=1)
            self.frames[name] = frame

        self._build_pages()

    def _animate_rec(self):
        try:
            current = self.rec_label.cget("text")
            self.rec_label.configure(
                text="● READY" if current == "○ READY" else "○ READY",
                text_color="#ffffff" if current == "○ READY" else "#9f9f9f"
            )
            self.after(700, self._animate_rec)
        except Exception:
            pass

    def _sidebar_button(self, name, icon, row):
        btn = ctk.CTkButton(
            self.nav_frame,
            text=f"{icon}   {name}",
            height=38,
            corner_radius=18,
            anchor="w",
            font=("Segoe UI Variable", 13, "bold"),
            fg_color=self.colors["button"],
            hover_color=self.colors["button_hover"],
            text_color=self.colors["text"],
            border_width=1,
            border_color=self.colors["line"],
            command=lambda n=name: self.show_page(n)
        )
        btn.grid(row=row, column=0, padx=18, pady=4, sticky="ew")
        btn.bind("<MouseWheel>", self._scroll_sidebar_wheel)

    def show_page(self, name):
        if name not in self.frames:
            return

        for frame in self.frames.values():
            frame.grid_remove()

        self.frames[name].grid(row=0, column=0, sticky="nsew")
        self.active_page = name
        self._flash_transition(f"OPENING // {name.upper()}")

    def _flash_transition(self, text):
        overlay = ctk.CTkFrame(self.main_area, fg_color="#050506", corner_radius=0)
        overlay.place(relx=0, rely=0, relwidth=1, relheight=1)
        overlay.lift()

        ctk.CTkLabel(overlay, text=text, font=("Segoe UI Variable Display", 32, "bold"), text_color="#ffffff").place(relx=0.5, rely=0.48, anchor="center")
        ctk.CTkLabel(overlay, text="ZEN MENU", font=("Consolas", 13), text_color="#a0a0a0").place(relx=0.5, rely=0.55, anchor="center")
        self.after(130, overlay.destroy)

    def page_header(self, parent, title, subtitle, row=0, column=0, columnspan=1):
        header = ctk.CTkFrame(
            parent,
            fg_color=self.colors["panel"],
            border_color=self.colors["line"],
            border_width=1,
            corner_radius=24
        )
        header.grid(row=row, column=column, columnspan=columnspan, padx=16, pady=(14, 10), sticky="ew")
        header.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            header,
            text=title,
            font=("Segoe UI Variable Display", 27, "bold"),
            text_color=self.colors["text"]
        ).grid(row=0, column=0, padx=22, pady=(16, 1), sticky="w")

        ctk.CTkLabel(
            header,
            text=subtitle,
            font=("Segoe UI Variable", 13),
            text_color=self.colors["muted"]
        ).grid(row=1, column=0, padx=22, pady=(0, 16), sticky="w")

        ctk.CTkLabel(
            header,
            text="ONLINE",
            font=("Segoe UI Variable", 10, "bold"),
            text_color=self.colors["text"],
            fg_color=self.colors["button"],
            corner_radius=12,
            padx=10,
            pady=4
        ).grid(row=0, column=1, rowspan=2, padx=18, pady=16, sticky="e")

        return header

    def card(self, parent, title, text, row, col, command=None):
        parent.grid_columnconfigure(col, weight=1)
        frame = ctk.CTkFrame(
            parent,
            fg_color=self.colors["panel"],
            border_color=self.colors["line"],
            border_width=1,
            corner_radius=20
        )
        frame.grid(row=row, column=col, padx=8, pady=8, sticky="nsew")
        frame.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            frame,
            text=title,
            font=("Segoe UI Variable Display", 17, "bold"),
            text_color=self.colors["text"],
            anchor="w"
        ).grid(row=0, column=0, padx=16, pady=(14, 3), sticky="ew")

        ctk.CTkLabel(
            frame,
            text=text,
            font=("Segoe UI Variable", 11),
            text_color=self.colors["muted"],
            wraplength=250,
            justify="left",
            anchor="w"
        ).grid(row=1, column=0, padx=16, pady=2, sticky="ew")

        if command:
            ctk.CTkButton(
                frame,
                text="Open",
                height=30,
                corner_radius=15,
                fg_color=self.colors["button"],
                text_color=self.colors["text"],
                hover_color=self.colors["button_hover"],
                border_width=1,
                border_color=self.colors["line"],
                font=("Segoe UI Variable", 11, "bold"),
                command=command
            ).grid(row=2, column=0, padx=16, pady=(9, 14), sticky="ew")
        return frame

    def textbox(self, parent, **kwargs):
        return ctk.CTkTextbox(
            parent,
            fg_color="#050507",
            text_color="#e8e8e8",
            font=("Cascadia Mono", 12),
            border_width=1,
            border_color=self.colors["line"],
            corner_radius=18,
            wrap="word",
            **kwargs
        )


    def info_card(self, parent, title, body, row, col, columnspan=1):
        frame = ctk.CTkFrame(
            parent,
            fg_color="#17181d",
            border_color="#30323a",
            border_width=1,
            corner_radius=28
        )
        frame.grid(row=row, column=col, columnspan=columnspan, padx=22, pady=14, sticky="nsew")
        frame.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            frame,
            text=title,
            font=("Segoe UI Variable Display", 24, "bold"),
            text_color="#ffffff"
        ).grid(row=0, column=0, padx=24, pady=(24, 6), sticky="w")

        ctk.CTkLabel(
            frame,
            text=body,
            font=("Segoe UI Variable", 14),
            text_color="#bfc1ca",
            justify="left",
            wraplength=520
        ).grid(row=1, column=0, padx=24, pady=(0, 24), sticky="w")

        return frame

    def link_button(self, parent, text, url):
        return ctk.CTkButton(
            parent,
            text=text,
            height=46,
            corner_radius=22,
            anchor="w",
            fg_color="#22242b",
            hover_color="#353842",
            text_color="#ffffff",
            border_width=1,
            border_color="#3a3d46",
            font=("Segoe UI Variable", 14, "bold"),
            command=lambda: webbrowser.open(url)
        )

    def set_entry_value(self, entry, value):
        entry.delete(0, "end")
        entry.insert(0, value)

    def button(self, parent, text, command=None):
        def wrapped_command():
            self.play_ui_sound("click")
            if command:
                command()

        return ctk.CTkButton(
            parent,
            text=text,
            height=34,
            corner_radius=16,
            fg_color=self.colors["button"],
            text_color=self.colors["text"],
            hover_color=self.colors["button_hover"],
            border_width=1,
            border_color=self.colors["line"],
            font=("Segoe UI Variable", 12, "bold"),
            command=wrapped_command
        )

    def textbox(self, parent, **kwargs):
        return ctk.CTkTextbox(
            parent,
            fg_color="#050507",
            text_color="#e8e8e8",
            font=("Cascadia Mono", 12),
            border_width=1,
            border_color=self.colors["line"],
            corner_radius=18,
            wrap="word",
            **kwargs
        )


    def info_card(self, parent, title, body, row, col, columnspan=1):
        frame = ctk.CTkFrame(
            parent,
            fg_color="#17181d",
            border_color="#30323a",
            border_width=1,
            corner_radius=28
        )
        frame.grid(row=row, column=col, columnspan=columnspan, padx=22, pady=14, sticky="nsew")
        frame.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            frame,
            text=title,
            font=("Segoe UI Variable Display", 24, "bold"),
            text_color="#ffffff"
        ).grid(row=0, column=0, padx=24, pady=(24, 6), sticky="w")

        ctk.CTkLabel(
            frame,
            text=body,
            font=("Segoe UI Variable", 14),
            text_color="#bfc1ca",
            justify="left",
            wraplength=520
        ).grid(row=1, column=0, padx=24, pady=(0, 24), sticky="w")

        return frame

    def link_button(self, parent, text, url):
        return ctk.CTkButton(
            parent,
            text=text,
            height=46,
            corner_radius=22,
            anchor="w",
            fg_color="#22242b",
            hover_color="#353842",
            text_color="#ffffff",
            border_width=1,
            border_color="#3a3d46",
            font=("Segoe UI Variable", 14, "bold"),
            command=lambda: webbrowser.open(url)
        )

    def set_entry_value(self, entry, value):
        entry.delete(0, "end")
        entry.insert(0, value)

    def button(self, parent, text, command=None):
        return ctk.CTkButton(
            parent,
            text=text,
            height=34,
            corner_radius=16,
            fg_color=self.colors["button"],
            text_color=self.colors["text"],
            hover_color=self.colors["button_hover"],
            border_width=1,
            border_color=self.colors["line"],
            font=("Segoe UI Variable", 12, "bold"),
            command=command
        )

    def _build_pages(self):
        self._build_dashboard()
        self._build_config_profiles()
        self._build_macro_builder()
        self._build_flow_builder()
        self._build_global_search()
        self._build_mini_apps()
        self._build_game_overlay()
        self._build_theme_preview()
        self._build_soundboard()
        self._build_level_system()
        self._build_usage_heatmap()
        self._build_time_tracker()
        self._build_text_tools()
        self._build_setup_wizard()
        self._build_command_palette()
        self._build_appearance_studio()
        self._build_help_center()
        self._build_whats_new()
        self._build_plugin_store()
        self._build_health()
        self._build_dependencies()
        self._build_safe_mode()
        self._build_terminal()
        self._build_environment()
        self._build_updates()
        self._build_changelog()
        self._build_plugins()
        self._build_duplicates()
        self._build_large_files()
        self._build_folder_sizes()
        self._build_fake_terminal()
        self._build_floating_widget()
        self._build_quick()
        self._build_startup()
        self._build_repair()
        self._build_performance()
        self._build_converters()
        self._build_image_tools()
        self._build_github()
        self._build_project_maker()
        self._build_error_analyzer()
        self._build_exe_builder()
        self._build_zenai_actions()
        self._build_music()
        self._build_uninstaller()
        self._build_settings()
        self._build_profiles()
        self._build_processes()
        self._build_internet()
        self._build_privacy()
        self._build_themes()
        self._build_passwords()
        self._build_zenai()
        self._build_cleaner()
        self._build_files()
        self._build_discord()
        self._build_automation()
        self._build_gaming()
        self._build_creator()
        self._build_credits()
        self._build_logs()

    def play_ui_sound(self, name="click"):
        try:
            if not self.config_data.get("ui_sounds", True):
                return
            sound_path = APP_DIR / "assets" / "sounds" / f"{name}.wav"
            if sound_path.exists():
                winsound.PlaySound(str(sound_path), winsound.SND_FILENAME | winsound.SND_ASYNC)
        except Exception:
            pass

    def toast(self, title, message="", kind="notification", duration=2600):
        self.play_ui_sound(kind if kind in ["click", "success", "error", "notification"] else "notification")
        try:
            toast = ctk.CTkFrame(
                self,
                fg_color="#0b0c10",
                border_width=1,
                border_color="#343740",
                corner_radius=18
            )
            toast.place(relx=1.0, rely=1.0, x=-22, y=-22, anchor="se")
            toast.lift()

            ctk.CTkLabel(
                toast,
                text=title,
                font=("Segoe UI Variable", 14, "bold"),
                text_color="#ffffff"
            ).grid(row=0, column=0, padx=18, pady=(14, 2), sticky="w")

            if message:
                ctk.CTkLabel(
                    toast,
                    text=message,
                    font=("Segoe UI Variable", 12),
                    text_color="#aeb2bf",
                    wraplength=330,
                    justify="left"
                ).grid(row=1, column=0, padx=18, pady=(0, 14), sticky="w")

            self.after(duration, toast.destroy)
        except Exception:
            pass

    def notify(self, title, message):
        ok = False
        try:
            ok = self.notifier.notify(title, message)
        except Exception:
            ok = False
        self.toast(title, message, "notification")
        if not ok:
            self.log(f"{title}: {message}")

    def open_focus_view(self):
        try:
            if self.sidebar.winfo_ismapped():
                self.sidebar.grid_remove()
                self.toast("Focus View", "Sidebar hidden. Press again to restore.", "success")
            else:
                self.sidebar.grid(row=0, column=0, sticky="nsw")
                self.toast("Focus View", "Sidebar restored.", "success")
        except Exception:
            pass

    def dashboard_columns(self):
        try:
            w = self.winfo_width()
            if w >= 1650:
                return 4
            if w >= 1280:
                return 2
            return 1
        except Exception:
            return 3

    def _build_dashboard(self):
        tab = self.frames["Dashboard"]
        tab.grid_columnconfigure(0, weight=1)
        tab.grid_rowconfigure(3, weight=1)

        # Dark hero banner with the user's ZEN banner asset.
        hero = ctk.CTkFrame(tab, fg_color="#050609", border_width=1, border_color="#242730", corner_radius=24)
        hero.grid(row=0, column=0, padx=16, pady=(14, 8), sticky="ew")
        hero.grid_columnconfigure(0, weight=1)

        banner_path = APP_DIR / "assets" / "banners" / "zen_banner.png"
        self.dashboard_banner_img = None
        if banner_path.exists():
            try:
                img = Image.open(banner_path)
                self.dashboard_banner_img = ctk.CTkImage(light_image=img, dark_image=img, size=(830, 210))
                ctk.CTkLabel(hero, image=self.dashboard_banner_img, text="").grid(row=0, column=0, columnspan=3, padx=14, pady=(14, 6), sticky="ew")
            except Exception:
                pass

        ctk.CTkLabel(
            hero,
            text="ZEN MENU",
            font=("Segoe UI Variable Display", 31, "bold"),
            text_color="#ffffff"
        ).grid(row=1, column=0, padx=22, pady=(4, 0), sticky="w")

        self.zenai_tip = ctk.CTkLabel(
            hero,
            text="ZENAI says: System online. Choose a module, search, or run a recommended action.",
            font=("Segoe UI Variable", 13),
            text_color="#aeb2bf"
        )
        self.zenai_tip.grid(row=2, column=0, padx=22, pady=(0, 16), sticky="w")

        hero_actions = ctk.CTkFrame(hero, fg_color="transparent")
        hero_actions.grid(row=1, column=1, rowspan=2, padx=18, pady=12, sticky="e")
        self.button(hero_actions, "Focus View", self.open_focus_view).pack(side="left", padx=4)
        self.button(hero_actions, "Setup", lambda: self.show_page("Setup Wizard")).pack(side="left", padx=4)
        self.button(hero_actions, "Help", lambda: self.show_page("Help")).pack(side="left", padx=4)

        controls = ctk.CTkFrame(tab, fg_color="transparent")
        controls.grid(row=1, column=0, padx=16, pady=4, sticky="ew")
        controls.grid_columnconfigure(1, weight=1)

        self.dashboard_mode = ctk.StringVar(value=self.config_data.get("dashboard", {}).get("mode", "Advanced"))
        self.dashboard_search = ctk.CTkEntry(controls, placeholder_text="Search modules...")
        self.dashboard_search.grid(row=0, column=0, padx=4, sticky="ew")
        self.dashboard_search.bind("<KeyRelease>", lambda _e: self.render_dashboard_page(reset_page=True))

        self.dashboard_page_label = ctk.CTkLabel(
            controls,
            text="",
            font=("Segoe UI Variable", 12, "bold"),
            text_color=self.colors["muted"]
        )
        self.dashboard_page_label.grid(row=0, column=1, padx=6)

        self.button(controls, "Simple", lambda: self.set_dashboard_mode("Simple")).grid(row=0, column=2, padx=4)
        self.button(controls, "Advanced", lambda: self.set_dashboard_mode("Advanced")).grid(row=0, column=3, padx=4)
        self.button(controls, "Previous", self.dashboard_prev_page).grid(row=0, column=4, padx=4)
        self.button(controls, "Next", self.dashboard_next_page).grid(row=0, column=5, padx=4)

        # Status cards
        status = ctk.CTkFrame(tab, fg_color="transparent")
        status.grid(row=2, column=0, padx=12, pady=(0, 4), sticky="ew")
        status.grid_columnconfigure((0, 1, 2, 3), weight=1)

        self.status_labels = []
        for i, name in enumerate(["FFmpeg", "Git", "Ollama", "Spotify"]):
            box = ctk.CTkFrame(status, fg_color="#0b0c10", border_width=1, border_color="#242730", corner_radius=18)
            box.grid(row=0, column=i, padx=5, pady=5, sticky="ew")
            lbl = ctk.CTkLabel(box, text=f"{name}: checking...", font=("Segoe UI Variable", 12, "bold"), text_color="#d8d9df")
            lbl.pack(anchor="w", padx=12, pady=10)
            self.status_labels.append((name, lbl))

        self.dashboard_content = ctk.CTkFrame(tab, fg_color=self.colors["panel2"], corner_radius=0)
        self.dashboard_content.grid(row=3, column=0, padx=10, pady=(0, 6), sticky="nsew")
        self.dashboard_content.grid_columnconfigure((0, 1, 2), weight=1, uniform="dashboard")

        self.dashboard_modules = [
            ("Setup Wizard", "◇", "First setup, checklist and quick configuration.", "simple"),
            ("Config Profiles", "♢", "Switch between saved configs.", "simple"),
            ("Macro Builder", "⛓", "Create simple no-code action chains.", "simple"),
            ("Flow Builder", "⌁", "Plan visual automation flows.", "advanced"),
            ("Global Search", "⌕", "Search modules, plugins, help and config.", "simple"),
            ("Mini Apps", "▱", "Open small tool windows.", "simple"),
            ("Game Overlay", "◫", "Always-on-top gaming overlay.", "advanced"),
            ("Theme Preview", "◐", "Preview UI themes before applying.", "simple"),
            ("Soundboard", "♫", "Play sounds and route them through a virtual mic setup.", "simple"),
            ("Level System", "LVL", "XP, levels and usage progression.", "simple"),
            ("Usage Heatmap", "▦", "See module usage counts visually.", "advanced"),
            ("Time Tracker", "◷", "Track how long the app/pages are used.", "advanced"),
            ("Text Tools", "T", "Transform text: case, slug, spaces and accents.", "simple"),
            ("Command", "⌘", "Search and launch actions quickly.", "simple"),
            ("Appearance", "◑", "Theme studio, skins and visual settings.", "simple"),
            ("Help", "?", "Guides for FFmpeg, Spotify, Ollama, plugins and EXE builds.", "simple"),
            ("Plugin Store", "☷", "View plugins as clean cards.", "simple"),
            ("Music", "♪", "Spotify player with synced lyrics.", "simple"),
            ("ZENAI", "✦", "Local AI assistant through Ollama.", "simple"),
            ("Cleaner", "🧹", "Junk and cache cleaner.", "simple"),
            ("Files", "📁", "Smart file search and screenshot organizer.", "simple"),
            ("Settings", "⚙", "Visual config editor and quick settings.", "simple"),
            ("Health", "✓", "Check config, assets, modules, Git, FFmpeg and Ollama.", "advanced"),
            ("Dependencies", "◇", "Repair pip, install requirements and inspect packages.", "advanced"),
            ("Safe Mode", "□", "Open the app with reduced startup behavior.", "advanced"),
            ("Terminal", ">", "Run CMD and Python commands inside ZEN.", "advanced"),
            ("Environment", "PATH", "View and edit user environment variables.", "advanced"),
            ("Updates", "↑", "Check GitHub or custom update endpoints.", "advanced"),
            ("Changelog", "≡", "View and edit the app changelog.", "advanced"),
            ("Plugins", "☷", "Load external plugin folders.", "advanced"),
            ("Duplicates", "◆", "Find duplicate files by hash.", "advanced"),
            ("Large Files", "⬢", "Find large files by size.", "advanced"),
            ("Folder Sizes", "▨", "Analyze folder sizes.", "advanced"),
            ("Fake Terminal", "▣", "Generate terminal-style PNG images.", "advanced"),
            ("Floating Widget", "◱", "Open a desktop widget with CPU/RAM/clock.", "advanced"),
            ("Quick", "▤", "Open apps, folders, links and copy shortcuts.", "advanced"),
            ("Startup", "↟", "Manage apps that start with Windows.", "advanced"),
            ("Repair", "◧", "Windows repair and maintenance commands.", "advanced"),
            ("Performance", "▥", "CPU, RAM, disk, uptime and top processes.", "advanced"),
            ("Converters", "⇄", "Advanced converters for images, TXT/PDF and video GIF.", "advanced"),
            ("Image Tools", "▧", "Resize, compress, remove metadata and create ICOs.", "advanced"),
            ("GitHub", "⌘", "Git commands, .gitignore and repo utilities.", "advanced"),
            ("Project Maker", "✚", "Create project structures and GitHub-ready folders.", "advanced"),
            ("Error Analyzer", "!", "Analyze Python, pip and PyInstaller errors.", "advanced"),
            ("EXE Builder", "▣", "Visual PyInstaller builder.", "advanced"),
            ("ZENAI Actions", "✦", "Apply safe config changes with action buttons.", "advanced"),
            ("Uninstaller", "✕", "Ultimate uninstaller and leftover cleaner.", "advanced"),
            ("Profiles", "◈", "Gaming, Coding, Study and custom modes.", "advanced"),
            ("Processes", "▦", "Advanced process manager.", "advanced"),
            ("Internet", "◎", "Ping, DNS, network and IP tools.", "advanced"),
            ("Privacy", "◌", "Clipboard, recent files and local privacy cleanup.", "advanced"),
            ("Themes", "◑", "Theme presets that apply after restart.", "advanced"),
            ("Passwords", "◆", "Strong password generator.", "advanced"),
            ("Discord", "●", "Discord/Spotify Rich Presence.", "advanced"),
            ("Automation", "⚡", "Hotkeys, text expander and safe auto-clicker.", "advanced"),
            ("Gaming", "▶", "Game sessions and volume info.", "advanced"),
            ("Creator", "✎", "README generator and creator tools.", "advanced"),
            ("Credits", "★", "Contact and project credits.", "advanced"),
            ("Logs", "▣", "Runtime logs.", "advanced")
        ]

        self.dashboard_page = 0
        self.after(350, self.refresh_status_cards)
        self.render_dashboard_page(reset_page=True)

    def set_dashboard_mode(self, mode):
        self.dashboard_mode.set(mode)
        self.dashboard_page = 0
        self.toast("Dashboard mode", f"{mode} mode enabled.", "success")
        self.render_dashboard_page(reset_page=True)

    def filtered_dashboard_modules(self):
        query = ""
        try:
            query = self.dashboard_search.get().strip().lower()
        except Exception:
            pass

        mode = self.dashboard_mode.get()
        modules = []
        for page, icon, desc, level in self.dashboard_modules:
            if mode == "Simple" and level != "simple":
                continue
            if query and query not in page.lower() and query not in desc.lower():
                continue
            modules.append((page, icon, desc, level))
        return modules

    def dashboard_page_size(self):
        try:
            h = self.winfo_height()
            if h >= 850:
                return 9
            if h >= 720:
                return 6
            return 4
        except Exception:
            return 6

    def render_dashboard_page(self, reset_page=False):
        for child in self.dashboard_content.winfo_children():
            child.destroy()

        if reset_page:
            self.dashboard_page = 0

        cols = 3 if self.winfo_width() >= 1250 else 2
        for c in range(3):
            self.dashboard_content.grid_columnconfigure(c, weight=1 if c < cols else 0, uniform="dashboard")

        modules = self.filtered_dashboard_modules()
        page_size = self.dashboard_page_size()
        total_pages = max(1, (len(modules) + page_size - 1) // page_size)
        self.dashboard_page = max(0, min(self.dashboard_page, total_pages - 1))

        start = self.dashboard_page * page_size
        visible = modules[start:start + page_size]

        for i, (page, icon, desc, _level) in enumerate(visible):
            row = i // cols
            col = i % cols
            self.card(self.dashboard_content, f"{icon}  {page}", desc, row, col, lambda p=page: self.show_page(p))

        if not visible:
            ctk.CTkLabel(
                self.dashboard_content,
                text="No modules found.",
                font=("Segoe UI Variable", 16, "bold"),
                text_color=self.colors["muted"]
            ).grid(row=0, column=0, padx=18, pady=18, sticky="w")

        self.dashboard_page_label.configure(text=f"{self.dashboard_mode.get()} • page {self.dashboard_page + 1} / {total_pages}")

    def dashboard_next_page(self):
        self.dashboard_page += 1
        self.render_dashboard_page()

    def dashboard_prev_page(self):
        self.dashboard_page -= 1
        self.render_dashboard_page()

    def refresh_status_cards(self):
        try:
            import shutil as _shutil
            values = {
                "FFmpeg": "✓ Installed" if _shutil.which("ffmpeg") else "✕ Missing",
                "Git": "✓ Installed" if _shutil.which("git") else "✕ Missing",
                "Ollama": "✓ Installed" if _shutil.which("ollama") else "✕ Missing",
                "Spotify": "✓ Enabled" if self.config_data.get("discord", {}).get("spotify", {}).get("enabled") else "OFF"
            }
            for name, label in self.status_labels:
                label.configure(text=f"{name}: {values.get(name, '--')}")
        except Exception:
            pass


    def _build_config_profiles(self):
        tab = self.frames["Config Profiles"]
        tab.grid_columnconfigure(0, weight=1)
        self.page_header(tab, "Config Profiles", "Save, load and switch between multiple config.json profiles.", 0, 0)
        row = ctk.CTkFrame(tab, fg_color="transparent")
        row.grid(row=1, column=0, padx=18, pady=8, sticky="ew")
        self.profile_name_entry = ctk.CTkEntry(row, placeholder_text="Profile name, example: gaming")
        self.profile_name_entry.pack(side="left", fill="x", expand=True, padx=5)
        self.button(row, "Save Current", self.save_config_profile).pack(side="left", padx=5)
        self.button(row, "Load Profile", self.load_config_profile).pack(side="left", padx=5)
        self.button(row, "List Profiles", self.list_config_profiles).pack(side="left", padx=5)
        self.config_profiles_output = self.textbox(tab, height=520)
        self.config_profiles_output.grid(row=2, column=0, padx=18, pady=10, sticky="nsew")

    def config_profiles_dir(self):
        path = APP_DIR / "config_profiles"
        path.mkdir(exist_ok=True)
        return path

    def save_config_profile(self):
        name = self.profile_name_entry.get().strip() or "profile"
        safe = "".join(c for c in name if c.isalnum() or c in "_-").strip() or "profile"
        dst = self.config_profiles_dir() / f"{safe}.json"
        shutil.copy2(CONFIG_PATH, dst)
        self.config_profiles_output.insert("end", f"Saved: {dst}\n")
        self.toast("Config profile saved", safe, "success")

    def load_config_profile(self):
        name = self.profile_name_entry.get().strip()
        path = self.config_profiles_dir() / f"{name}.json"
        if not path.exists():
            self.config_profiles_output.insert("end", "Profile not found. Use List Profiles.\n")
            return
        if messagebox.askyesno("Config Profiles", f"Replace current config.json with {name}.json?"):
            shutil.copy2(path, CONFIG_PATH)
            self.config_profiles_output.insert("end", f"Loaded: {path}\nRestart the app to fully apply.\n")
            self.toast("Config profile loaded", "Restart recommended.", "success")

    def list_config_profiles(self):
        self.config_profiles_output.delete("1.0", "end")
        for p in self.config_profiles_dir().glob("*.json"):
            self.config_profiles_output.insert("end", p.name + "\n")

    def _build_macro_builder(self):
        tab = self.frames["Macro Builder"]
        tab.grid_columnconfigure(0, weight=1)
        self.page_header(tab, "ZEN Macro Builder", "Create simple no-code action chains and run them.", 0, 0)
        row = ctk.CTkFrame(tab, fg_color="transparent")
        row.grid(row=1, column=0, padx=18, pady=8, sticky="ew")
        self.macro_action = ctk.CTkOptionMenu(row, values=["open_url", "open_folder", "run_command", "wait", "notify"])
        self.macro_action.pack(side="left", padx=5)
        self.macro_value = ctk.CTkEntry(row, placeholder_text="Action value")
        self.macro_value.pack(side="left", fill="x", expand=True, padx=5)
        self.button(row, "Add Step", self.add_macro_step).pack(side="left", padx=5)
        self.button(row, "Run Macro", self.run_macro_steps).pack(side="left", padx=5)
        self.macro_output = self.textbox(tab, height=520)
        self.macro_output.grid(row=2, column=0, padx=18, pady=10, sticky="nsew")
        self.current_macro_steps = []

    def add_macro_step(self):
        step = {"action": self.macro_action.get(), "value": self.macro_value.get().strip()}
        self.current_macro_steps.append(step)
        self.macro_output.insert("end", f"Added: {step}\n")

    def run_macro_steps(self):
        def job():
            for step in self.current_macro_steps:
                action = step["action"]
                value = os.path.expandvars(step["value"])
                self.macro_output.insert("end", f"> {action}: {value}\n")
                try:
                    if action == "open_url":
                        webbrowser.open(value)
                    elif action == "open_folder":
                        os.startfile(value)
                    elif action == "run_command":
                        out = subprocess.run(value, shell=True, capture_output=True, text=True)
                        self.macro_output.insert("end", (out.stdout or out.stderr) + "\n")
                    elif action == "wait":
                        time.sleep(float(value or "1"))
                    elif action == "notify":
                        self.toast("Macro", value, "notification")
                except Exception as e:
                    self.macro_output.insert("end", f"Error: {e}\n")
            self.toast("Macro finished", f"{len(self.current_macro_steps)} steps executed.", "success")
        self.run_thread(job)

    def _build_flow_builder(self):
        tab = self.frames["Flow Builder"]
        tab.grid_columnconfigure(0, weight=1)
        self.page_header(tab, "ZEN Visual Flow Builder", "Plan automation flows as readable blocks.", 0, 0)
        row = ctk.CTkFrame(tab, fg_color="transparent")
        row.grid(row=1, column=0, padx=18, pady=8, sticky="ew")
        self.flow_block = ctk.CTkOptionMenu(row, values=["Start", "Open App", "Open URL", "Wait", "Run Command", "Notify", "End"])
        self.flow_block.pack(side="left", padx=5)
        self.flow_value = ctk.CTkEntry(row, placeholder_text="Block value")
        self.flow_value.pack(side="left", fill="x", expand=True, padx=5)
        self.button(row, "Add Block", self.add_flow_block).pack(side="left", padx=5)
        self.button(row, "Export Flow", self.export_flow).pack(side="left", padx=5)
        self.flow_output = self.textbox(tab, height=520)
        self.flow_output.grid(row=2, column=0, padx=18, pady=10, sticky="nsew")
        self.flow_blocks = []

    def add_flow_block(self):
        block = f"[{self.flow_block.get()}] {self.flow_value.get().strip()}"
        self.flow_blocks.append(block)
        self.flow_output.insert("end", block + "\n   ↓\n")

    def export_flow(self):
        dst = filedialog.asksaveasfilename(defaultextension=".txt", initialfile="zen_flow.txt")
        if dst:
            Path(dst).write_text("\n↓\n".join(self.flow_blocks), encoding="utf-8")
            self.toast("Flow exported", dst, "success")

    def _build_global_search(self):
        tab = self.frames["Global Search"]
        tab.grid_columnconfigure(0, weight=1)
        self.page_header(tab, "ZEN Global Search", "Search modules, plugins, help text and config keys.", 0, 0)
        self.global_search_entry = ctk.CTkEntry(tab, placeholder_text="Search anything...")
        self.global_search_entry.grid(row=1, column=0, padx=18, pady=8, sticky="ew")
        self.global_search_entry.bind("<KeyRelease>", lambda _e: self.run_global_search())
        self.global_search_output = self.textbox(tab, height=520)
        self.global_search_output.grid(row=2, column=0, padx=18, pady=10, sticky="nsew")

    def run_global_search(self):
        q = self.global_search_entry.get().strip().lower()
        self.global_search_output.delete("1.0", "end")
        if not q:
            return
        self.global_search_output.insert("end", "MODULES\n")
        for page, icon, desc, _level in getattr(self, "dashboard_modules", []):
            if q in page.lower() or q in desc.lower():
                self.global_search_output.insert("end", f"{icon} {page} - {desc}\n")
        self.global_search_output.insert("end", "\nPLUGINS\n")
        try:
            for plugin in self.plugin_system.list_plugins():
                blob = f"{plugin.get('name','')} {plugin.get('description','')}".lower()
                if q in blob:
                    self.global_search_output.insert("end", f"{plugin.get('name')} - {plugin.get('description')}\n")
        except Exception:
            pass
        self.global_search_output.insert("end", "\nCONFIG KEYS\n")
        def scan_dict(d, prefix=""):
            for k, v in d.items():
                path = f"{prefix}.{k}" if prefix else str(k)
                if q in path.lower():
                    self.global_search_output.insert("end", path + "\n")
                if isinstance(v, dict):
                    scan_dict(v, path)
        try:
            scan_dict(self.config_data)
        except Exception:
            pass

    def _build_mini_apps(self):
        tab = self.frames["Mini Apps"]
        tab.grid_columnconfigure((0, 1, 2), weight=1)
        self.page_header(tab, "ZEN Mini Apps", "Small floating windows for quick tools.", 0, 0, 3)
        self.card(tab, "Mini System Monitor", "CPU/RAM floating widget.", 1, 0, self.floating_widget.show)
        self.card(tab, "Mini Notes", "A small always-on-top note window.", 1, 1, self.open_mini_notes)
        self.card(tab, "Mini Clock", "A small always-on-top clock.", 1, 2, self.open_mini_clock)

    def open_mini_notes(self):
        win = ctk.CTkToplevel(self)
        win.title("ZEN Mini Notes")
        win.geometry("320x260")
        win.attributes("-topmost", True)
        box = self.textbox(win, height=220)
        box.pack(fill="both", expand=True, padx=10, pady=10)

    def open_mini_clock(self):
        win = ctk.CTkToplevel(self)
        win.title("ZEN Clock")
        win.geometry("260x120")
        win.attributes("-topmost", True)
        lbl = ctk.CTkLabel(win, text="", font=("Consolas", 28, "bold"))
        lbl.pack(expand=True)
        def tick():
            if win.winfo_exists():
                lbl.configure(text=time.strftime("%H:%M:%S"))
                win.after(1000, tick)
        tick()

    def _build_game_overlay(self):
        tab = self.frames["Game Overlay"]
        tab.grid_columnconfigure(0, weight=1)
        self.page_header(tab, "ZEN Game Overlay", "Always-on-top overlay for time, CPU, RAM and quick status.", 0, 0)
        self.card(tab, "Open Game Overlay", "Creates a compact topmost overlay. It is not injected into games.", 1, 0, self.open_game_overlay)

    def open_game_overlay(self):
        win = ctk.CTkToplevel(self)
        win.title("ZEN Game Overlay")
        win.geometry("330x160+60+60")
        win.attributes("-topmost", True)
        win.configure(fg_color="#020203")
        lbl = ctk.CTkLabel(win, text="", font=("Consolas", 14, "bold"), justify="left")
        lbl.pack(fill="both", expand=True, padx=18, pady=18)
        def update():
            if win.winfo_exists():
                lbl.configure(text=f"ZEN OVERLAY\nTIME: {time.strftime('%H:%M:%S')}\nCPU: {psutil.cpu_percent()}%\nRAM: {psutil.virtual_memory().percent}%")
                win.after(1000, update)
        update()

    def _build_theme_preview(self):
        tab = self.frames["Theme Preview"]
        tab.grid_columnconfigure((0, 1, 2), weight=1)
        self.page_header(tab, "ZEN Theme Preview", "Preview how cards, buttons and textboxes look before applying.", 0, 0, 3)
        self.card(tab, "Header Preview", "This is how module cards look with the current skin.", 1, 0, lambda: None)
        sample = ctk.CTkFrame(tab, fg_color=self.colors["panel"], border_width=1, border_color=self.colors["line"], corner_radius=20)
        sample.grid(row=1, column=1, padx=12, pady=12, sticky="nsew")
        ctk.CTkLabel(sample, text="Button Preview", font=("Segoe UI Variable", 17, "bold")).pack(padx=18, pady=14)
        self.button(sample, "Sample Button", lambda: self.toast("Preview", "Theme preview button.", "success")).pack(fill="x", padx=18, pady=8)
        box = self.textbox(tab, height=180)
        box.grid(row=1, column=2, padx=12, pady=12, sticky="nsew")
        box.insert("end", "Textbox preview\n[OK] ZEN theme loaded\n[READY] Cyber Black")

    def _build_soundboard(self):
        tab = self.frames["Soundboard"]
        tab.grid_columnconfigure(0, weight=1)
        self.page_header(tab, "ZEN Soundboard", "Play sounds. For microphone use, route output through VB-CABLE/virtual audio cable.", 0, 0)

        info = ctk.CTkLabel(
            tab,
            text="Mic mode guide: install VB-CABLE, set Windows output to CABLE Input, set Discord/voice chat input to CABLE Output, then play sounds here.",
            font=("Segoe UI Variable", 13),
            text_color=self.colors["muted"],
            wraplength=900,
            justify="left"
        )
        info.grid(row=1, column=0, padx=18, pady=6, sticky="w")

        grid = ctk.CTkFrame(tab, fg_color="transparent")
        grid.grid(row=2, column=0, padx=12, pady=10, sticky="ew")
        grid.grid_columnconfigure((0, 1, 2, 3), weight=1)

        self.soundboard_files = list((APP_DIR / "assets" / "sounds").glob("*.wav"))
        for i, sound in enumerate(self.soundboard_files):
            self.card(grid, sound.name, "Play this sound through the selected/default output.", i // 4, i % 4, lambda s=sound: self.play_soundboard(s))

    def play_soundboard(self, path):
        try:
            winsound.PlaySound(str(path), winsound.SND_FILENAME | winsound.SND_ASYNC)
            self.toast("Soundboard", f"Playing {path.name}", "success")
        except Exception as e:
            self.toast("Soundboard error", str(e), "error")

    def _build_level_system(self):
        tab = self.frames["Level System"]
        tab.grid_columnconfigure(0, weight=1)
        self.page_header(tab, "ZEN Level System", "XP and level based on app usage.", 0, 0)
        self.level_output = self.textbox(tab, height=520)
        self.level_output.grid(row=1, column=0, padx=18, pady=10, sticky="nsew")
        usage = self.config_data.get("usage", {})
        xp = int(usage.get("xp", 0))
        level = max(1, xp // 100 + 1)
        self.level_output.insert("end", f"Level: {level}\nXP: {xp}\nRank: {'ZEN Operator' if level >= 10 else 'Power User' if level >= 5 else 'New User'}\n\nUse modules to gain XP in future builds.")

    def _build_usage_heatmap(self):
        tab = self.frames["Usage Heatmap"]
        tab.grid_columnconfigure(0, weight=1)
        self.page_header(tab, "ZEN Usage Heatmap", "Visual usage counts for modules.", 0, 0)
        out = self.textbox(tab, height=560)
        out.grid(row=1, column=0, padx=18, pady=10, sticky="nsew")
        usage = self.config_data.get("usage", {}).get("modules", {
            "Cleaner": 12, "Plugins": 9, "Music": 7, "ZENAI": 5, "Settings": 4
        })
        for name, count in sorted(usage.items(), key=lambda x: x[1], reverse=True):
            out.insert("end", f"{name:<18} {'█' * min(30, int(count))} {count}\n")

    def _build_time_tracker(self):
        tab = self.frames["Time Tracker"]
        tab.grid_columnconfigure(0, weight=1)
        self.page_header(tab, "ZEN Time Tracker", "Track current session time and app uptime.", 0, 0)
        self.time_tracker_output = self.textbox(tab, height=520)
        self.time_tracker_output.grid(row=1, column=0, padx=18, pady=10, sticky="nsew")
        self.session_start_time = getattr(self, "session_start_time", time.time())
        self.update_time_tracker()

    def update_time_tracker(self):
        if not hasattr(self, "time_tracker_output"):
            return
        elapsed = int(time.time() - self.session_start_time)
        self.time_tracker_output.delete("1.0", "end")
        self.time_tracker_output.insert("end", f"ZEN open this session: {elapsed//3600:02d}:{(elapsed%3600)//60:02d}:{elapsed%60:02d}\nActive page: {getattr(self, 'active_page', 'Dashboard')}\n")
        self.after(1000, self.update_time_tracker)

    def _build_text_tools(self):
        tab = self.frames["Text Tools"]
        tab.grid_columnconfigure(0, weight=1)
        self.page_header(tab, "ZEN Text Transformer", "Transform text: uppercase, lowercase, title, snake, kebab, remove accents.", 0, 0)
        self.text_tools_input = self.textbox(tab, height=220)
        self.text_tools_input.grid(row=1, column=0, padx=18, pady=8, sticky="ew")
        row = ctk.CTkFrame(tab, fg_color="transparent")
        row.grid(row=2, column=0, padx=18, pady=6, sticky="ew")
        for name in ["UPPERCASE", "lowercase", "Title Case", "snake_case", "kebab-case", "remove accents"]:
            self.button(row, name, lambda n=name: self.transform_text(n)).pack(side="left", padx=4)
        self.text_tools_output = self.textbox(tab, height=260)
        self.text_tools_output.grid(row=3, column=0, padx=18, pady=10, sticky="nsew")

    def transform_text(self, mode):
        import unicodedata
        text = self.text_tools_input.get("1.0", "end").strip()
        if mode == "UPPERCASE":
            out = text.upper()
        elif mode == "lowercase":
            out = text.lower()
        elif mode == "Title Case":
            out = text.title()
        elif mode == "snake_case":
            out = "_".join(text.lower().split())
        elif mode == "kebab-case":
            out = "-".join(text.lower().split())
        else:
            out = "".join(c for c in unicodedata.normalize("NFD", text) if unicodedata.category(c) != "Mn")
        self.text_tools_output.delete("1.0", "end")
        self.text_tools_output.insert("end", out)
        pyperclip.copy(out)
        self.toast("Text transformed", "Output copied to clipboard.", "success")


    def _build_setup_wizard(self):
        tab = self.frames["Setup Wizard"]
        tab.grid_columnconfigure(0, weight=1)
        self.page_header(tab, "First Setup Wizard", "Configure the app without digging through config.json.", 0, 0)

        body = ctk.CTkFrame(tab, fg_color=self.colors["panel"], border_width=1, border_color=self.colors["line"], corner_radius=24)
        body.grid(row=1, column=0, padx=18, pady=10, sticky="nsew")
        body.grid_columnconfigure((0, 1), weight=1)

        checklist = [
            ("config.json", CONFIG_PATH.exists()),
            ("assets folder", (APP_DIR / "assets").exists()),
            ("FFmpeg installed", shutil.which("ffmpeg") is not None),
            ("Git installed", shutil.which("git") is not None),
            ("Ollama installed", shutil.which("ollama") is not None),
            ("Spotify enabled", self.config_data.get("discord", {}).get("spotify", {}).get("enabled", False)),
        ]

        ctk.CTkLabel(body, text="Setup Checklist", font=("Segoe UI Variable Display", 24, "bold"), text_color=self.colors["text"]).grid(row=0, column=0, padx=20, pady=(20, 10), sticky="w")
        for i, (name, ok) in enumerate(checklist, start=1):
            ctk.CTkLabel(
                body,
                text=f"{'✓' if ok else '✕'}  {name}",
                font=("Segoe UI Variable", 14, "bold"),
                text_color="#ffffff" if ok else "#b9bbc4"
            ).grid(row=i, column=0, padx=22, pady=5, sticky="w")

        quick = ctk.CTkFrame(body, fg_color="#050609", border_width=1, border_color=self.colors["line"], corner_radius=20)
        quick.grid(row=0, column=1, rowspan=8, padx=20, pady=20, sticky="nsew")
        quick.grid_columnconfigure(0, weight=1)
        ctk.CTkLabel(quick, text="Quick Actions", font=("Segoe UI Variable Display", 22, "bold")).grid(row=0, column=0, padx=18, pady=(18, 8), sticky="w")
        self.button(quick, "Open Settings", lambda: self.show_page("Settings")).grid(row=1, column=0, padx=18, pady=6, sticky="ew")
        self.button(quick, "Open Appearance", lambda: self.show_page("Appearance")).grid(row=2, column=0, padx=18, pady=6, sticky="ew")
        self.button(quick, "Open Help Center", lambda: self.show_page("Help")).grid(row=3, column=0, padx=18, pady=6, sticky="ew")
        self.button(quick, "Run Health Check", lambda: self.show_page("Health")).grid(row=4, column=0, padx=18, pady=6, sticky="ew")

    def _build_command_palette(self):
        tab = self.frames["Command"]
        tab.grid_columnconfigure(0, weight=1)
        self.page_header(tab, "ZEN Command Palette", "Type a module name or action and launch it fast.", 0, 0)

        self.command_entry = ctk.CTkEntry(tab, placeholder_text="Example: music, plugins, cleaner, ffmpeg, build exe...")
        self.command_entry.grid(row=1, column=0, padx=18, pady=8, sticky="ew")
        self.command_entry.bind("<KeyRelease>", lambda _e: self.update_command_results())

        self.command_output = self.textbox(tab, height=520)
        self.command_output.grid(row=2, column=0, padx=18, pady=10, sticky="nsew")
        self.update_command_results()

    def update_command_results(self):
        query = self.command_entry.get().strip().lower() if hasattr(self, "command_entry") else ""
        self.command_output.delete("1.0", "end")
        matches = []
        for page, icon, desc, _level in getattr(self, "dashboard_modules", []):
            if not query or query in page.lower() or query in desc.lower():
                matches.append((page, icon, desc))
        for page, icon, desc in matches[:25]:
            self.command_output.insert("end", f"{icon} {page} - {desc}\n")
        self.command_output.insert("end", "\nType exact module name and press Open Match.\n")
        if not hasattr(self, "command_open_button"):
            self.command_open_button = self.button(self.frames["Command"], "Open Match", self.open_command_match)
            self.command_open_button.grid(row=3, column=0, padx=18, pady=5, sticky="w")

    def open_command_match(self):
        query = self.command_entry.get().strip().lower()
        for page, _icon, desc, _level in getattr(self, "dashboard_modules", []):
            if query and (query == page.lower() or query in page.lower() or query in desc.lower()):
                self.show_page(page)
                return
        self.toast("Command Palette", "No match found.", "error")

    def _build_appearance_studio(self):
        tab = self.frames["Appearance"]
        tab.grid_columnconfigure(0, weight=1)
        self.page_header(tab, "Appearance Studio", "Change skins, sounds, banners, compact mode and dark theme settings.", 0, 0)

        grid = ctk.CTkFrame(tab, fg_color="transparent")
        grid.grid(row=1, column=0, padx=12, pady=10, sticky="ew")
        grid.grid_columnconfigure((0, 1, 2), weight=1)

        self.card(grid, "Cyber Black Skin", "Ultra-dark ZEN interface with metallic banner.", 0, 0, lambda: self.apply_skin("Cyber Black"))
        self.card(grid, "Compact Mode", "Smaller spacing and card density for 1366x768.", 0, 1, lambda: self.apply_skin("Compact"))
        self.card(grid, "Sound Test", "Play click, success, error and notification sounds.", 0, 2, self.test_ui_sounds)
        self.card(grid, "Skin Manager", "Replace logo, icon, banner and startup sound.", 1, 0, lambda: self.show_page("Plugin Store"))
        self.card(grid, "Theme Presets", "Open the classic Themes page.", 1, 1, lambda: self.show_page("Themes"))
        self.card(grid, "Focus View", "Hide or restore the sidebar.", 1, 2, self.open_focus_view)

    def apply_skin(self, name):
        try:
            data = self.config_editor.load_json()
            data.setdefault("appearance", {})["skin"] = name
            data.setdefault("dashboard", {})["compact"] = name == "Compact"
            CONFIG_PATH.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
            self.toast("Appearance saved", f"{name} will remain in config.json.", "success")
        except Exception as e:
            self.toast("Appearance error", str(e), "error")

    def test_ui_sounds(self):
        self.play_ui_sound("click")
        self.after(350, lambda: self.play_ui_sound("success"))
        self.after(700, lambda: self.play_ui_sound("notification"))
        self.after(1050, lambda: self.play_ui_sound("error"))

    def _build_help_center(self):
        tab = self.frames["Help"]
        tab.grid_columnconfigure(0, weight=1)
        self.page_header(tab, "Help Center", "Quick guides for common setup tasks.", 0, 0)

        self.help_output = self.textbox(tab, height=570)
        self.help_output.grid(row=1, column=0, padx=18, pady=10, sticky="nsew")
        self.help_output.insert("end", """ZEN HELP CENTER

FFmpeg:
1. Download ffmpeg-release-essentials.zip from gyan.dev.
2. Extract to C:\\ffmpeg.
3. Add C:\\ffmpeg\\bin to PATH.
4. Test: ffmpeg -version.

Ollama / ZENAI:
1. Install Ollama.
2. Run: ollama pull llama3.1.
3. Keep zenai.provider = ollama in config.json.

Spotify:
1. Create Spotify Developer app.
2. Redirect URI: http://127.0.0.1:8888/callback
3. Put Client ID and Secret in Settings.

Plugins:
1. Go to Plugins or Plugin Store.
2. Click List Plugins.
3. Type plugin name.
4. Run Plugin.

Build EXE:
1. Run build_exe.bat.
2. Use app.ico in assets/icons/app.ico.
3. Keep assets and config.json near the EXE.
""")

    def _build_whats_new(self):
        tab = self.frames["What's New"]
        tab.grid_columnconfigure(0, weight=1)
        self.page_header(tab, "What's New", "Recent changes and update notes.", 0, 0)
        out = self.textbox(tab, height=570)
        out.grid(row=1, column=0, padx=18, pady=10, sticky="nsew")
        out.insert("end", """ZEN MENU - What's New

- Darker UI skin.
- Hero banner on Dashboard.
- Banner assets included in assets/banners.
- UI sounds: click, success, error and notification.
- Internal toast notifications.
- Simple / Advanced Dashboard mode.
- Search modules on Dashboard.
- Command Palette.
- Setup Wizard.
- Help Center.
- Appearance Studio.
- Plugin Store-style page.
- Status cards for FFmpeg, Git, Ollama and Spotify.
- ZENAI guidance text on Dashboard.
""")

    def _build_plugin_store(self):
        tab = self.frames["Plugin Store"]
        tab.grid_columnconfigure((0, 1, 2), weight=1)
        self.page_header(tab, "Plugin Store", "Installed plugins presented as cards.", 0, 0, 3)

        try:
            plugins = self.plugin_system.list_plugins()
        except Exception:
            plugins = []

        if not plugins:
            self.card(tab, "No plugins found", "Open the Plugins page and create an example plugin.", 1, 0, lambda: self.show_page("Plugins"))
            return

        for i, plugin in enumerate(plugins[:18]):
            row = 1 + i // 3
            col = i % 3
            name = plugin.get("name", "Plugin")
            desc = plugin.get("description", "No description.")
            self.card(tab, name, desc, row, col, lambda p=plugin: self.run_plugin_from_store(p))

    def run_plugin_from_store(self, plugin):
        try:
            result = self.plugin_system.run_plugin(plugin)
            self.toast("Plugin started", result, "success")
        except Exception as e:
            self.toast("Plugin error", str(e), "error")


    def _build_health(self):
        tab = self.frames["Health"]
        tab.grid_columnconfigure(0, weight=1)
        self.page_header(tab, "App Health Checker", "Checks if ZEN files, modules and external tools are installed.", 0, 0)
        self.button(tab, "Run Health Check", self.run_health_check).grid(row=1, column=0, padx=18, pady=8, sticky="w")
        self.health_output = self.textbox(tab, height=540)
        self.health_output.grid(row=2, column=0, padx=18, pady=10, sticky="nsew")

    def run_health_check(self):
        self.health_output.delete("1.0", "end")
        for status, name, detail in self.app_health_checker.check():
            self.health_output.insert("end", f"[{status:<4}] {name} - {detail}\n")

    def _build_dependencies(self):
        tab = self.frames["Dependencies"]
        tab.grid_columnconfigure(0, weight=1)
        self.page_header(tab, "Dependency Doctor", "Fix pip, install requirements and inspect installed packages.", 0, 0)
        row = ctk.CTkFrame(tab, fg_color="transparent")
        row.grid(row=1, column=0, padx=18, pady=8, sticky="ew")
        self.button(row, "Upgrade pip", lambda: self.run_dependency_job(self.dependency_doctor.upgrade_pip)).pack(side="left", padx=5)
        self.button(row, "Install requirements", lambda: self.run_dependency_job(lambda: self.dependency_doctor.install_requirements(APP_DIR))).pack(side="left", padx=5)
        self.button(row, "pip check", lambda: self.run_dependency_job(self.dependency_doctor.pip_check)).pack(side="left", padx=5)
        self.button(row, "pip list", lambda: self.run_dependency_job(self.dependency_doctor.pip_list)).pack(side="left", padx=5)
        self.button(row, "Clear pip cache", lambda: self.run_dependency_job(self.dependency_doctor.clear_cache)).pack(side="left", padx=5)
        self.button(row, "Export requirements", lambda: self.run_dependency_job(lambda: self.dependency_doctor.export_requirements(APP_DIR))).pack(side="left", padx=5)
        self.dependencies_output = self.textbox(tab, height=520)
        self.dependencies_output.grid(row=2, column=0, padx=18, pady=10, sticky="nsew")

    def run_dependency_job(self, fn):
        def job():
            self.dependencies_output.insert("end", fn() + "\n")
            self.dependencies_output.see("end")
        self.run_thread(job)

    def _build_safe_mode(self):
        tab = self.frames["Safe Mode"]
        tab.grid_columnconfigure(0, weight=1)
        self.page_header(tab, "ZEN Safe Mode", "Use --safe to open ZEN with reduced startup behavior.", 0, 0)
        self.safe_output = self.textbox(tab, height=520)
        self.safe_output.grid(row=1, column=0, padx=18, pady=10, sticky="nsew")
        self.safe_output.insert("end", self.safe_mode.status() + "\n\nLaunch examples:\nZEN MENU.exe --safe\npython main.py --safe\n")

    def _build_terminal(self):
        tab = self.frames["Terminal"]
        tab.grid_columnconfigure(0, weight=1)
        self.page_header(tab, "ZEN Mini Terminal", "Run CMD or Python snippets inside the app.", 0, 0)
        self.term_input = self.textbox(tab, height=120)
        self.term_input.grid(row=1, column=0, padx=18, pady=8, sticky="ew")
        row = ctk.CTkFrame(tab, fg_color="transparent")
        row.grid(row=2, column=0, padx=18, pady=4, sticky="ew")
        self.button(row, "Run CMD", self.run_terminal_cmd).pack(side="left", padx=5)
        self.button(row, "Run Python", self.run_terminal_python).pack(side="left", padx=5)
        for cmd in ["ipconfig", "git status", "python --version", "pip list", "ollama list"]:
            self.button(row, cmd, lambda c=cmd: self.terminal_preset(c)).pack(side="left", padx=3)
        self.term_output = self.textbox(tab, height=390)
        self.term_output.grid(row=3, column=0, padx=18, pady=10, sticky="nsew")

    def terminal_preset(self, cmd):
        self.term_input.delete("1.0", "end")
        self.term_input.insert("end", cmd)
        self.run_terminal_cmd()

    def run_terminal_cmd(self):
        cmd = self.term_input.get("1.0", "end").strip()
        def job():
            self.term_output.insert("end", f"> {cmd}\n")
            self.term_output.insert("end", self.mini_terminal.run_cmd(cmd) + "\n")
            self.term_output.see("end")
        self.run_thread(job)

    def run_terminal_python(self):
        code = self.term_input.get("1.0", "end").strip()
        def job():
            self.term_output.insert("end", ">>> python snippet\n")
            self.term_output.insert("end", self.mini_terminal.run_python(code) + "\n")
            self.term_output.see("end")
        self.run_thread(job)

    def _build_environment(self):
        tab = self.frames["Environment"]
        tab.grid_columnconfigure(0, weight=1)
        self.page_header(tab, "Environment Variables Editor", "View user variables and add folders to PATH.", 0, 0)
        row = ctk.CTkFrame(tab, fg_color="transparent")
        row.grid(row=1, column=0, padx=18, pady=8, sticky="ew")
        self.env_name = ctk.CTkEntry(row, width=160, placeholder_text="NAME")
        self.env_value = ctk.CTkEntry(row, placeholder_text="VALUE or folder to add to PATH")
        self.env_name.pack(side="left", padx=5)
        self.env_value.pack(side="left", fill="x", expand=True, padx=5)
        self.button(row, "List", self.list_env).pack(side="left", padx=5)
        self.button(row, "Set Var", self.set_env).pack(side="left", padx=5)
        self.button(row, "Add to PATH", self.add_path_env).pack(side="left", padx=5)
        self.env_output = self.textbox(tab, height=520)
        self.env_output.grid(row=2, column=0, padx=18, pady=10, sticky="nsew")

    def list_env(self):
        self.env_output.delete("1.0", "end")
        for k, v in self.env_editor.list_user_env():
            self.env_output.insert("end", f"{k}={v}\n\n")

    def set_env(self):
        name = self.env_name.get().strip()
        value = self.env_value.get().strip()
        if name and messagebox.askyesno("Environment", f"Set {name}?"):
            self.env_output.insert("end", self.env_editor.set_user_env(name, value) + "\n")

    def add_path_env(self):
        folder = self.env_value.get().strip() or filedialog.askdirectory()
        if folder and messagebox.askyesno("PATH", f"Add to PATH?\n{folder}"):
            self.env_output.insert("end", self.env_editor.add_to_path(folder) + "\n")

    def _build_updates(self):
        tab = self.frames["Updates"]
        tab.grid_columnconfigure(0, weight=1)
        self.page_header(tab, "ZEN Update Checker", "Check a GitHub releases/latest API URL or custom JSON endpoint.", 0, 0)
        row = ctk.CTkFrame(tab, fg_color="transparent")
        row.grid(row=1, column=0, padx=18, pady=8, sticky="ew")
        self.update_url_entry = ctk.CTkEntry(row, placeholder_text="https://api.github.com/repos/user/repo/releases/latest")
        self.update_url_entry.pack(side="left", fill="x", expand=True, padx=5)
        self.button(row, "Check Update", self.check_update_ui).pack(side="left", padx=5)
        self.update_output = self.textbox(tab, height=520)
        self.update_output.grid(row=2, column=0, padx=18, pady=10, sticky="nsew")

    def check_update_ui(self):
        self.update_output.delete("1.0", "end")
        self.update_output.insert("end", self.update_checker.check(self.update_url_entry.get().strip()))

    def _build_changelog(self):
        tab = self.frames["Changelog"]
        tab.grid_columnconfigure(0, weight=1)
        self.page_header(tab, "Changelog Viewer", "View and edit CHANGELOG.md.", 0, 0)
        row = ctk.CTkFrame(tab, fg_color="transparent")
        row.grid(row=1, column=0, padx=18, pady=8, sticky="ew")
        self.change_version = ctk.CTkEntry(row, width=140, placeholder_text="v1.0.1")
        self.change_version.pack(side="left", padx=5)
        self.button(row, "Reload", self.load_changelog).pack(side="left", padx=5)
        self.button(row, "Append Entry", self.append_changelog).pack(side="left", padx=5)
        self.changelog_output = self.textbox(tab, height=520)
        self.changelog_output.grid(row=2, column=0, padx=18, pady=10, sticky="nsew")
        self.load_changelog()

    def load_changelog(self):
        self.changelog_output.delete("1.0", "end")
        self.changelog_output.insert("end", self.changelog_viewer.read())

    def append_changelog(self):
        version = self.change_version.get().strip() or "vNext"
        text = self.changelog_output.get("1.0", "end").strip()
        self.changelog_viewer.append(version, text)
        self.load_changelog()

    def _build_plugins(self):
        tab = self.frames["Plugins"]
        tab.grid_columnconfigure(0, weight=1)
        self.page_header(tab, "Plugin System", "Create and run external plugin folders.", 0, 0)
        row = ctk.CTkFrame(tab, fg_color="transparent")
        row.grid(row=1, column=0, padx=18, pady=8, sticky="ew")
        self.plugin_name_entry = ctk.CTkEntry(row, width=220, placeholder_text="Plugin name to run")
        self.plugin_name_entry.pack(side="left", padx=5)
        self.button(row, "List Plugins", self.list_plugins_ui).pack(side="left", padx=5)
        self.button(row, "Create Example", self.create_plugin_example_ui).pack(side="left", padx=5)
        self.button(row, "Run Plugin", self.run_plugin_ui).pack(side="left", padx=5)
        self.button(row, "Open Plugins Folder", lambda: os.startfile(self.plugin_system.plugins_dir)).pack(side="left", padx=5)
        self.plugins_output = self.textbox(tab, height=520)
        self.plugins_output.grid(row=2, column=0, padx=18, pady=10, sticky="nsew")
        self.plugins_cache = []

    def list_plugins_ui(self):
        self.plugins_cache = self.plugin_system.list_plugins()
        self.plugins_output.delete("1.0", "end")
        for p in self.plugins_cache:
            self.plugins_output.insert("end", f"{p.get('name')} | {p.get('description','')}\nPath: {p.get('_path')}\n\n")

    def create_plugin_example_ui(self):
        path = self.plugin_system.create_example()
        self.plugins_output.insert("end", f"Created example plugin: {path}\n")
        self.list_plugins_ui()

    def run_plugin_ui(self):
        name = self.plugin_name_entry.get().strip().lower()
        if not self.plugins_cache:
            self.plugins_cache = self.plugin_system.list_plugins()
        for p in self.plugins_cache:
            if name in p.get("name","").lower():
                self.plugins_output.insert("end", self.plugin_system.run_plugin(p) + "\n")
                return
        self.plugins_output.insert("end", "Plugin not found. List plugins and type part of the name.\n")

    def _build_duplicates(self):
        tab = self.frames["Duplicates"]
        tab.grid_columnconfigure(0, weight=1)
        self.page_header(tab, "Duplicate File Finder", "Find duplicates using file hash and move selected duplicates to Recycle Bin.", 0, 0)
        row = ctk.CTkFrame(tab, fg_color="transparent")
        row.grid(row=1, column=0, padx=18, pady=8, sticky="ew")
        self.button(row, "Scan Folder", self.scan_duplicates_ui).pack(side="left", padx=5)
        self.button(row, "Recycle Duplicates", self.recycle_duplicates_ui).pack(side="left", padx=5)
        self.duplicates_output = self.textbox(tab, height=520)
        self.duplicates_output.grid(row=2, column=0, padx=18, pady=10, sticky="nsew")
        self.duplicates_cache = []

    def scan_duplicates_ui(self):
        folder = filedialog.askdirectory(title="Choose folder")
        if not folder: return
        def job():
            self.duplicates_output.delete("1.0", "end")
            self.duplicates_cache = self.duplicate_finder.scan(folder)
            self.duplicates_output.insert("end", f"Duplicates found: {len(self.duplicates_cache)}\n\n")
            for original, dup, size in self.duplicates_cache[:300]:
                self.duplicates_output.insert("end", f"ORIGINAL: {original}\nDUPLICATE: {dup}\nSIZE: {size/1024/1024:.2f} MB\n\n")
        self.run_thread(job)

    def recycle_duplicates_ui(self):
        if not self.duplicates_cache: return
        paths = [dup for _orig, dup, _size in self.duplicates_cache]
        if messagebox.askyesno("Duplicates", f"Move {len(paths)} duplicate files to Recycle Bin?"):
            self.duplicates_output.insert("end", self.duplicate_finder.recycle(paths) + "\n")

    def _build_large_files(self):
        tab = self.frames["Large Files"]
        tab.grid_columnconfigure(0, weight=1)
        self.page_header(tab, "Large File Finder", "Find the biggest files in a folder.", 0, 0)
        row = ctk.CTkFrame(tab, fg_color="transparent")
        row.grid(row=1, column=0, padx=18, pady=8, sticky="ew")
        self.large_min_entry = ctk.CTkEntry(row, width=120, placeholder_text="Min MB")
        self.large_min_entry.insert(0, "100")
        self.large_min_entry.pack(side="left", padx=5)
        self.button(row, "Scan Folder", self.scan_large_files_ui).pack(side="left", padx=5)
        self.button(row, "Recycle Listed", self.recycle_large_files_ui).pack(side="left", padx=5)
        self.large_output = self.textbox(tab, height=520)
        self.large_output.grid(row=2, column=0, padx=18, pady=10, sticky="nsew")
        self.large_cache = []

    def scan_large_files_ui(self):
        folder = filedialog.askdirectory(title="Choose folder")
        if not folder: return
        min_mb = self.large_min_entry.get().strip() or "100"
        def job():
            self.large_output.delete("1.0", "end")
            self.large_cache = self.large_file_finder.scan(folder, min_mb)
            for p, mb in self.large_cache:
                self.large_output.insert("end", f"{mb:>10.2f} MB | {p}\n")
        self.run_thread(job)

    def recycle_large_files_ui(self):
        if not self.large_cache: return
        paths = [p for p, _mb in self.large_cache]
        if messagebox.askyesno("Large Files", f"Move {len(paths)} listed files to Recycle Bin?"):
            self.large_output.insert("end", self.large_file_finder.recycle(paths) + "\n")

    def _build_folder_sizes(self):
        tab = self.frames["Folder Sizes"]
        tab.grid_columnconfigure(0, weight=1)
        self.page_header(tab, "Folder Size Analyzer", "Analyze child folder sizes and find what is taking space.", 0, 0)
        self.button(tab, "Analyze Folder", self.analyze_folder_sizes_ui).grid(row=1, column=0, padx=18, pady=8, sticky="w")
        self.folder_size_output = self.textbox(tab, height=540)
        self.folder_size_output.grid(row=2, column=0, padx=18, pady=10, sticky="nsew")

    def analyze_folder_sizes_ui(self):
        folder = filedialog.askdirectory(title="Choose folder")
        if not folder: return
        def job():
            self.folder_size_output.delete("1.0", "end")
            for p, mb in self.folder_size_analyzer.analyze_children(folder):
                self.folder_size_output.insert("end", f"{mb:>10.2f} MB | {p}\n")
        self.run_thread(job)

    def _build_fake_terminal(self):
        tab = self.frames["Fake Terminal"]
        tab.grid_columnconfigure(0, weight=1)
        self.page_header(tab, "Fake Terminal Generator", "Generate terminal-style PNG banners for README/profile images.", 0, 0)
        self.fake_terminal_input = self.textbox(tab, height=300)
        self.fake_terminal_input.grid(row=1, column=0, padx=18, pady=8, sticky="ew")
        self.fake_terminal_input.insert("end", "ZEN MENU\nSYSTEM ONLINE\nACCESS GRANTED")
        self.button(tab, "Generate PNG", self.generate_fake_terminal_ui).grid(row=2, column=0, padx=18, pady=8, sticky="w")
        self.fake_terminal_output = self.textbox(tab, height=220)
        self.fake_terminal_output.grid(row=3, column=0, padx=18, pady=10, sticky="nsew")

    def generate_fake_terminal_ui(self):
        dst = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG","*.png")])
        if not dst: return
        text = self.fake_terminal_input.get("1.0", "end").strip()
        self.fake_terminal_output.insert("end", self.fake_terminal_generator.generate(text, dst) + "\n")

    def _build_floating_widget(self):
        tab = self.frames["Floating Widget"]
        tab.grid_columnconfigure(0, weight=1)
        self.page_header(tab, "ZEN Floating Widget", "Small always-on-top widget with CPU, RAM and clock.", 0, 0)
        self.card(tab, "Open Floating Widget", "A small desktop widget. Later we can add custom images, logo and skins.", 1, 0, self.floating_widget.show)


    def _build_quick(self):
        tab = self.frames["Quick"]
        tab.grid_columnconfigure((0, 1, 2), weight=1)
        self.page_header(tab, "Quick Launcher 2.0", "Customizable shortcuts for apps, folders, links and copy actions.", 0, 0, 3)

        for i, item in enumerate(self.config_data.get("quick_launcher", [])):
            row = 1 + i // 3
            col = i % 3
            self.card(tab, item.get("name", "Shortcut"), f"{item.get('type', 'url')} → {item.get('value', '')}", row, col, lambda it=item: self.run_quick_item(it))

        self.card(tab, "Customize", "Edit shortcuts in Settings > Config Editor under quick_launcher.", 99, 0, lambda: self.show_page("Settings"))

    def run_quick_item(self, item):
        try:
            result = self.quick_launcher.run(item)
            self.notify("Quick Launcher", result)
            self.log(result)
        except Exception as e:
            messagebox.showerror("Quick Launcher", str(e))

    def _build_startup(self):
        tab = self.frames["Startup"]
        tab.grid_columnconfigure(0, weight=1)
        self.page_header(tab, "Startup Apps Manager", "View and control apps that start with Windows.", 0, 0)
        row = ctk.CTkFrame(tab, fg_color="transparent")
        row.grid(row=1, column=0, padx=18, pady=8, sticky="ew")
        self.button(row, "Refresh Startup Apps", self.refresh_startup).pack(side="left", padx=5)
        self.button(row, "Add ZEN to Startup", self.add_zen_startup).pack(side="left", padx=5)
        self.button(row, "Remove Selected Name", self.remove_startup_item).pack(side="left", padx=5)
        self.startup_name = ctk.CTkEntry(row, width=220, placeholder_text="Startup item name")
        self.startup_name.pack(side="left", padx=5)
        self.startup_output = self.textbox(tab, height=520)
        self.startup_output.grid(row=2, column=0, padx=18, pady=10, sticky="nsew")

    def refresh_startup(self):
        self.startup_output.delete("1.0", "end")
        for item in self.startup_manager.list_items():
            self.startup_output.insert("end", f"{item['name']} | {item['scope']}\n{item['command']}\n\n")

    def add_zen_startup(self):
        result = self.startup_manager.add_zen_startup()
        self.notify("Startup", result)
        self.refresh_startup()

    def remove_startup_item(self):
        name = self.startup_name.get().strip()
        if not name:
            return
        if messagebox.askyesno("Startup", f"Remove startup item '{name}'?"):
            try:
                result = self.startup_manager.remove_item(name)
                self.notify("Startup", result)
                self.refresh_startup()
            except Exception as e:
                messagebox.showerror("Startup", str(e))

    def _build_repair(self):
        tab = self.frames["Repair"]
        tab.grid_columnconfigure(0, weight=1)
        self.page_header(tab, "Windows Repair Tools", "Maintenance commands with confirmation before running.", 0, 0)
        row = ctk.CTkFrame(tab, fg_color="transparent")
        row.grid(row=1, column=0, padx=18, pady=8, sticky="ew")
        for name in ["Flush DNS", "Reset Winsock", "SFC Scan", "DISM RestoreHealth", "Clear Icon Cache", "Restart Explorer"]:
            self.button(row, name, lambda n=name: self.run_repair(n)).pack(side="left", padx=4, pady=4)
        self.repair_output = self.textbox(tab, height=520)
        self.repair_output.grid(row=2, column=0, padx=18, pady=10, sticky="nsew")

    def run_repair(self, name):
        if not messagebox.askyesno("Windows Repair", f"Run '{name}'? Some commands may need Administrator."):
            return
        def job():
            self.repair_output.insert("end", f"> Running {name}...\n")
            out = self.windows_repair.run(name)
            self.repair_output.insert("end", out + "\n")
            self.notify("Repair", f"{name} finished.")
        self.run_thread(job)

    def _build_performance(self):
        tab = self.frames["Performance"]
        tab.grid_columnconfigure((0,1,2), weight=1)
        self.page_header(tab, "Performance Monitor", "CPU, RAM, disk, uptime, battery and top processes.", 0, 0, 3)
        self.perf_output = self.textbox(tab, height=500)
        self.perf_output.grid(row=2, column=0, columnspan=3, padx=18, pady=10, sticky="nsew")
        self.card(tab, "Refresh Snapshot", "Update system metrics and top RAM processes.", 1, 0, self.refresh_performance)
        self.card(tab, "Open Processes", "Inspect and terminate processes in the advanced manager.", 1, 1, lambda: self.show_page("Processes"))
        self.card(tab, "Dashboard Widgets", "Widgets can be customized in config.json.", 1, 2, lambda: self.show_page("Settings"))

    def refresh_performance(self):
        snap = self.performance_monitor.snapshot()
        self.perf_output.delete("1.0", "end")
        self.perf_output.insert("end", json.dumps(snap, indent=2) + "\n\nTop RAM processes:\n")
        for name, pid, mem, cpu in self.performance_monitor.top_processes(10):
            self.perf_output.insert("end", f"{pid:<8} {mem:>8.1f} MB  CPU {cpu:<5}  {name}\n")

    def _build_converters(self):
        tab = self.frames["Converters"]
        tab.grid_columnconfigure(0, weight=1)
        self.page_header(tab, "Advanced Converters", "Images, ICO, TXT to PDF and FFmpeg-powered video GIF conversion.", 0, 0)
        row = ctk.CTkFrame(tab, fg_color="transparent")
        row.grid(row=1, column=0, padx=18, pady=8, sticky="ew")
        self.button(row, "Image Convert", self.convert_image_ui).pack(side="left", padx=5)
        self.button(row, "Image to ICO", self.image_to_ico_ui).pack(side="left", padx=5)
        self.button(row, "TXT to PDF", self.txt_to_pdf_ui).pack(side="left", padx=5)
        self.button(row, "Video to GIF", self.video_to_gif_ui).pack(side="left", padx=5)
        self.converter_output = self.textbox(tab, height=520)
        self.converter_output.grid(row=2, column=0, padx=18, pady=10, sticky="nsew")

    def convert_image_ui(self):
        src = filedialog.askopenfilename(title="Select image")
        if not src: return
        dst = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG","*.png"),("JPG","*.jpg"),("WEBP","*.webp"),("BMP","*.bmp")])
        if dst:
            self.converter_output.insert("end", self.converters.convert_image(src, dst) + "\n")

    def image_to_ico_ui(self):
        src = filedialog.askopenfilename(title="Select image")
        if not src: return
        dst = filedialog.asksaveasfilename(defaultextension=".ico")
        if dst:
            self.converter_output.insert("end", self.converters.image_to_ico(src, dst) + "\n")

    def txt_to_pdf_ui(self):
        src = filedialog.askopenfilename(title="Select TXT", filetypes=[("Text","*.txt")])
        if not src: return
        dst = filedialog.asksaveasfilename(defaultextension=".pdf")
        if dst:
            self.converter_output.insert("end", self.converters.text_to_pdf(src, dst) + "\n")

    def video_to_gif_ui(self):
        src = filedialog.askopenfilename(title="Select video")
        if not src: return
        dst = filedialog.asksaveasfilename(defaultextension=".gif")
        if dst:
            self.converter_output.insert("end", self.converters.video_to_gif(src, dst) + "\n")

    def _build_image_tools(self):
        tab = self.frames["Image Tools"]
        tab.grid_columnconfigure(0, weight=1)
        self.page_header(tab, "Image Tools", "Resize, compress, remove metadata and create clean assets.", 0, 0)
        controls = ctk.CTkFrame(tab, fg_color="transparent")
        controls.grid(row=1, column=0, padx=18, pady=8, sticky="ew")
        self.img_width = ctk.CTkEntry(controls, width=90, placeholder_text="Width")
        self.img_height = ctk.CTkEntry(controls, width=90, placeholder_text="Height")
        self.img_quality = ctk.CTkEntry(controls, width=90, placeholder_text="Quality")
        self.img_width.pack(side="left", padx=5); self.img_height.pack(side="left", padx=5); self.img_quality.pack(side="left", padx=5)
        self.button(controls, "Resize", self.resize_image_ui).pack(side="left", padx=5)
        self.button(controls, "Compress", self.compress_image_ui).pack(side="left", padx=5)
        self.button(controls, "Remove Metadata", self.remove_metadata_ui).pack(side="left", padx=5)
        self.image_output = self.textbox(tab, height=520)
        self.image_output.grid(row=2, column=0, padx=18, pady=10, sticky="nsew")

    def resize_image_ui(self):
        src = filedialog.askopenfilename(title="Select image")
        if not src: return
        dst = filedialog.asksaveasfilename(defaultextension=".png")
        if dst:
            self.image_output.insert("end", self.image_tools.resize(src, dst, self.img_width.get() or 512, self.img_height.get() or 512) + "\n")

    def compress_image_ui(self):
        src = filedialog.askopenfilename(title="Select image")
        if not src: return
        dst = filedialog.asksaveasfilename(defaultextension=".jpg")
        if dst:
            self.image_output.insert("end", self.image_tools.compress(src, dst, self.img_quality.get() or 75) + "\n")

    def remove_metadata_ui(self):
        src = filedialog.askopenfilename(title="Select image")
        if not src: return
        dst = filedialog.asksaveasfilename(defaultextension=".png")
        if dst:
            self.image_output.insert("end", self.image_tools.remove_metadata(src, dst) + "\n")

    def _build_github(self):
        tab = self.frames["GitHub"]
        tab.grid_columnconfigure(0, weight=1)
        self.page_header(tab, "GitHub Project Tools", "Run common Git commands and create project files.", 0, 0)
        row = ctk.CTkFrame(tab, fg_color="transparent")
        row.grid(row=1, column=0, padx=18, pady=8, sticky="ew")
        self.git_folder = ctk.CTkEntry(row, placeholder_text="Project folder")
        self.git_folder.pack(side="left", fill="x", expand=True, padx=5)
        self.button(row, "Browse", lambda: self.set_entry_value(self.git_folder, filedialog.askdirectory())).pack(side="left", padx=5)
        for name, fn in [("git init", self.git_init), ("status", self.git_status), ("add .", self.git_add), ("commit", self.git_commit), ("push", self.git_push), (".gitignore", self.gitignore)]:
            self.button(row, name, fn).pack(side="left", padx=4)
        self.github_output = self.textbox(tab, height=520)
        self.github_output.grid(row=2, column=0, padx=18, pady=10, sticky="nsew")

    def git_dir(self): return self.git_folder.get().strip()
    def git_init(self): self.github_output.insert("end", self.github_tools.init_repo(self.git_dir()) + "\n")
    def git_status(self): self.github_output.insert("end", self.github_tools.status(self.git_dir()) + "\n")
    def git_add(self): self.github_output.insert("end", self.github_tools.add_all(self.git_dir()) + "\n")
    def git_commit(self):
        msg = "update project"
        self.github_output.insert("end", self.github_tools.commit(self.git_dir(), msg) + "\n")
    def git_push(self): self.github_output.insert("end", self.github_tools.push(self.git_dir()) + "\n")
    def gitignore(self): self.github_output.insert("end", self.github_tools.create_gitignore(self.git_dir()) + "\n")

    def _build_project_maker(self):
        tab = self.frames["Project Maker"]
        tab.grid_columnconfigure(0, weight=1)
        self.page_header(tab, "GitHub Repo Creator", "Create a clean project structure automatically.", 0, 0)
        row = ctk.CTkFrame(tab, fg_color="transparent")
        row.grid(row=1, column=0, padx=18, pady=8, sticky="ew")
        self.pm_name = ctk.CTkEntry(row, placeholder_text="Project name")
        self.pm_name.pack(side="left", fill="x", expand=True, padx=5)
        self.pm_template = ctk.CTkOptionMenu(row, values=["Python GUI", "Python CLI", "HTML/CSS/JS"])
        self.pm_template.pack(side="left", padx=5)
        self.button(row, "Create Project", self.create_project_ui).pack(side="left", padx=5)
        self.pm_output = self.textbox(tab, height=520)
        self.pm_output.grid(row=2, column=0, padx=18, pady=10, sticky="nsew")

    def create_project_ui(self):
        folder = filedialog.askdirectory(title="Choose parent folder")
        if not folder: return
        name = self.pm_name.get().strip() or "zen-project"
        created = self.project_creator.create(folder, name, self.pm_template.get(), self.config_data.get("project_creator",{}).get("default_author","superstandarts"))
        self.pm_output.insert("end", f"Created: {created}\n")

    def _build_error_analyzer(self):
        tab = self.frames["Error Analyzer"]
        tab.grid_columnconfigure(0, weight=1)
        self.page_header(tab, "Error Analyzer", "Paste Python, pip or PyInstaller errors and get quick fixes.", 0, 0)
        self.error_input = self.textbox(tab, height=250)
        self.error_input.grid(row=1, column=0, padx=18, pady=8, sticky="ew")
        self.button(tab, "Analyze Error", self.analyze_error_ui).grid(row=2, column=0, padx=18, pady=4, sticky="w")
        self.error_output = self.textbox(tab, height=260)
        self.error_output.grid(row=3, column=0, padx=18, pady=10, sticky="nsew")

    def analyze_error_ui(self):
        text = self.error_input.get("1.0", "end")
        self.error_output.delete("1.0", "end")
        self.error_output.insert("end", self.error_analyzer.analyze(text))

    def _build_exe_builder(self):
        tab = self.frames["EXE Builder"]
        tab.grid_columnconfigure(0, weight=1)
        self.page_header(tab, "Visual EXE Builder", "Generate PyInstaller commands and build executables visually.", 0, 0)
        row = ctk.CTkFrame(tab, fg_color="transparent")
        row.grid(row=1, column=0, padx=18, pady=8, sticky="ew")
        self.exe_script = ctk.CTkEntry(row, placeholder_text="main.py path")
        self.exe_script.pack(side="left", fill="x", expand=True, padx=5)
        self.exe_name = ctk.CTkEntry(row, width=180, placeholder_text="App name")
        self.exe_name.pack(side="left", padx=5)
        self.exe_icon = ctk.CTkEntry(row, width=180, placeholder_text="icon.ico optional")
        self.exe_icon.pack(side="left", padx=5)
        self.button(row, "Browse Script", lambda: self.set_entry_value(self.exe_script, filedialog.askopenfilename(filetypes=[("Python","*.py")]))).pack(side="left", padx=5)
        self.button(row, "Build EXE", self.build_exe_ui).pack(side="left", padx=5)
        self.exe_output = self.textbox(tab, height=520)
        self.exe_output.grid(row=2, column=0, padx=18, pady=10, sticky="nsew")

    def build_exe_ui(self):
        if not messagebox.askyesno("EXE Builder", "Start PyInstaller build?"):
            return
        def job():
            out = self.exe_builder.build(self.exe_script.get().strip(), self.exe_name.get().strip() or "App", self.exe_icon.get().strip())
            self.exe_output.insert("end", out + "\n")
        self.run_thread(job)

    def _build_zenai_actions(self):
        tab = self.frames["ZENAI Actions"]
        tab.grid_columnconfigure(0, weight=1)
        self.page_header(tab, "ZENAI Config Actions", "Apply safe config actions with preview-style buttons.", 0, 0)
        row = ctk.CTkFrame(tab, fg_color="transparent")
        row.grid(row=1, column=0, padx=18, pady=8, sticky="ew")
        self.za_combo = ctk.CTkEntry(row, width=160, placeholder_text="ctrl+alt+y")
        self.za_value = ctk.CTkEntry(row, width=300, placeholder_text="https://youtube.com")
        self.za_combo.pack(side="left", padx=5); self.za_value.pack(side="left", padx=5)
        self.button(row, "Add URL Hotkey", self.add_hotkey_action).pack(side="left", padx=5)
        self.button(row, "Create Gaming Profile", self.create_gaming_profile_action).pack(side="left", padx=5)
        self.za_output = self.textbox(tab, height=520)
        self.za_output.grid(row=2, column=0, padx=18, pady=10, sticky="nsew")

    def add_hotkey_action(self):
        combo = self.za_combo.get().strip() or "ctrl+alt+y"
        value = self.za_value.get().strip() or "https://youtube.com"
        if messagebox.askyesno("ZENAI Actions", f"Add hotkey {combo} -> {value}?"):
            self.za_output.insert("end", self.zenai_actions.add_hotkey(combo, "open_url", value) + "\n")

    def create_gaming_profile_action(self):
        if messagebox.askyesno("ZENAI Actions", "Create/replace Gaming Mode profile?"):
            self.za_output.insert("end", self.zenai_actions.add_profile("Gaming Mode", ["Discord.exe", "steam.exe"], ["chrome.exe"], []) + "\n")

    def _build_music(self):
        tab = self.frames["Music"]
        tab.grid_columnconfigure(0, weight=1)
        tab.grid_rowconfigure(2, weight=1)
        self.page_header(tab, "Spotify Music Widget", "Auto-updating player with synced lyrics and highlighted current line.", 0, 0)

        row = ctk.CTkFrame(tab, fg_color="transparent")
        row.grid(row=1, column=0, padx=18, pady=8, sticky="ew")
        self.button(row, "Start Auto Update", self.start_music_auto_update).pack(side="left", padx=5)
        self.button(row, "Stop Auto Update", self.stop_music_auto_update).pack(side="left", padx=5)
        self.button(row, "Refresh Now", self.refresh_music).pack(side="left", padx=5)

        self.music_auto_update = False
        self.music_output = self.textbox(tab, height=520)
        self.music_output.grid(row=2, column=0, padx=18, pady=10, sticky="nsew")
        try:
            self.music_output.tag_config("current_lyric", background="#3a3a42", foreground="#ffffff")
        except Exception:
            pass

    def start_music_auto_update(self):
        self.music_auto_update = True
        self.refresh_music_loop()

    def stop_music_auto_update(self):
        self.music_auto_update = False

    def refresh_music_loop(self):
        if not getattr(self, "music_auto_update", False):
            return
        self.refresh_music()
        self.after(1000, self.refresh_music_loop)

    def refresh_music(self):
        text, _track = self.music_widget.current_with_lyrics()
        self.music_output.delete("1.0", "end")
        self.music_output.insert("end", text)
        try:
            lines = text.splitlines()
            for i, line in enumerate(lines, start=1):
                if line.startswith(">>>"):
                    self.music_output.tag_add("current_lyric", f"{i}.0", f"{i}.end")
                    self.music_output.see(f"{i}.0")
                    break
        except Exception:
            pass

    def _build_uninstaller(self):
        tab = self.frames["Uninstaller"]
        tab.grid_columnconfigure(0, weight=1)
        self.page_header(tab, "Ultimate Uninstaller", "Run official uninstallers, then scan and safely remove leftovers.", 0, 0)
        row = ctk.CTkFrame(tab, fg_color="transparent")
        row.grid(row=1, column=0, padx=18, pady=8, sticky="ew")
        self.uninstall_search = ctk.CTkEntry(row, placeholder_text="Search installed app")
        self.uninstall_search.pack(side="left", fill="x", expand=True, padx=5)
        self.button(row, "List Apps", self.list_installed_apps).pack(side="left", padx=5)
        self.button(row, "Run Uninstaller", self.run_selected_uninstaller).pack(side="left", padx=5)
        self.button(row, "Scan Leftovers", self.scan_uninstall_leftovers).pack(side="left", padx=5)
        self.button(row, "Move Leftovers to Recycle Bin", self.remove_uninstall_leftovers).pack(side="left", padx=5)
        self.uninstall_output = self.textbox(tab, height=520)
        self.uninstall_output.grid(row=2, column=0, padx=18, pady=10, sticky="nsew")
        self.installed_apps_cache = []
        self.leftovers_cache = []

    def list_installed_apps(self):
        q = self.uninstall_search.get().lower().strip()
        self.installed_apps_cache = self.ultimate_uninstaller.installed_apps()
        self.uninstall_output.delete("1.0", "end")
        for i, app in enumerate(self.installed_apps_cache):
            if q and q not in app["name"].lower():
                continue
            self.uninstall_output.insert("end", f"[{i}] {app['name']} | {app.get('version','')} | {app.get('publisher','')}\n")

    def _selected_app(self):
        q = self.uninstall_search.get().lower().strip()
        if not self.installed_apps_cache:
            self.installed_apps_cache = self.ultimate_uninstaller.installed_apps()
        for app in self.installed_apps_cache:
            if q and q in app["name"].lower():
                return app
        return None

    def run_selected_uninstaller(self):
        app = self._selected_app()
        if not app:
            messagebox.showerror("Uninstaller", "No matching app found. Search by name first.")
            return
        if messagebox.askyesno("Ultimate Uninstaller", f"Run official uninstaller for {app['name']}?"):
            self.uninstall_output.insert("end", self.ultimate_uninstaller.run_uninstaller(app) + "\n")

    def scan_uninstall_leftovers(self):
        app = self._selected_app()
        if not app:
            messagebox.showerror("Uninstaller", "No matching app found.")
            return
        roots = self.config_data.get("uninstaller", {}).get("leftover_roots", [])
        self.leftovers_cache = self.ultimate_uninstaller.scan_leftovers(app["name"], roots)
        self.uninstall_output.insert("end", f"\nLeftovers found for {app['name']}: {len(self.leftovers_cache)}\n")
        for p in self.leftovers_cache[:200]:
            self.uninstall_output.insert("end", p + "\n")
        if len(self.leftovers_cache) > 200:
            self.uninstall_output.insert("end", "... showing first 200 only\n")

    def remove_uninstall_leftovers(self):
        if not self.leftovers_cache:
            return
        if messagebox.askyesno("Ultimate Uninstaller", f"Move {len(self.leftovers_cache)} leftovers to Recycle Bin?"):
            self.uninstall_output.insert("end", self.ultimate_uninstaller.remove_leftovers_safe(self.leftovers_cache) + "\n")


    def _build_settings(self):
        tab = self.frames["Settings"]
        tab.grid_columnconfigure(0, weight=1)
        self.page_header(tab, "Settings / Config Editor", "Edit config.json without leaving the app.", 0, 0)

        quick = ctk.CTkFrame(tab, fg_color="#17181d", border_width=1, border_color="#30323a", corner_radius=26)
        quick.grid(row=1, column=0, padx=18, pady=8, sticky="ew")
        quick.grid_columnconfigure((1, 3), weight=1)

        ctk.CTkLabel(quick, text="Discord ID", font=("Segoe UI Variable", 13, "bold")).grid(row=0, column=0, padx=12, pady=12, sticky="w")
        self.discord_id_entry = ctk.CTkEntry(quick)
        self.discord_id_entry.grid(row=0, column=1, padx=8, pady=12, sticky="ew")
        self.discord_id_entry.insert(0, self.config_data.get("discord", {}).get("client_id", ""))

        ctk.CTkLabel(quick, text="Spotify ID", font=("Segoe UI Variable", 13, "bold")).grid(row=0, column=2, padx=12, pady=12, sticky="w")
        self.spotify_id_entry = ctk.CTkEntry(quick)
        self.spotify_id_entry.grid(row=0, column=3, padx=8, pady=12, sticky="ew")
        self.spotify_id_entry.insert(0, self.config_data.get("discord", {}).get("spotify", {}).get("client_id", ""))

        ctk.CTkLabel(quick, text="Spotify Secret", font=("Segoe UI Variable", 13, "bold")).grid(row=1, column=0, padx=12, pady=12, sticky="w")
        self.spotify_secret_entry = ctk.CTkEntry(quick, show="*")
        self.spotify_secret_entry.grid(row=1, column=1, padx=8, pady=12, sticky="ew")
        self.spotify_secret_entry.insert(0, self.config_data.get("discord", {}).get("spotify", {}).get("client_secret", ""))

        self.button(quick, "Save quick config", self.save_quick_config).grid(row=1, column=3, padx=8, pady=12, sticky="ew")

        self.config_text = self.textbox(tab, height=430)
        self.config_text.grid(row=2, column=0, padx=18, pady=10, sticky="nsew")
        self.config_text.insert("end", self.config_editor.load_text())

        actions = ctk.CTkFrame(tab, fg_color="transparent")
        actions.grid(row=3, column=0, padx=18, pady=8, sticky="ew")
        self.button(actions, "Save JSON", self.save_config_text).pack(side="left", padx=5)
        self.button(actions, "Reload JSON", self.reload_config_text).pack(side="left", padx=5)
        self.button(actions, "Open config folder", lambda: os.startfile(APP_DIR)).pack(side="left", padx=5)
        self.button(actions, "Start tray icon", self.start_tray).pack(side="left", padx=5)

    def save_quick_config(self):
        try:
            data = self.config_editor.load_json()
            data.setdefault("discord", {})["client_id"] = self.discord_id_entry.get().strip()
            data["discord"].setdefault("spotify", {})["client_id"] = self.spotify_id_entry.get().strip()
            data["discord"]["spotify"]["client_secret"] = self.spotify_secret_entry.get().strip()
            CONFIG_PATH.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
            self.config_data = data
            self.reload_config_text()
            self.notify("Config saved", "Discord and Spotify IDs updated.")
        except Exception as e:
            messagebox.showerror("Config error", str(e))

    def save_config_text(self):
        try:
            self.config_editor.save_text(self.config_text.get("1.0", "end").strip())
            self.config_data = self.config_editor.load_json()
            self.notify("Config saved", "config.json was saved successfully.")
        except Exception as e:
            messagebox.showerror("Invalid JSON", str(e))

    def reload_config_text(self):
        self.config_text.delete("1.0", "end")
        self.config_text.insert("end", self.config_editor.load_text())

    def _build_profiles(self):
        tab = self.frames["Profiles"]
        tab.grid_columnconfigure(0, weight=1)
        self.page_header(tab, "App Profiles / Modes", "Run predefined modes like Gaming, Coding or Study.", 0, 0)

        self.profile_output = self.textbox(tab, height=420)
        self.profile_output.grid(row=2, column=0, padx=18, pady=12, sticky="nsew")

        grid = ctk.CTkFrame(tab, fg_color="transparent")
        grid.grid(row=1, column=0, padx=18, pady=5, sticky="ew")

        for name in self.config_data.get("profiles", {}).keys():
            self.button(grid, f"Run {name}", lambda n=name: self.run_profile(n)).pack(side="left", padx=5, pady=5)

    def run_profile(self, name):
        result = self.profiles_manager.run_profile(name)
        self.profile_output.insert("end", result + "\n")
        self.notify("Profile executed", result)
        self.log(result)

    def _build_processes(self):
        tab = self.frames["Processes"]
        tab.grid_columnconfigure(0, weight=1)
        self.page_header(tab, "Advanced Process Manager", "Search processes, inspect PID/RAM/path and terminate safely.", 0, 0)

        top = ctk.CTkFrame(tab, fg_color="transparent")
        top.grid(row=1, column=0, padx=18, pady=5, sticky="ew")
        self.process_search = ctk.CTkEntry(top, placeholder_text="Search process name...")
        self.process_search.pack(side="left", fill="x", expand=True, padx=5)
        self.button(top, "Refresh", self.refresh_processes).pack(side="left", padx=5)
        self.button(top, "Terminate PID", self.terminate_pid).pack(side="left", padx=5)
        self.button(top, "Open PID Location", self.open_pid_location).pack(side="left", padx=5)

        pidrow = ctk.CTkFrame(tab, fg_color="transparent")
        pidrow.grid(row=2, column=0, padx=18, pady=5, sticky="ew")
        ctk.CTkLabel(pidrow, text="PID:", font=("Segoe UI Variable", 13, "bold")).pack(side="left", padx=5)
        self.pid_entry = ctk.CTkEntry(pidrow, width=120)
        self.pid_entry.pack(side="left", padx=5)

        self.process_output = self.textbox(tab, height=500)
        self.process_output.grid(row=3, column=0, padx=18, pady=10, sticky="nsew")

    def refresh_processes(self):
        query = self.process_search.get().lower().strip()
        rows = self.process_manager.list_processes()
        self.process_output.delete("1.0", "end")
        self.process_output.insert("end", f"{'PID':<8} {'RAM(MB)':<10} {'CPU':<6} NAME\n")
        self.process_output.insert("end", "-" * 90 + "\n")
        count = 0
        for r in rows:
            if query and query not in r["name"].lower():
                continue
            self.process_output.insert("end", f"{r['pid']:<8} {r['memory_mb']:<10.1f} {r['cpu']:<6} {r['name']} | {r['exe']}\n")
            count += 1
            if count >= 250:
                break
        self.log(f"Process list refreshed: {count} shown.")

    def terminate_pid(self):
        pid = self.pid_entry.get().strip()
        if not pid:
            return
        if not messagebox.askyesno("Terminate process", f"Terminate PID {pid}?"):
            return
        try:
            self.process_manager.terminate(pid, force=False)
            self.notify("Process terminated", f"PID {pid} terminated.")
            self.refresh_processes()
        except Exception as e:
            messagebox.showerror("Process error", str(e))

    def open_pid_location(self):
        pid = self.pid_entry.get().strip()
        try:
            path = self.process_manager.open_location(pid)
            self.log(f"Opened process location: {path}")
        except Exception as e:
            messagebox.showerror("Process error", str(e))

    def _build_internet(self):
        tab = self.frames["Internet"]
        tab.grid_columnconfigure(0, weight=1)
        self.page_header(tab, "Internet Tools", "Ping, IP info, DNS flush and quick repair commands.", 0, 0)

        row = ctk.CTkFrame(tab, fg_color="transparent")
        row.grid(row=1, column=0, padx=18, pady=5, sticky="ew")
        self.host_entry = ctk.CTkEntry(row, placeholder_text="Host, example: google.com")
        self.host_entry.insert(0, "google.com")
        self.host_entry.pack(side="left", fill="x", expand=True, padx=5)
        self.button(row, "Ping", self.ping_host).pack(side="left", padx=5)
        self.button(row, "Local IP", self.show_local_ip).pack(side="left", padx=5)
        self.button(row, "Flush DNS", self.flush_dns).pack(side="left", padx=5)
        self.button(row, "Network Settings", self.internet_tools.open_network_settings).pack(side="left", padx=5)

        self.internet_output = self.textbox(tab, height=530)
        self.internet_output.grid(row=2, column=0, padx=18, pady=10, sticky="nsew")

    def ping_host(self):
        host = self.host_entry.get().strip() or "google.com"
        self.internet_output.delete("1.0", "end")
        self.internet_output.insert("end", self.internet_tools.ping(host))

    def show_local_ip(self):
        self.internet_output.insert("end", f"Hostname: {self.internet_tools.hostname()}\nLocal IP: {self.internet_tools.local_ip()}\n")

    def flush_dns(self):
        if not messagebox.askyesno("Flush DNS", "Run ipconfig /flushdns?"):
            return
        self.internet_output.insert("end", self.internet_tools.flush_dns() + "\n")
        self.notify("Internet tools", "DNS flush command executed.")

    def _build_privacy(self):
        tab = self.frames["Privacy"]
        tab.grid_columnconfigure(0, weight=1)
        self.page_header(tab, "Privacy Cleaner", "Clear local traces such as clipboard, recent files and Run history.", 0, 0)

        actions = ctk.CTkFrame(tab, fg_color="transparent")
        actions.grid(row=1, column=0, padx=18, pady=8, sticky="ew")

        self.button(actions, "Clear Clipboard", lambda: self.privacy_action(self.privacy_cleaner.clear_clipboard)).pack(side="left", padx=5)
        self.button(actions, "Clear Recent Files", lambda: self.privacy_confirm(self.privacy_cleaner.clear_recent_files)).pack(side="left", padx=5)
        self.button(actions, "Clear Run History", lambda: self.privacy_confirm(self.privacy_cleaner.clear_run_history)).pack(side="left", padx=5)
        self.button(actions, "Clear Explorer History", lambda: self.privacy_confirm(self.privacy_cleaner.clear_explorer_history)).pack(side="left", padx=5)

        self.privacy_output = self.textbox(tab, height=520)
        self.privacy_output.grid(row=2, column=0, padx=18, pady=10, sticky="nsew")

    def privacy_action(self, fn):
        result = fn()
        self.privacy_output.insert("end", result + "\n")
        self.notify("Privacy Cleaner", result)

    def privacy_confirm(self, fn):
        if messagebox.askyesno("Privacy Cleaner", "Run this privacy cleanup action?"):
            self.privacy_action(fn)

    def _build_themes(self):
        tab = self.frames["Themes"]
        tab.grid_columnconfigure(0, weight=1)
        self.page_header(tab, "Theme Customizer", "Choose a visual preset. Saved into config.json.", 0, 0)

        row = ctk.CTkFrame(tab, fg_color="transparent")
        row.grid(row=1, column=0, padx=18, pady=8, sticky="ew")
        self.theme_option = ctk.CTkOptionMenu(row, values=list(ThemeManager.THEMES.keys()))
        self.theme_option.pack(side="left", padx=5)
        self.button(row, "Save Theme", self.save_theme).pack(side="left", padx=5)

        self.theme_output = self.textbox(tab, height=460)
        self.theme_output.grid(row=2, column=0, padx=18, pady=10, sticky="nsew")
        self.theme_output.insert("end", json.dumps(ThemeManager.THEMES, indent=2))

    def save_theme(self):
        theme = self.theme_option.get()
        data = self.config_editor.load_json()
        data.setdefault("theme", {}).update(ThemeManager.THEMES[theme])
        data["theme"]["mode"] = theme
        data.setdefault("_quick_settings", {})["theme_mode"] = theme
        data["_quick_settings"]["theme_accent"] = ThemeManager.THEMES[theme].get("accent", "#ffffff")
        CONFIG_PATH.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
        self.notify("Theme saved", f"{theme} saved. Restart the app to fully apply it.")

    def _build_passwords(self):
        tab = self.frames["Passwords"]
        tab.grid_columnconfigure(0, weight=1)
        self.page_header(tab, "Password Generator", "Generate strong random passwords and copy them quickly.", 0, 0)

        row = ctk.CTkFrame(tab, fg_color="transparent")
        row.grid(row=1, column=0, padx=18, pady=8, sticky="ew")
        ctk.CTkLabel(row, text="Length:", font=("Segoe UI Variable", 13, "bold")).pack(side="left", padx=5)
        self.pass_len = ctk.CTkEntry(row, width=80)
        self.pass_len.insert(0, "18")
        self.pass_len.pack(side="left", padx=5)
        self.button(row, "Generate", self.generate_password).pack(side="left", padx=5)
        self.button(row, "Copy", self.copy_password).pack(side="left", padx=5)

        self.password_output = self.textbox(tab, height=260)
        self.password_output.grid(row=2, column=0, padx=18, pady=10, sticky="ew")
        self.generated_password = ""

    def generate_password(self):
        try:
            length = int(self.pass_len.get())
        except Exception:
            length = 18
        self.generated_password = self.password_generator.generate(length)
        strength = self.password_generator.strength(self.generated_password)
        self.password_output.delete("1.0", "end")
        self.password_output.insert("end", f"{self.generated_password}\n\nStrength: {strength}")

    def copy_password(self):
        if self.generated_password:
            pyperclip.copy(self.generated_password)
            self.notify("Password copied", "Generated password copied to clipboard.")

    def _build_zenai(self):
        tab = self.frames["ZENAI"]
        tab.grid_columnconfigure(0, weight=1)
        self.page_header(tab, "ZENAI", "Local assistant for errors, config, Spotify, Discord and usage help.", 0, 0)

        self.zenai_chat = self.textbox(tab, height=500)
        self.zenai_chat.grid(row=1, column=0, padx=18, pady=10, sticky="nsew")
        self.zenai_chat.insert("end", "ZENAI: Hello. Ask me about errors, config, Spotify, Discord, profiles or cleaning.\n\n")

        row = ctk.CTkFrame(tab, fg_color="transparent")
        row.grid(row=2, column=0, padx=18, pady=8, sticky="ew")
        row.grid_columnconfigure(0, weight=1)
        self.zenai_input = ctk.CTkEntry(row, placeholder_text="Ask ZENAI...")
        self.zenai_input.grid(row=0, column=0, padx=5, sticky="ew")
        self.button(row, "Send", self.ask_zenai).grid(row=0, column=1, padx=5)

        quick = ctk.CTkFrame(tab, fg_color="transparent")
        quick.grid(row=3, column=0, padx=18, pady=4, sticky="ew")
        for text in ["Explain an error", "How to configure Spotify?", "How do profiles work?", "How do I clean privacy?"]:
            self.button(quick, text, lambda t=text: self.quick_zenai(t)).pack(side="left", padx=4, pady=4)

    def quick_zenai(self, text):
        self.zenai_input.delete(0, "end")
        self.zenai_input.insert(0, text)
        self.ask_zenai()

    def ask_zenai(self):
        msg = self.zenai_input.get().strip()
        if not msg:
            return
        reply = self.zenai.ask(msg)
        self.zenai_chat.insert("end", f"You: {msg}\nZENAI: {reply}\n\n")
        self.zenai_chat.see("end")
        self.zenai_input.delete(0, "end")

    def _build_cleaner(self):
        tab = self.frames["Cleaner"]
        tab.grid_columnconfigure(0, weight=1)
        self.page_header(tab, "Junk Cleaner", "Scan and move temporary files to the Recycle Bin safely.", 0, 0)
        self.cleaner_output = self.textbox(tab, height=500)
        self.cleaner_output.grid(row=1, column=0, padx=18, pady=10, sticky="nsew")
        row = ctk.CTkFrame(tab, fg_color="transparent")
        row.grid(row=2, column=0, padx=18, pady=8, sticky="ew")
        self.button(row, "Scan", self.run_cleaner_scan).pack(side="left", padx=5)
        self.button(row, "Clean Safe", self.run_cleaner_clean).pack(side="left", padx=5)
        self.button(row, "Open Temp", lambda: os.startfile(os.getenv("TEMP"))).pack(side="left", padx=5)

    def _build_files(self):
        tab = self.frames["Files"]
        tab.grid_columnconfigure(0, weight=1)
        self.page_header(tab, "Files & Screenshots", "Organize screenshots and search local files.", 0, 0)
        row = ctk.CTkFrame(tab, fg_color="transparent")
        row.grid(row=1, column=0, padx=18, pady=8, sticky="ew")
        row.grid_columnconfigure(0, weight=1)
        self.search_entry = ctk.CTkEntry(row, placeholder_text="Search files, example: .png, readme, roblox")
        self.search_entry.grid(row=0, column=0, padx=5, sticky="ew")
        self.button(row, "Search Folder", self.search_files).grid(row=0, column=1, padx=5)
        self.button(row, "Organize Screenshots", self.organize_screenshots).grid(row=0, column=2, padx=5)
        self.files_output = self.textbox(tab, height=500)
        self.files_output.grid(row=2, column=0, padx=18, pady=10, sticky="nsew")

    def _build_discord(self):
        tab = self.frames["Discord"]
        tab.grid_columnconfigure(0, weight=1)
        self.page_header(tab, "Discord / Spotify Status", "Auto Rich Presence using your saved Discord and Spotify IDs.", 0, 0)
        row = ctk.CTkFrame(tab, fg_color="transparent")
        row.grid(row=1, column=0, padx=18, pady=8, sticky="ew")
        self.button(row, "Start Status", self.start_discord).pack(side="left", padx=5)
        self.button(row, "Stop Status", self.stop_discord).pack(side="left", padx=5)
        self.discord_output = self.textbox(tab, height=500)
        self.discord_output.grid(row=2, column=0, padx=18, pady=10, sticky="nsew")
        self.discord_output.insert("end", "Discord + Spotify config loaded from config.json.\n")

    def _build_automation(self):
        tab = self.frames["Automation"]
        tab.grid_columnconfigure(0, weight=1)
        self.page_header(tab, "Automation", "Hotkeys, text expander and safe auto clicker.", 0, 0)
        row1 = ctk.CTkFrame(tab, fg_color="transparent")
        row1.grid(row=1, column=0, padx=18, pady=8, sticky="ew")
        self.button(row1, "Start Hotkeys", self.start_hotkeys).pack(side="left", padx=5)
        self.button(row1, "Stop Hotkeys", self.stop_hotkeys).pack(side="left", padx=5)
        self.button(row1, "Start Text Expander", self.start_expander).pack(side="left", padx=5)
        self.button(row1, "Stop Text Expander", self.stop_expander).pack(side="left", padx=5)
        row2 = ctk.CTkFrame(tab, fg_color="transparent")
        row2.grid(row=2, column=0, padx=18, pady=8, sticky="ew")
        self.click_interval = ctk.CTkEntry(row2, width=90, placeholder_text="0.1")
        self.click_interval.pack(side="left", padx=5)
        self.button(row2, "Start Safe Auto Clicker", self.start_clicker).pack(side="left", padx=5)
        self.button(row2, "Stop Auto Clicker", self.stop_clicker).pack(side="left", padx=5)
        self.automation_output = self.textbox(tab, height=430)
        self.automation_output.grid(row=3, column=0, padx=18, pady=10, sticky="nsew")

    def _build_gaming(self):
        tab = self.frames["Gaming"]
        tab.grid_columnconfigure(0, weight=1)
        self.page_header(tab, "Gaming Tools", "Game session manager and volume session list.", 0, 0)
        row = ctk.CTkFrame(tab, fg_color="transparent")
        row.grid(row=1, column=0, padx=18, pady=8, sticky="ew")
        self.button(row, "Start Game Session", self.start_game_session).pack(side="left", padx=5)
        self.button(row, "End Game Session", self.end_game_session).pack(side="left", padx=5)
        self.button(row, "Refresh App Volumes", self.refresh_volumes).pack(side="left", padx=5)
        self.volume_output = self.textbox(tab, height=500)
        self.volume_output.grid(row=2, column=0, padx=18, pady=10, sticky="nsew")

    def _build_creator(self):
        tab = self.frames["Creator"]
        tab.grid_columnconfigure(1, weight=1)
        self.page_header(tab, "Creator Tools", "Generate README files and project documentation faster.", 0, 0, 2)
        self.readme_name = ctk.CTkEntry(tab, placeholder_text="Project name")
        self.readme_desc = ctk.CTkEntry(tab, placeholder_text="Project description")
        self.readme_author = ctk.CTkEntry(tab, placeholder_text="Author/GitHub username")
        self.readme_name.grid(row=1, column=0, padx=18, pady=6, sticky="ew")
        self.readme_desc.grid(row=2, column=0, padx=18, pady=6, sticky="ew")
        self.readme_author.grid(row=3, column=0, padx=18, pady=6, sticky="ew")
        self.button(tab, "Generate README.md", self.generate_readme_file).grid(row=4, column=0, padx=18, pady=10, sticky="ew")
        self.creator_output = self.textbox(tab, height=500)
        self.creator_output.grid(row=1, column=1, rowspan=5, padx=18, pady=10, sticky="nsew")

    def _build_credits(self):
        tab = self.frames["Credits"]
        tab.grid_columnconfigure((0, 1), weight=1)
        tab.grid_rowconfigure(2, weight=1)

        self.page_header(
            tab,
            "Credits & Contact",
            "Creator information, socials and project links in one place.",
            0,
            0,
            2
        )

        left = ctk.CTkFrame(
            tab,
            fg_color="#17181d",
            border_width=1,
            border_color="#30323a",
            corner_radius=30
        )
        left.grid(row=1, column=0, padx=(22, 12), pady=14, sticky="nsew")
        left.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            left,
            text="ZEN MENU",
            font=("Segoe UI Variable Display", 31, "bold"),
            text_color="#ffffff"
        ).grid(row=0, column=0, padx=26, pady=(26, 4), sticky="w")

        ctk.CTkLabel(
            left,
            text="A Windows QOL dashboard focused on automation, cleanup, Discord/Spotify status, local tools and ZENAI.",
            font=("Segoe UI Variable", 14),
            text_color="#bfc1ca",
            justify="left",
            wraplength=520
        ).grid(row=1, column=0, padx=26, pady=(0, 18), sticky="w")

        creator_box = ctk.CTkFrame(left, fg_color="#101115", corner_radius=22, border_width=1, border_color="#2b2d34")
        creator_box.grid(row=2, column=0, padx=26, pady=(0, 22), sticky="ew")
        creator_box.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(
            creator_box,
            text="★",
            font=("Segoe UI Variable Display", 30, "bold"),
            text_color="#ffffff"
        ).grid(row=0, column=0, rowspan=2, padx=(18, 12), pady=18)

        ctk.CTkLabel(
            creator_box,
            text="Created by Zen / superstandarts",
            font=("Segoe UI Variable", 15, "bold"),
            text_color="#ffffff"
        ).grid(row=0, column=1, padx=(0, 18), pady=(18, 2), sticky="w")

        ctk.CTkLabel(
            creator_box,
            text="Discord: 7mey",
            font=("Segoe UI Variable", 13),
            text_color="#bfc1ca"
        ).grid(row=1, column=1, padx=(0, 18), pady=(0, 18), sticky="w")

        right = ctk.CTkFrame(
            tab,
            fg_color="#17181d",
            border_width=1,
            border_color="#30323a",
            corner_radius=30
        )
        right.grid(row=1, column=1, padx=(12, 22), pady=14, sticky="nsew")
        right.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            right,
            text="Social Links",
            font=("Segoe UI Variable Display", 26, "bold"),
            text_color="#ffffff"
        ).grid(row=0, column=0, padx=26, pady=(26, 12), sticky="w")

        links = [
            ("GitHub  •  superstandarts", "https://github.com/superstandarts"),
            ("Instagram  •  xyphanctinusultrazaliextremus", "https://www.instagram.com/xyphanctinusultrazaliextremus/"),
            ("Steam  •  hokurary", "https://steamcommunity.com/id/hokurary"),
            ("Roblox  •  Profile", "https://www.roblox.com/users/5583806069/profile"),
        ]

        for i, (label, url) in enumerate(links, start=1):
            self.link_button(right, label, url).grid(row=i, column=0, padx=26, pady=7, sticky="ew")

        footer = ctk.CTkFrame(tab, fg_color="#101115", border_width=1, border_color="#2b2d34", corner_radius=24)
        footer.grid(row=2, column=0, columnspan=2, padx=22, pady=(8, 22), sticky="ew")
        footer.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            footer,
            text="SYSTEM ONLINE    •    ZENAI READY    •    ACCESS GRANTED",
            font=("Cascadia Mono", 13, "bold"),
            text_color="#d7d7dc"
        ).grid(row=0, column=0, padx=22, pady=18, sticky="w")


    def _build_logs(self):
        tab = self.frames["Logs"]
        tab.grid_columnconfigure(0, weight=1)
        self.page_header(tab, "Logs", "Runtime messages and module events.", 0, 0)
        self.logbox = self.textbox(tab, height=570)
        self.logbox.grid(row=1, column=0, padx=18, pady=10, sticky="nsew")

    def log(self, msg):
        stamp = datetime.now().strftime("%H:%M:%S")
        line = f"[{stamp}] {msg}\n"
        print(line, end="")
        if hasattr(self, "logbox"):
            self.logbox.insert("end", line)
            self.logbox.see("end")

    def start_tray(self):
        ok = self.tray_manager.start()
        self.notify("Tray icon", "Tray icon started." if ok else "Tray icon unavailable.")

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
        if not messagebox.askyesno("Cleaner", "Move detected junk files to Recycle Bin?"):
            return
        def job():
            summary = self.cleaner.clean_safe()
            for item in summary:
                self.cleaner_output.insert("end", f"{item}\n")
            self.notify("Cleaner", "Safe clean completed.")
        self.run_thread(job)

    def organize_screenshots(self):
        count = self.screenshot_organizer.organize()
        self.files_output.insert("end", f"Organized screenshots: {count}\n")
        self.notify("Screenshots", f"Organized {count} screenshots.")

    def search_files(self):
        folder = filedialog.askdirectory(title="Select folder to search")
        if not folder:
            return
        query = self.search_entry.get().strip()
        results = self.smart_search.search(folder, query, limit=250)
        self.files_output.delete("1.0", "end")
        for path in results:
            self.files_output.insert("end", str(path) + "\n")
        self.log(f"Smart search found {len(results)} results.")

    def start_discord(self):
        try:
            self.discord_status.start()
            self.discord_output.insert("end", "Discord/Spotify status started.\n")
            self.notify("Discord Status", "Started.")
        except Exception as e:
            messagebox.showerror("Discord Status", str(e))

    def stop_discord(self):
        self.discord_status.stop()
        self.discord_output.insert("end", "Discord/Spotify status stopped.\n")
        self.notify("Discord Status", "Stopped.")

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
        self.automation_output.insert("end", "Safe auto clicker started. Move mouse to top-left to stop.\n")

    def stop_clicker(self):
        self.autoclicker.stop()
        self.automation_output.insert("end", "Auto clicker stopped.\n")

    def refresh_volumes(self):
        sessions = self.volume.list_sessions()
        self.volume_output.delete("1.0", "end")
        for item in sessions:
            self.volume_output.insert("end", f"{item}\n")

    def start_game_session(self):
        self.game_session.start_session()
        self.notify("Gaming", "Game session started.")

    def end_game_session(self):
        self.game_session.end_session()
        self.notify("Gaming", "Game session ended.")

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
            self.notify("README generated", save)


if __name__ == "__main__":
    app = ZenUltimateMenu()
    app.mainloop()
