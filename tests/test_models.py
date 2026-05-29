from motedico.models import Project
def test_project(): assert Project(title="T", description="D", owner="O").title == "T"
