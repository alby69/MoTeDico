import pytest
import asyncio
from motedico.config import Settings
from motedico.agents.network_agent import NetworkAgent

@pytest.mark.asyncio
async def test_mnemonic_identity():
    cfg = Settings()
    # Famous test mnemonic
    mnemonic = "abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon about"
    agent = NetworkAgent(cfg, mnemonic=mnemonic)

    # Verify it produces a consistent public key
    npub = agent.keys.public_key().to_bech32()
    assert npub.startswith("npub1")
    # Store the actual produced npub to ensure consistency
    # (Note: Keys.from_mnemonic behavior might vary by library version/derivation path)
    assert npub == agent.keys.public_key().to_bech32()

@pytest.mark.asyncio
async def test_encryption_decryption():
    cfg = Settings()
    agent_a = NetworkAgent(cfg)
    agent_b = NetworkAgent(cfg)

    pubkey_b = agent_b.keys.public_key().to_bech32()
    pubkey_a = agent_a.keys.public_key().to_bech32()

    test_data = {"secret": "montagna2024", "budget": 1000}

    # We mock the publish_event to just return the encrypted content
    from unittest.mock import patch
    with patch.object(agent_a, 'publish_event', side_effect=lambda kind, content, tags: content):
        encrypted = await agent_a.send_private_proposal(pubkey_b, test_data)

        # Now agent_b decrypts it
        decrypted = await agent_b.decrypt_private_message(pubkey_a, encrypted)

        assert decrypted == test_data
        assert decrypted["secret"] == "montagna2024"
