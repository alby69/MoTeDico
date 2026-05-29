from fastapi import FastAPI, Request, Form, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from motedico.config import Settings
from motedico.agents.project_agent import ProjectAgent
from motedico.agents.advisor_agent import AdvisorAgent
from motedico.agents.social_agent import SocialAgent
from motedico.models import ProjectStatus, ProposalStatus
import asyncio
from contextlib import asynccontextmanager

# In-memory state for the demo
cfg = Settings()
project_agent = ProjectAgent(cfg)
advisor_agent = AdvisorAgent(cfg)
social_agent = SocialAgent(cfg)

@asynccontextmanager
async def lifespan(app: FastAPI):
    await project_agent.start()
    await advisor_agent.start()
    await social_agent.start()
    yield
    await project_agent.stop()
    await advisor_agent.stop()
    await social_agent.stop()

app = FastAPI(title="MoTeDico Web", lifespan=lifespan)
templates = Jinja2Templates(directory="motedico/web/templates")

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    projects = list(project_agent.projects.values())
    return templates.TemplateResponse(request=request, name="index.html", context={"projects": projects})

@app.post("/projects", response_class=RedirectResponse)
async def create_project(title: str = Form(...), description: str = Form(...), owner: str = Form(...)):
    project = await project_agent.create_project(title, description, owner)
    # Simulate community upvote
    await social_agent.react_to_project(project.id)
    # Trigger AI advisor
    asyncio.create_task(advisor_agent_logic(project.id))
    return RedirectResponse(url="/", status_code=303)

async def advisor_agent_logic(project_id: str):
    # Wait a bit for dramatic effect in the UI
    await asyncio.sleep(2)
    project = project_agent.projects.get(project_id)
    if project:
        proposal = await advisor_agent.analyze_and_propose(project)
        if proposal:
            await project_agent.add_proposal(project_id, proposal.author, proposal.content)
            # Simulate reaction to proposal
            await social_agent.react_to_proposal("pr_1")

@app.get("/projects/{project_id}", response_class=HTMLResponse)
async def project_details(request: Request, project_id: str):
    project = project_agent.projects.get(project_id)
    if not project:
        return HTMLResponse(content="Project not found", status_code=404)
    return templates.TemplateResponse(request=request, name="project.html", context={"project": project})

@app.post("/projects/{project_id}/proposals/{proposal_id}/accept", response_class=RedirectResponse)
async def accept_proposal(project_id: str, proposal_id: str):
    await project_agent.accept_proposal(project_id, proposal_id)
    return RedirectResponse(url=f"/projects/{project_id}", status_code=303)
