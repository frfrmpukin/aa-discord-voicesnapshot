from allianceauth import hooks
from allianceauth.services.hooks import UrlHook


@hooks.register('url_hook')
def register_urls():
    return UrlHook(
        app_name='aa_discord_voicesnapshot',
        urlconf='aa_discord_voicesnapshot.urls',
        prefix='voicesnapshot/'
    )
