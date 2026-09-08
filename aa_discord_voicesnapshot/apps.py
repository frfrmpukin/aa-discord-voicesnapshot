from django.apps import AppConfig
from django.db.models.signals import post_migrate

def start_gateway(sender, **kwargs):
    from aa_discord_voicesnapshot.gateway import VoiceGatewayClient
    VoiceGatewayClient().start()

class AaDiscordVoiceSnapshotConfig(AppConfig):
    name = 'aa_discord_voicesnapshot'

    def ready(self):
        post_migrate.connect(start_gateway, sender=self)
