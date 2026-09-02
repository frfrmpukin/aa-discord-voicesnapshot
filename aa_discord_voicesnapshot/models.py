from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.db.models import JSONField


class VoiceSnapshot(models.Model):
    taken_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    timestamp = models.DateTimeField(default=timezone.now)
    channel_id = models.BigIntegerField()
    channel_name = models.CharField(max_length=255)
    occupants = JSONField()  # list of {username, user_id}

    class Meta:
        permissions = [
            ("take_snapshot", "Can take Discord voice snapshots"),
            ("view_snapshot_history", "Can view Discord snapshot history"),
            ("edit_snapshot", "Can edit Discord snapshots"),
            ("delete_snapshot", "Can delete Discord snapshots"),
        ]

    def __str__(self):
        return f"Snapshot {self.id} at {self.timestamp}"
