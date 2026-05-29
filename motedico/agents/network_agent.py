import asyncio
import json
from typing import Optional, List, Dict
from motedico.agents.base import BaseAgent
from motedico.config import Settings

try:
    from nostr_sdk import (
        Client, Keys, EventBuilder, Tag, Filter, Event,
        Nip44Version, nip44_encrypt, nip44_decrypt, PublicKey, NostrSigner, RelayUrl
    )
except ImportError:
    Client = None

class NetworkAgent(BaseAgent):
    def __init__(self, config: Settings, secret_key: Optional[str] = None, mnemonic: Optional[str] = None):
        super().__init__(config)
        if Client is None:
            self.client = None
            return

        if mnemonic:
            self.keys = Keys.from_mnemonic(mnemonic)
        elif secret_key:
            self.keys = Keys.parse(secret_key)
        else:
            self.keys = Keys.generate()

        self.signer = NostrSigner.keys(self.keys)
        self.client = Client(self.signer)
        self.relays = config.nostr_relays

    async def start(self):
        if not self.client: return
        for relay in self.relays:
            # FIX: Convert string to RelayUrl
            await self.client.add_relay(RelayUrl.parse(relay))
        await self.client.connect()
        self.logger.info(f"Connected to Nostr as {self.keys.public_key().to_bech32()}")

    async def stop(self):
        if self.client: await self.client.disconnect()

    async def publish_event(self, kind: int, content: str, tags: List[List[str]] = None):
        if not self.client:
            self.logger.warning("Client not initialized. Simulating event.")
            return f"mock_event_id_{kind}"

        nostr_tags = [Tag.parse(t) for t in tags] if tags else []
        event = EventBuilder(kind, content, nostr_tags).to_event(self.signer)
        event_id = await self.client.send_event(event)
        self.logger.info(f"Published event kind {kind}: {event_id.to_bech32()}")
        return event_id.to_bech32()

    async def publish_file_metadata(self, url: str, mime: str, sha256: str, alt: str = ""):
        tags = [["url", url], ["m", mime], ["x", sha256], ["alt", alt], ["t", "motedico_attachment"]]
        return await self.publish_event(1063, alt, tags)

    async def send_private_proposal(self, receiver_pubkey_bech32: str, proposal_data: Dict):
        if not self.client: return
        receiver_pubkey = PublicKey.parse(receiver_pubkey_bech32)
        content = json.dumps(proposal_data)
        encrypted_content = nip44_encrypt(self.keys.secret_key(), receiver_pubkey, content, Nip44Version.V2)
        tags = [["p", receiver_pubkey.to_hex()]]
        return await self.publish_event(4, encrypted_content, tags)

    async def decrypt_private_message(self, sender_pubkey_bech32: str, encrypted_content: str) -> Optional[Dict]:
        if not self.client: return None
        sender_pubkey = PublicKey.parse(sender_pubkey_bech32)
        try:
            decrypted_json = nip44_decrypt(self.keys.secret_key(), sender_pubkey, encrypted_content)
            return json.loads(decrypted_json)
        except Exception as e:
            self.logger.error(f"Decryption failed: {e}")
            return None
