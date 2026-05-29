import hashlib
from pathlib import Path
from typing import Optional
from motedico.agents.base import BaseAgent
from motedico.config import Settings

class StorageAgent(BaseAgent):
    """
    Handles content-addressable storage using IPFS.
    Ensures project descriptions and multimedia are stored permanently and uniquely.
    """

    def __init__(self, config: Settings):
        super().__init__(config)

    async def start(self):
        """Initialize the storage agent."""
        self.logger.info("StorageAgent started.")

    async def stop(self):
        pass

    async def upload_content(self, content: str) -> str:
        """
        Simulates uploading text content to IPFS.
        :param content: The text string to 'store'.
        :return: A mock IPFS Content Identifier (CID).
        """
        # In a real implementation, this would post to an IPFS node or Pinning service
        cid = "Qm" + hashlib.sha256(content.encode()).hexdigest()[:44]
        self.logger.info(f"Content stored with CID: {cid}")
        return cid

    async def get_file_url(self, cid: str) -> str:
        """
        Returns a public gateway URL for a given CID.
        """
        return f"https://ipfs.io/ipfs/{cid}"
