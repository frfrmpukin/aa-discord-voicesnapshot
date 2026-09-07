from django.apps import AppConfig
from django.urls import include, path
import threading

class AaDiscordVoiceSnapshotConfig(AppConfig):
    name = 'aa_discord_voicesnapshot'

    def ready(self):
        # Register URLs
        from allianceauth.urls import urlpatterns
        urlpatterns += [
            path('voicesnapshot/', include('aa_discord_voicesnapshot.urls')),
        ]

        # Start Discord voice gateway listener
        from .gateway import VoiceGatewayClient
        client = VoiceGatewayClient()
        client.start()
