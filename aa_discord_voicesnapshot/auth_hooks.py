from allianceauth import hooks
from allianceauth.services.hooks import MenuItemHook, UrlHook

#
# URL HOOK
#
@hooks.register('url_hook')
def register_urls():
    return UrlHook(
        urls='aa_discord_voicesnapshot.urls',
        namespace='aa_voicesnapshot',
        base_url=r'^voicesnapshot/'
    )

#
# MENU HOOK
#
class VoiceSnapshotMenu(MenuItemHook):
    def __init__(self):
        super().__init__(
            "Discord Voice Snapshot",
            "fa fa-microphone",
            "aa_voicesnapshot:snapshot", 
        )

    def render(self, request):
        if request.user.has_perm("aa_discord_voicesnapshot.take_snapshot") or \
           request.user.has_perm("aa_discord_voicesnapshot.view_snapshot_history"):
            return super().render(request)
        return ""

@hooks.register('menu_item_hook')
def register_menu():
    return VoiceSnapshotMenu()
