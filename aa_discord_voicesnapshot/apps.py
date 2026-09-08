from django.apps import AppConfig

class AaDiscordVoiceSnapshotConfig(AppConfig):
    name = 'aa_discord_voicesnapshot'

    def ready(self):
        from .gateway import VoiceGatewayClient
        VoiceGatewayClient().start()
