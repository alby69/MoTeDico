import asyncio
import json
from typing import Optional, List
from motedico.agents.base import BaseAgent
from motedico.config import Settings

try:
    from nostr_sdk import (
        Client,
        Keys,
        EventBuilder,
        Tag,
        Filter,
        Event
    )
except ImportError:
    Client = None

class NetworkAgent(BaseAgent):
    """Handles communication via Nostr."""

    def __init__(self, config: Settings, secret_key: Optional[str] = None):
        super().__init__(config)
        if Client is None:
            self.logger.error("nostr-sdk not installed.")
            self.client = None
            return

        if secret_key:
            self.keys = Keys.parse(secret_key)
        else:
            self.keys = Keys.generate()

        self.client = Client(self.keys)
        self.relays = config.nostr_relays

    async def start(self):
        if not self.client:
            return
        for relay in self.relays:
            await self.client.add_relay(relay)
        await self.client.connect()
        self.logger.info(f"Connected to Nostr as {self.keys.public_key().to_bech32()}")

    async def stop(self):
        if self.client:
            await self.client.disconnect()

    async def publish_event(self, kind: int, content: str, tags: List[List[str]] = None):
        """Publishes an event to Nostr."""
        if not self.client:
            self.logger.warning("Client not initialized. Simulating event.")
            return f"mock_event_id_{kind}"

        nostr_tags = []
        if tags:
            for t in tags:
                nostr_tags.append(Tag.parse(t))

        event = EventBuilder(kind, content, nostr_tags).to_event(self.keys)
        event_id = await self.client.send_event(event)
        self.logger.info(f"Published event kind {kind}: {event_id.to_bech32()}")
        return event_id.to_bech32()
