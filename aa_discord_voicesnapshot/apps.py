from django.apps import AppConfig
from django.urls import include, path


class AaDiscordVoiceSnapshotConfig(AppConfig):
    name = 'aa_discord_voicesnapshot'

    def ready(self):
        # Import the global Alliance Auth URL list
        from allianceauth.urls import urlpatterns

        # Inject this plugin's URLs into AA's main URL tree
        urlpatterns += [
            path('voicesnapshot/', include('aa_discord_voicesnapshot.urls')),
        ]
