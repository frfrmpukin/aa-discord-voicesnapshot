import logging
from django.apps import AppConfig

logger = logging.getLogger(__name__)

class AaDiscordVoiceSnapshotConfig(AppConfig):
    name = "aa_discord_voicesnapshot"

    def ready(self):
        logger.info("VoiceSnapshot: AppConfig.ready() starting gateway thread")
        from aa_discord_voicesnapshot.gateway import VoiceGatewayClient
        VoiceGatewayClient().start()
