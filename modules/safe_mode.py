
class SafeMode:
    def __init__(self, argv):
        self.enabled = any(arg.lower() in ["--safe", "/safe", "-safe"] for arg in argv)

    def status(self):
        if self.enabled:
            return "SAFE MODE ENABLED: startup sound, Discord, Spotify, tray and automation should not auto-start."
        return "Safe Mode is off. Launch with --safe to enable."
