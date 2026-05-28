import hashlib
from pathlib import Path
from typing import Optional
from motedico.agents.base import BaseAgent
from motedico.config import Settings

class StorageAgent(BaseAgent):
    """Handles content storage and CID generation."""

    def __init__(self, config: Settings):
        super().__init__(config)

    async def start(self):
        self.logger.info("StorageAgent started.")

    async def stop(self):
        pass

    async def upload_content(self, content: str) -> str:
        """Simulates uploading content to IPFS and returning a CID."""
        cid = "Qm" + hashlib.sha256(content.encode()).hexdigest()[:44]
        self.logger.info(f"Content stored with CID: {cid}")
        return cid

    async def get_file_url(self, cid: str) -> str:
        """Returns a public gateway URL for a CID."""
        return f"https://ipfs.io/ipfs/{cid}"
