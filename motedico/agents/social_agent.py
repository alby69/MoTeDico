from motedico.agents.base import BaseAgent
from motedico.config import Settings

class SocialAgent(BaseAgent):
    """Monitors interactions and provides community feedback."""

    def __init__(self, config: Settings):
        super().__init__(config)

    async def start(self):
        self.logger.info("SocialAgent monitoring project activity...")

    async def stop(self):
        pass

    async def react_to_project(self, project_id: str):
        """Simulates a community reaction to a new project."""
        self.logger.info(f"Community is interested in project {project_id}! +5 upvotes.")
        await self.emit_event("community_reaction", {"project_id": project_id, "reaction": "upvote", "count": 5})

    async def react_to_proposal(self, proposal_id: str):
        """Simulates a community reaction to a new proposal."""
        self.logger.info(f"The community thinks proposal {proposal_id} is very helpful!")
        await self.emit_event("community_reaction", {"proposal_id": proposal_id, "reaction": "helpful"})
