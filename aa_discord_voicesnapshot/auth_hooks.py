from allianceauth import hooks
from allianceauth.services.hooks import MenuItemHook
from allianceauth.hooks import UrlHook

#
# URL HOOK
#
@hooks.register('url_hook')
def register_urls():
    return UrlHook(
        'aa_discord_voicesnapshot.urls',   # module
        'aa_discord_voicesnapshot',        # app_name
        'voicesnapshot'                    # prefix
    )

#
# MENU HOOK
#
class VoiceSnapshotMenu(MenuItemHook):
    def __init__(self):
        super().__init__(
            "Discord Voice Snapshot",
            "fa fa-microphone",
            "voicesnapshot:snapshot",       # FIXED namespace
        )

    def render(self, request):
        if request.user.has_perm("aa_discord_voicesnapshot.take_snapshot") or \
           request.user.has_perm("aa_discord_voicesnapshot.view_snapshot_history"):
            return super().render(request)
        return ""

@hooks.register('menu_item_hook')
def register_menu():
    return VoiceSnapshotMenu()
