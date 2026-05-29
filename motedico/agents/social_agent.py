from motedico.agents.base import BaseAgent
from motedico.config import Settings

class SocialAgent(BaseAgent):
    """
    Manages social interactions, reactions (upvotes), and community graph
    without central databases, leveraging Nostr.
    """

    def __init__(self, config: Settings):
        super().__init__(config)

    async def start(self):
        """Begin monitoring decentralized feed for project activity."""
        self.logger.info("SocialAgent monitoring project activity...")

    async def stop(self):
        pass

    async def react_to_project(self, project_id: str):
        """
        Simulates a community reaction to a new project.
        :param project_id: The ID of the project being reacted to.
        """
        self.logger.info(f"Community is interested in project {project_id}! +5 upvotes.")
        await self.emit_event("community_reaction", {"project_id": project_id, "reaction": "upvote", "count": 5})

    async def react_to_proposal(self, proposal_id: str):
        """
        Simulates a community reaction to a specific proposal.
        """
        self.logger.info(f"The community thinks proposal {proposal_id} is very helpful!")
        await self.emit_event("community_reaction", {"proposal_id": proposal_id, "reaction": "helpful"})
