from allianceauth.services.hooks import MenuItemHook

class VoiceSnapshotMenu(MenuItemHook):
    def __init__(self):
        super().__init__(
            "Discord Voice Snapshot",      # text
            "fa fa-microphone",            # icon
            "voicesnapshot:snapshot",      # CORRECT url_name
        )


    def render(self, request):
        if request.user.has_perm("aa_discord_voicesnapshot.take_snapshot") or \
           request.user.has_perm("aa_discord_voicesnapshot.view_snapshot_history"):
            return super().render(request)
        return ""
