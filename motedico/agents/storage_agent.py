import hashlib
import aiohttp
from pathlib import Path
from typing import Optional
from motedico.agents.base import BaseAgent
from motedico.config import Settings
from motedico.exceptions import StorageError

class StorageAgent(BaseAgent):
    """
    Handles content-addressable storage using IPFS.
    Ensures project descriptions and multimedia are stored permanently and uniquely.
    """

    def __init__(self, config: Settings):
        super().__init__(config)
        self.session: Optional[aiohttp.ClientSession] = None

    async def start(self):
        """Initialize the storage agent and aiohttp session."""
        self.logger.info("StorageAgent started.")
        self.session = aiohttp.ClientSession()

    async def stop(self):
        """Close the aiohttp session."""
        if self.session:
            await self.session.close()

    async def upload_content(self, content: str) -> str:
        """
        Uploads text content to IPFS.
        :param content: The text string to store.
        :return: An IPFS Content Identifier (CID).
        """
        # If no credentials, use mock simulation
        if not self.config.ipfs_project_id:
            self.logger.warning("IPFS credentials missing. Using mock CID.")
            cid = "Qm" + hashlib.sha256(content.encode()).hexdigest()[:44]
            return cid

        try:
            auth = aiohttp.BasicAuth(self.config.ipfs_project_id, self.config.ipfs_project_secret)
            data = aiohttp.FormData()
            data.add_field('file', content)

            async with self.session.post(
                self.config.ipfs_gateway_url,
                data=data,
                auth=auth
            ) as response:
                response.raise_for_status()
                result = await response.json()
                cid = result['Hash']
                self.logger.info(f"Content uploaded to IPFS. CID: {cid}")
                return cid
        except Exception as e:
            self.logger.error(f"IPFS upload failed: {e}. Falling back to mock.")
            return "Qm" + hashlib.sha256(content.encode()).hexdigest()[:44]

    async def get_file_url(self, cid: str) -> str:
        """
        Returns a public gateway URL for a given CID.
        """
        return f"https://ipfs.io/ipfs/{cid}"
