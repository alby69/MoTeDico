import hashlib
import aiohttp
from pathlib import Path
from typing import Optional
from motedico.agents.base import BaseAgent
from motedico.config import Settings
from motedico.exceptions import StorageError

class StorageAgent(BaseAgent):
    def __init__(self, config: Settings):
        super().__init__(config)
        self.session: Optional[aiohttp.ClientSession] = None

    async def start(self):
        self.logger.info("StorageAgent started.")
        self.session = aiohttp.ClientSession()

    async def stop(self):
        if self.session:
            await self.session.close()

    async def upload_content(self, content: str) -> str:
        if not self.config.ipfs_project_id:
            self.logger.warning("IPFS credentials missing. Using mock CID.")
            return "Qm" + hashlib.sha256(content.encode()).hexdigest()[:44]

        try:
            auth = aiohttp.BasicAuth(self.config.ipfs_project_id, self.config.ipfs_project_secret)
            data = aiohttp.FormData()
            data.add_field('file', content)

            async with self.session.post(self.config.ipfs_gateway_url, data=data, auth=auth) as response:
                response.raise_for_status()
                result = await response.json()
                cid = result['Hash']
                self.logger.info(f"Content uploaded to IPFS. CID: {cid}")
                return cid
        except Exception as e:
            self.logger.error(f"IPFS upload failed: {e}. Falling back to mock.")
            return "Qm" + hashlib.sha256(content.encode()).hexdigest()[:44]

    async def get_file_url(self, cid: str) -> str:
        return f"https://ipfs.io/ipfs/{cid}"
