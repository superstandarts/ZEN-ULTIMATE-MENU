class VolumeController:
    def __init__(self, logger=print):
        self.logger = logger

    def list_sessions(self):
        try:
            from pycaw.pycaw import AudioUtilities, ISimpleAudioVolume
            sessions = AudioUtilities.GetAllSessions()
            output = []
            for session in sessions:
                name = session.Process.name() if session.Process else "System Sounds"
                volume = session._ctl.QueryInterface(ISimpleAudioVolume)
                output.append(f"{name}: {round(volume.GetMasterVolume() * 100)}% | muted={volume.GetMute()}")
            return output
        except Exception as e:
            return [f"Volume controller unavailable: {e}"]
