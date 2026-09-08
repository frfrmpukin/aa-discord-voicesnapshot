import json
import threading
import websocket
import time
import logging

from django.conf import settings
from django.utils import timezone

from .models import VoiceState

log = logging.getLogger(__name__)

GATEWAY_URL = "wss://gateway.discord.gg/?v=10&encoding=json"


class VoiceGatewayClient(threading.Thread):
    def __init__(self):
        super().__init__(daemon=True)
        self.ws = None
        self.heartbeat_interval = None
        self.last_seq = None
        self.running = True

    def run(self):
        while self.running:
            try:
                self.connect()
                self.listen()
            except Exception as e:
                log.error(f"Voice gateway crashed: {e}")
                time.sleep(5)

    def connect(self):
        self.ws = websocket.WebSocket()
        self.ws.connect(GATEWAY_URL)

        # Receive HELLO packet
        hello = json.loads(self.ws.recv())
        self.heartbeat_interval = hello["d"]["heartbeat_interval"] / 1000

        # IDENTIFY packet (Discord Gateway v10 compliant)
        identify = {
            "op": 2,
            "d": {
                "token": settings.DISCORD_BOT_TOKEN,
                "intents": 1 << 2,  # GUILD_VOICE_STATES
                "capabilities": 4096,  # REQUIRED for voice state subscriptions
                "properties": {
                    "$os": "linux",
                    "$browser": "AA-VoiceSnapshot",
                    "$device": "AA-VoiceSnapshot"
                }
            }
        }

        self.ws.send(json.dumps(identify))

        # Start heartbeat thread
        threading.Thread(target=self.heartbeat, daemon=True).start()

    def heartbeat(self):
        while self.running:
            try:
                self.ws.send(json.dumps({"op": 1, "d": self.last_seq}))
            except Exception:
                return
            time.sleep(self.heartbeat_interval)

    def listen(self):
        while self.running:
            msg = self.ws.recv()
            if not msg:
                continue

            payload = json.loads(msg)
            op = payload.get("op")
            t = payload.get("t")
            d = payload.get("d")
            self.last_seq = payload.get("s")

            if t == "VOICE_STATE_UPDATE":
                self.handle_voice_state(d)

    def handle_voice_state(self, d):
        user_id = int(d["user_id"])
        channel_id = d.get("channel_id")

        VoiceState.objects.update_or_create(
            user_id=user_id,
            defaults={"channel_id": channel_id}
        )

        log.debug(f"Voice update: {user_id} -> {channel_id}")
