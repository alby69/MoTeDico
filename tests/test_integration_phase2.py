import pytest
import asyncio
from unittest.mock import AsyncMock, patch
from motedico.config import Settings
from motedico.agents.advisor_agent import AdvisorAgent
from motedico.models import Project

@pytest.mark.asyncio
async def test_advisor_llm_call():
    cfg = Settings(gemini_api_key="test_key")
    advisor = AdvisorAgent(cfg)

    # Mock the LLM provider
    mock_provider = AsyncMock()
    mock_provider.generate.return_value = "Advice from AI"

    with patch("motedico.agents.advisor_agent.get_llm_provider", return_value=mock_provider):
        await advisor.start()
        project = Project(id="prj_1", title="Test", description="Test", owner="User")
        proposal = await advisor.analyze_and_propose(project)

        assert proposal.content == "Advice from AI"
        mock_provider.generate.assert_called_once()

@pytest.mark.asyncio
async def test_advisor_fallback():
    # No API key should trigger fallback
    cfg = Settings()
    advisor = AdvisorAgent(cfg)
    await advisor.start()

    project = Project(id="prj_1", title="Test", description="Vacanza", owner="User")
    proposal = await advisor.analyze_and_propose(project)

    assert "Trentino" in proposal.content
