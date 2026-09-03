from django.apps import AppConfig
from allianceauth import hooks
from .navigation import VoiceSnapshotMenu

class AADiscordVoiceSnapshotConfig(AppConfig):
    name = "aa_discord_voicesnapshot"
    verbose_name = "Discord Voice Snapshot"

    def ready(self):
        hooks.register(VoiceSnapshotMenu())
