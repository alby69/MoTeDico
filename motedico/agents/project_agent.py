import json
from typing import Dict, List
from motedico.agents.base import BaseAgent
from motedico.config import Settings
from motedico.models import Project, Proposal, ProjectStatus, ProposalStatus

class ProjectAgent(BaseAgent):
    """Manages project lifecycle and proposal tracking."""

    def __init__(self, config: Settings):
        super().__init__(config)
        self.projects: Dict[str, Project] = {}

    async def start(self):
        self.logger.info("ProjectAgent started.")

    async def stop(self):
        pass

    async def create_project(self, title: str, description: str, owner: str) -> Project:
        """Creates a new project and broadcasts it."""
        project_id = f"prj_{len(self.projects) + 1}"
        project = Project(id=project_id, title=title, description=description, owner=owner)
        self.projects[project_id] = project

        await self.emit_event("project_created", project.model_dump())
        return project

    async def add_proposal(self, project_id: str, author: str, content: str) -> Proposal:
        """Adds a proposal (PR) to a project."""
        if project_id not in self.projects:
            raise ValueError(f"Project {project_id} not found.")

        project = self.projects[project_id]
        proposal_id = f"pr_{len(project.proposals) + 1}"
        proposal = Proposal(id=proposal_id, project_id=project_id, author=author, content=content)

        project.proposals.append(proposal)
        await self.emit_event("proposal_received", proposal.model_dump())
        return proposal

    async def accept_proposal(self, project_id: str, proposal_id: str):
        """Accepts (merges) a proposal into the project."""
        if project_id not in self.projects:
            raise ValueError(f"Project {project_id} not found.")

        project = self.projects[project_id]
        for prop in project.proposals:
            if prop.id == proposal_id:
                prop.status = ProposalStatus.ACCEPTED
                self.logger.info(f"Proposal {proposal_id} accepted for project {project_id}")
                await self.emit_event("proposal_accepted", {"project_id": project_id, "proposal_id": proposal_id})
                return

        raise ValueError(f"Proposal {proposal_id} not found in project {project_id}")
