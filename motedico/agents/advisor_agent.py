import asyncio
from typing import Optional
from motedico.agents.base import BaseAgent
from motedico.config import Settings
from motedico.models import Project, Proposal

class AdvisorAgent(BaseAgent):
    """
    AI-powered agent that monitors the network for projects and
    automatically submits advice in the form of proposals (Pull Requests).
    """

    def __init__(self, config: Settings):
        super().__init__(config)

    async def start(self):
        """Start monitoring for projects."""
        self.logger.info("AdvisorAgent started.")

    async def stop(self):
        pass

    async def analyze_and_propose(self, project: Project) -> Optional[Proposal]:
        """
        Analyzes a project description and generates a suggested course of action.
        Uses configured LLM providers (Gemini/OpenAI).
        """
        self.logger.info(f"Analyzing project: {project.title}")

        # NOTE: In a production environment, this would call get_llm_provider(self.config)
        # similar to the PodcastGen translator logic.
        # For this PoC, we provide a structured heuristic advice.

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
