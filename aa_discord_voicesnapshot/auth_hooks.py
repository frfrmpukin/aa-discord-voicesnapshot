from allianceauth import hooks
from allianceauth.services.hooks import UrlHook, MenuItemHook


#
# URL HOOK  (YOUR AA VERSION — 3 POSITIONAL ARGUMENTS)
#
@hooks.register('url_hook')
def register_urls():
    return UrlHook(
        'aa_discord_voicesnapshot.urls',   # module
        'aa_discord_voicesnapshot',        # base_url / app_name
        'voicesnapshot'                    # prefix
    )


#
# NAVIGATION MENU HOOK
#
class VoiceSnapshotMenu(MenuItemHook):
    def __init__(self):
        super().__init__(
            "Discord Voice Snapshot",
            "aa_discord_voicesnapshot:snapshot",
            "fa fa-microphone"
        )

    def render(self, request):
        if request.user.has_perm("aa_discord_voicesnapshot.take_snapshot") or \
           request.user.has_perm("aa_discord_voicesnapshot.view_snapshot_history"):
            return super().render(request)
        return ""


@hooks.register('menu_item_hook')
def register_menu():
    return VoiceSnapshotMenu()
