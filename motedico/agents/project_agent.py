from motedico.agents.base import BaseAgent
from motedico.models import Project, Proposal, ProposalStatus
class ProjectAgent(BaseAgent):
    def __init__(self, config):
        super().__init__(config)
        self.projects = {}
    async def start(self): pass
    async def stop(self): pass
    async def create_project(self, title, description, owner):
        pid = f"prj_{len(self.projects)+1}"
        p = Project(id=pid, title=title, description=description, owner=owner)
        self.projects[pid] = p
        return p
    async def add_proposal(self, pid, author, content):
        if pid not in self.projects: raise ValueError(f"Project {pid} not found")
        pr = Proposal(id=f"pr_{len(self.projects[pid].proposals)+1}", project_id=pid, author=author, content=content)
        self.projects[pid].proposals.append(pr)
        return pr
    async def accept_proposal(self, pid, prid):
        for p in self.projects[pid].proposals:
            if p.id == prid: p.status = ProposalStatus.ACCEPTED
