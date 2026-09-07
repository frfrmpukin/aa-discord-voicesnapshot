from django.apps import AppConfig
from django.urls import include, path


class AaDiscordVoiceSnapshotConfig(AppConfig):
    name = 'aa_discord_voicesnapshot'

    def ready(self):
        # Import Alliance Auth's global URL list
        from allianceauth.urls import urlpatterns

        # Register this plugin's URLs under /voicesnapshot/
        urlpatterns += [
            path('voicesnapshot/', include('aa_discord_voicesnapshot.urls')),
        ]
