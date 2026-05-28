import pytest
from motedico.models import Project, Proposal, ProjectStatus, ProposalStatus

def test_project_model():
    project = Project(
        title="Test Project",
        description="A test description",
        owner="test_user"
    )
    assert project.title == "Test Project"
    assert project.status == ProjectStatus.OPEN
    assert len(project.proposals) == 0

def test_proposal_model():
    proposal = Proposal(
        project_id="prj_1",
        author="advisor_agent",
        content="This is advice"
    )
    assert proposal.project_id == "prj_1"
    assert proposal.status == ProposalStatus.PENDING

def test_project_with_proposals():
    proposal = Proposal(
        project_id="prj_1",
        author="advisor_agent",
        content="This is advice"
    )
    project = Project(
        id="prj_1",
        title="Test Project",
        description="A test description",
        owner="test_user",
        proposals=[proposal]
    )
    assert len(project.proposals) == 1
    assert project.proposals[0].content == "This is advice"
