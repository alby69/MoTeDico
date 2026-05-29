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
pa = ProjectAgent(cfg)
aa = AdvisorAgent(cfg)
sa = SocialAgent(cfg)

@asynccontextmanager
async def lifespan(app: FastAPI):
    await pa.start()
    await aa.start()
    await sa.start()
    yield
    await pa.stop()
    await aa.stop()
    await sa.stop()

app = FastAPI(title="MoTeDico Web", lifespan=lifespan)
templates = Jinja2Templates(directory="motedico/web/templates")

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse(request=request, name="index.html", context={"projects": list(pa.projects.values())})

@app.post("/projects", response_class=RedirectResponse)
async def create_project(title: str = Form(...), description: str = Form(...), owner: str = Form(...)):
    project = await pa.create_project(title, description, owner)
    await sa.react_to_project(project.id)
    # Correctly register the AI proposal by passing the ProjectAgent reference or using a closure
    asyncio.create_task(advisor_agent_logic(project.id))
    return RedirectResponse(url="/", status_code=303)

async def advisor_agent_logic(project_id: str):
    await asyncio.sleep(2)
    project = pa.projects.get(project_id)
    if project:
        proposal = await aa.analyze_and_propose(project)
        if proposal:
            # FIX: Properly add proposal to the project state
            await pa.add_proposal(project_id, proposal.author, proposal.content)
            await sa.react_to_proposal("pr_1")

@app.get("/projects/{project_id}", response_class=HTMLResponse)
async def project_details(request: Request, project_id: str):
    project = pa.projects.get(project_id)
    if not project:
        return HTMLResponse(content="Project not found", status_code=404)
    return templates.TemplateResponse(request=request, name="project.html", context={"project": project})

@app.post("/projects/{project_id}/proposals/{proposal_id}/accept", response_class=RedirectResponse)
async def accept_proposal(project_id: str, proposal_id: str):
    await pa.accept_proposal(project_id, proposal_id)
    return RedirectResponse(url=f"/projects/{project_id}", status_code=303)
