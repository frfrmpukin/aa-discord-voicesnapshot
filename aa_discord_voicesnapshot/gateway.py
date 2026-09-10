"""
aa_discord_voicesnapshot.gateway

Reworked to:
 - Defer Django model imports until runtime to allow importing the package
   in contexts where Django settings are not configured.
 - Resolve Discord token at runtime from environment or Django settings.
 - Allow explicit token injection for tests/CI.
 - Log token prefix (first 8 chars) for debugging without exposing full secret.
"""

from __future__ import annotations

import os
import logging
import threading
import time
import json
from typing import Optional, Any

# Keep local imports minimal at module import time.
# Defer Django/model imports until runtime to avoid requiring DJANGO_SETTINGS_MODULE
# when importing the package for tests or CLI tools.

log = logging.getLogger(__name__)

# Default values that can be overridden at runtime
DEFAULT_GATEWAY_VERSION = 10
DEFAULT_INTENTS = 0  # set as needed by your implementation

# Helper: import models only when needed
def _import_models():
    """
    Import Django models lazily. Call this only after Django is configured.
    """
    try:
        from .models import VoiceState  # type: ignore
    except Exception as exc:
        # Re-raise with context so callers can handle it
        raise RuntimeError("Failed to import aa_discord_voicesnapshot.models; "
                           "ensure Django is configured before using model-backed features") from exc
    return VoiceState

# Helper: resolve token from environment or Django settings
def _get_token_from_env_or_settings() -> str:
    """
    Resolve the Discord bot token. Preference order:
      1. DISCORD_TOKEN environment variable
      2. Django settings.DISCORD_BOT_TOKEN
    Raises RuntimeError if no token is found.
    """
    token = os.environ.get("DISCORD_TOKEN")
    if token:
        try:
            log.debug("Resolved DISCORD token from environment; prefix=%s", token[:8])
        except Exception:
            log.debug("Resolved DISCORD token from environment")
        return token

    # Lazy import of Django settings to avoid import-time dependency
    try:
        from django.conf import settings  # type: ignore
    except Exception:
        raise RuntimeError("Django settings not available and DISCORD_TOKEN env var not set")

    token = getattr(settings, "DISCORD_BOT_TOKEN", None)
    if token:
        try:
            log.debug("Resolved DISCORD token from Django settings; prefix=%s", token[:8])
        except Exception:
            log.debug("Resolved DISCORD token from Django settings")
        return token

    raise RuntimeError("No Discord token found: set DISCORD_TOKEN env var or DISCORD_BOT_TOKEN in Django settings")

# Helper: resolve guild id (optional)
def _get_guild_id_from_env_or_settings() -> Optional[str]:
    gid = os.environ.get("VOICESNAPSHOT_GUILD_ID")
    if gid:
        return gid
    try:
        from django.conf import settings  # type: ignore
        return getattr(settings, "VOICESNAPSHOT_GUILD_ID", None)
    except Exception:
        return None

# Minimal gateway client skeleton
class VoiceGatewayClient(threading.Thread):
    """
    VoiceGatewayClient runs in its own thread and manages the connection to Discord's gateway
    for the voice snapshot plugin.

    Usage:
      client = VoiceGatewayClient()  # token resolved from env or settings
      client.start()
      client.join()

    Or for tests:
      client = VoiceGatewayClient(token="test-token")
    """

    def __init__(self, token: Optional[str] = None, guild_id: Optional[str] = None, *args: Any, **kwargs: Any):
        super().__init__(daemon=True)
        # Token may be provided explicitly (useful for tests/CI).
        # If not provided, resolve at runtime.
        self._explicit_token = token
        self._token: Optional[str] = None
        self._guild_id = guild_id or _get_guild_id_from_env_or_settings()
        self._VoiceState = None  # will be set by _ensure_models()
        self._running = threading.Event()
        self._connected = threading.Event()
        self._ws = None  # placeholder for websocket connection object
        self._lock = threading.RLock()

        # internal state
        self._identify_payload = None

        log.debug("VoiceGatewayClient initialized (token_provided=%s, guild_id=%s)",
                  bool(token), self._guild_id)

    # Public API: allow token injection before start
    @property
    def token(self) -> str:
        if self._token is None:
            if self._explicit_token:
                self._token = self._explicit_token
                try:
                    log.debug("Using explicit token provided to VoiceGatewayClient; prefix=%s", self._token[:8])
                except Exception:
                    log.debug("Using explicit token provided to VoiceGatewayClient")
            else:
                self._token = _get_token_from_env_or_settings()
        return self._token

    def _ensure_models(self):
        if self._VoiceState is None:
            self._VoiceState = _import_models()
        return self._VoiceState

    # Example connect method (non-blocking)
    def connect(self) -> None:
        """
        Prepare and attempt to connect to the Discord gateway.
        This method should be safe to call from a context where Django settings are configured.
        """
        log.info("VoiceGatewayClient.connect() called")
        # Ensure token resolution happens here (not at import time)
        try:
            _ = self.token  # triggers resolution
        except Exception as exc:
            log.exception("Token resolution failed in connect(): %s", exc)
            raise

        # If your implementation needs models, ensure they are imported now
        try:
            self._ensure_models()
        except RuntimeError:
            # If models are not required for a particular run, you can ignore or log
            log.debug("Models not available or not required at connect time")

        # The real implementation would open a websocket and identify
        # For safety in this drop-in, we only set flags and log.
        self._running.set()
        log.info("VoiceGatewayClient marked running; ready to start gateway loop")

    # Thread run loop
    def run(self) -> None:
        """
        Thread entrypoint. This method blocks until the client stops.
        """
        log.info("VoiceGatewayClient thread starting")
        try:
            # Ensure token is resolved before attempting network operations
            _ = self.token
        except Exception:
            log.exception("VoiceGatewayClient cannot start: token resolution failed")
            return

        # If models are needed for runtime, import them now
        try:
            self._ensure_models()
        except RuntimeError:
            log.debug("VoiceGatewayClient continuing without models")

        # Example loop: replace with actual gateway connect/receive logic
        self._running.set()
        try:
            while self._running.is_set():
                # Placeholder: actual implementation should manage websocket lifecycle,
                # heartbeats, identify, resume, event handling, etc.
                log.debug("VoiceGatewayClient heartbeat (guild=%s)", self._guild_id)
                time.sleep(5)
        except Exception:
            log.exception("Unhandled exception in VoiceGatewayClient run loop")
        finally:
            log.info("VoiceGatewayClient thread exiting")
            self._running.clear()

    def start(self) -> None:
        """
        Start the client thread and attempt to connect.
        """
        log.debug("VoiceGatewayClient.start() called")
        # Call connect path first to fail fast if token missing
        self.connect()
        super().start()
        log.info("VoiceGatewayClient thread started")

    def stop(self) -> None:
        """
        Stop the client loop and wait for thread to exit.
        """
        log.info("VoiceGatewayClient.stop() called")
        self._running.clear()
        # If there is a websocket, close it here (implementation-specific)
        # e.g. await self._ws.close() in async code or self._ws.close() for sync libs

    # Convenience for join
    def join(self, timeout: Optional[float] = None) -> None:
        log.debug("VoiceGatewayClient.join(timeout=%s) called", timeout)
        super().join(timeout)

    # Representation
    def __repr__(self) -> str:
        token_present = bool(self._explicit_token or os.environ.get("DISCORD_TOKEN"))
        return f"<VoiceGatewayClient(token_present={token_present}, guild_id={self._guild_id})>"
