
class ErrorAnalyzer:
    RULES = [
        ("ModuleNotFoundError", "A Python module is missing. Run: pip install <module> or install_requirements.bat."),
        ("FileNotFoundError", "A file path is missing or wrong. Check config.json/assets and relative paths."),
        ("TclError", "Tkinter/CustomTkinter UI error. Usually caused by mixing pack/grid or invalid widget options."),
        ("cannot use geometry manager pack", "You are mixing pack() and grid() in the same container. Use only one per parent frame."),
        ("PermissionError", "Permission denied. Try running as Administrator or close the app using the file."),
        ("Failed building wheel", "pip failed compiling a package. Upgrade pip/setuptools/wheel or use another package version."),
        ("PyInstaller", "PyInstaller build issue. Use --clean and make sure config.json/assets are next to the exe."),
        ("JSONDecodeError", "config.json is invalid. Check commas, quotes and braces."),
    ]

    def analyze(self, text):
        found = []
        for key, explanation in self.RULES:
            if key.lower() in text.lower():
                found.append(f"{key}: {explanation}")
        if not found:
            return "No known pattern detected. Paste the full traceback or ask ZENAI."
        return "\n\n".join(found)
