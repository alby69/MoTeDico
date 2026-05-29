import asyncio
import json
from typing import Optional, List, Dict
from motedico.agents.base import BaseAgent
from motedico.config import Settings

try:
    from nostr_sdk import (
        Client,
        Keys,
        EventBuilder,
        Tag,
        Filter,
        Event,
        Nip44Version,
        nip44_encrypt,
        nip44_decrypt,
        PublicKey,
        NostrSigner
    )
except ImportError:
    # Fallback if the environment does not have nostr-sdk installed
    Client = None

class NetworkAgent(BaseAgent):
    """
    Handles P2P identity and communication using the Nostr protocol.
    Enables agents to announce projects and proposals globally without central servers.
    """

    def __init__(self, config: Settings, secret_key: Optional[str] = None, mnemonic: Optional[str] = None):
        """
        Setup Nostr keys and client.
        :param secret_key: Optional hex string for existing identity.
        :param mnemonic: Optional mnemonic seed phrase (NIP-06).
        """
        super().__init__(config)
        if Client is None:
            self.logger.error("nostr-sdk not installed. NetworkAgent will be dysfunctional.")
            self.client = None
            return

        if mnemonic:
            # Support for NIP-06 mnemonic seed phrases
            self.keys = Keys.from_mnemonic(mnemonic)
        elif secret_key:
            self.keys = Keys.parse(secret_key)
        else:
            # Generate a new ephemeral key pair for this session
            self.keys = Keys.generate()

        # In latest nostr-sdk, Client requires a NostrSigner
        self.signer = NostrSigner.keys(self.keys)
        self.client = Client(self.signer)
        self.relays = config.nostr_relays

    async def start(self):
        """Connect to configured Nostr relays and setup relay management."""
        if not self.client:
            return
        for relay in self.relays:
            await self.client.add_relay(relay)

        # Connect to relays
        await self.client.connect()
        self.logger.info(f"Connected to Nostr as {self.keys.public_key().to_bech32()}")

    async def stop(self):
        """Disconnect from the Nostr network."""
        if self.client:
            await self.client.disconnect()

    async def publish_event(self, kind: int, content: str, tags: List[List[str]] = None):
        """
        Publishes an event to the Nostr network.
        :param kind: The Nostr event kind (e.g., 1 for text note).
        :param content: The body of the message.
        :param tags: Optional list of tags for metadata.
        """
        if not self.client:
            self.logger.warning("Client not initialized. Simulating event.")
            return f"mock_event_id_{kind}"

        nostr_tags = []
        if tags:
            for t in tags:
                nostr_tags.append(Tag.parse(t))

        event = EventBuilder(kind, content, nostr_tags).to_event(self.signer)
        event_id = await self.client.send_event(event)
        self.logger.info(f"Published event kind {kind}: {event_id.to_bech32()}")
        return event_id.to_bech32()

    async def publish_file_metadata(self, url: str, mime: str, sha256: str, alt: str = ""):
        """
        Implementation of NIP-94 (File Metadata) for multimedia attachments.
        """
        if not self.client:
            return

        tags = [
            ["url", url],
            ["m", mime],
            ["x", sha256],
            ["alt", alt],
            ["t", "motedico_attachment"]
        ]

        return await self.publish_event(1063, alt, tags)

    async def send_private_proposal(self, receiver_pubkey_bech32: str, proposal_data: Dict):
        """
        Sends an encrypted proposal (Pull Request) using NIP-44.
        :param receiver_pubkey_bech32: The bech32 public key (npub...) of the project owner.
        :param proposal_data: Dictionary containing the proposal details.
        """
        if not self.client:
            self.logger.warning("Client not initialized. Cannot send private message.")
            return

        receiver_pubkey = PublicKey.parse(receiver_pubkey_bech32)
        content = json.dumps(proposal_data)

        # NIP-44 encryption
        encrypted_content = nip44_encrypt(self.keys.secret_key(), receiver_pubkey, content, Nip44Version.V2)

        tags = [["p", receiver_pubkey.to_hex()]]
        return await self.publish_event(4, encrypted_content, tags)

    async def decrypt_private_message(self, sender_pubkey_bech32: str, encrypted_content: str) -> Optional[Dict]:
        """
        Decrypts a private message using NIP-44.
        """
        if not self.client:
            return None

        sender_pubkey = PublicKey.parse(sender_pubkey_bech32)
        try:
            decrypted_json = nip44_decrypt(self.keys.secret_key(), sender_pubkey, encrypted_content)
            return json.loads(decrypted_json)
        except Exception as e:
            self.logger.error(f"Decryption failed: {e}")
            return None
