from allianceauth.services.hooks import MenuItemHook

class VoiceSnapshotMenu(MenuItemHook):
    def __init__(self):
        super().__init__(
            "aa_discord_voicesnapshot:snapshot",   # URL name FIRST
            "Discord Voice Snapshot",              # Label SECOND
            "fa fa-microphone"                     # Icon THIRD
        )

    def render(self, request):
        if request.user.has_perm("aa_discord_voicesnapshot.take_snapshot") or \
           request.user.has_perm("aa_discord_voicesnapshot.view_snapshot_history"):
            return super().render(request)
        return ""
