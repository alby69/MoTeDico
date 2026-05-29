import asyncio
import logging
from typing import Optional
from motedico.agents.base import BaseAgent
from motedico.config import Settings
from motedico.models import Project, Proposal
from motedico.llm import get_llm_provider

ADVISOR_SYSTEM_PROMPT = """Sei un esperto consulente di progetti.
Il tuo compito è analizzare la descrizione di un progetto e fornire un consiglio pratico,
concreto e creativo sotto forma di una "Proposta" (simile a una Pull Request).

REGOLE:
- Sii sintetico ma esaustivo.
- Fornisci passi azionabili.
- Usa un tono professionale ma amichevole.
- Rispondi in italiano."""

class AdvisorAgent(BaseAgent):
    """
    AI-powered agent that monitors the network for projects and
    automatically submits advice in the form of proposals (Pull Requests).
    """

    def __init__(self, config: Settings):
        """Initialize the advisor with LLM capabilities."""
        super().__init__(config)
        self.provider = None

    async def start(self):
        """Start monitoring and initialize LLM provider."""
        self.logger.info("AdvisorAgent started.")
        try:
            self.provider = get_llm_provider(self.config)
        except Exception as e:
            self.logger.error(f"Failed to initialize LLM provider: {e}")

    async def stop(self):
        pass

    async def analyze_and_propose(self, project: Project) -> Optional[Proposal]:
        """
        Analyzes a project description and generates a suggested course of action.
        Uses configured LLM providers (Gemini/OpenAI).
        """
        self.logger.info(f"Analyzing project: {project.title}")

        user_prompt = f"Progetto: {project.title}\nDescrizione: {project.description}"

        # In PoC mode or if provider fails, we use a fallback
        if not self.provider or (not self.config.gemini_api_key and not self.config.openai_api_key):
            self.logger.warning("LLM Provider not fully configured. Using fallback advice.")
            advice = self._generate_fallback_advice(project)
        else:
            try:
                model = self.config.gemini_model if self.config.llm_provider == "gemini" else self.config.openai_model
                advice = await self.provider.generate(model, ADVISOR_SYSTEM_PROMPT, user_prompt)
            except Exception as e:
                self.logger.error(f"LLM generation failed: {e}. Using fallback.")
                advice = self._generate_fallback_advice(project)

        proposal = Proposal(
            project_id=project.id,
            author="AI_Advisor",
            content=advice
        )

        await self.emit_event("ai_proposal_generated", proposal.model_dump())
        return proposal

    def _generate_fallback_advice(self, project: Project) -> str:
        """Heuristic-based fallback advice."""
        advice = f"Ecco un consiglio per il tuo progetto '{project.title}': "
        if "vacanza" in project.description.lower():
            advice += "Considera il Trentino Alto Adige per luglio, è fresco e pieno di sentieri per ogni budget."
        else:
            advice += "Assicurati di definire bene le tappe e il budget per ogni fase del tuo progetto."
        return advice
