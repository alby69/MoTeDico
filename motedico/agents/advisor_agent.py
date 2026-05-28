import asyncio
from typing import Optional
from motedico.agents.base import BaseAgent
from motedico.config import Settings
from motedico.models import Project, Proposal

class AdvisorAgent(BaseAgent):
    """AI Agent that provides automated advice for projects."""

    def __init__(self, config: Settings):
        super().__init__(config)

    async def start(self):
        self.logger.info("AdvisorAgent started.")

    async def stop(self):
        pass

    async def analyze_and_propose(self, project: Project) -> Optional[Proposal]:
        """Analyzes a project and returns a Proposal."""
        self.logger.info(f"Analyzing project: {project.title}")

        # In a real scenario, this would call an LLM (Gemini/OpenAI)
        # For the PoC, we will simulate the LLM response

        advice = f"Ecco un consiglio per il tuo progetto '{project.title}': "
        if "vacanza" in project.description.lower():
            advice += "Considera il Trentino Alto Adige per luglio, è fresco e pieno di sentieri per ogni budget."
        else:
            advice += "Assicurati di definire bene le tappe e il budget per ogni fase."

        proposal = Proposal(
            project_id=project.id,
            author="AI_Advisor",
            content=advice
        )

        await self.emit_event("ai_proposal_generated", proposal.model_dump())
        return proposal
