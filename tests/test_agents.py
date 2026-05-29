import pytest
import asyncio
from motedico.config import Settings
from motedico.agents.project_agent import ProjectAgent
from motedico.agents.advisor_agent import AdvisorAgent
from motedico.models import ProjectStatus, ProposalStatus

@pytest.mark.asyncio
async def test_project_advisor_flow():
    cfg = Settings()
    project_agent = ProjectAgent(cfg)
    advisor_agent = AdvisorAgent(cfg)

    # Create project
    project = await project_agent.create_project("Test", "Vacanza", "Owner")
    assert project.id == "prj_1"

    # Generate proposal
    proposal = await advisor_agent.analyze_and_propose(project)
    assert proposal.project_id == "prj_1"
    assert "Trentino" in proposal.content

    # Add proposal to project
    await project_agent.add_proposal(project.id, proposal.author, proposal.content)
    assert len(project_agent.projects["prj_1"].proposals) == 1

    # Accept proposal
    await project_agent.accept_proposal("prj_1", "pr_1")
    assert project_agent.projects["prj_1"].proposals[0].status == ProposalStatus.ACCEPTED

@pytest.mark.asyncio
async def test_project_not_found():
    cfg = Settings()
    project_agent = ProjectAgent(cfg)
    with pytest.raises(ValueError, match="not found"):
        await project_agent.add_proposal("non_existent", "author", "content")
