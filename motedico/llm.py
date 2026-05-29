from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Optional
from motedico.config import Settings
from motedico.exceptions import LLMError

class LLMProvider(ABC):
    """Abstract base class for LLM providers."""
    @abstractmethod
    async def generate(self, model: str, system_prompt: str, user_prompt: str) -> str:
        """Generates text using the LLM."""
        pass

class GeminiProvider(LLMProvider):
    """Google Gemini LLM provider."""
    def __init__(self, api_key: str):
        self.api_key = api_key

    async def generate(self, model: str, system_prompt: str, user_prompt: str) -> str:
        try:
            from google import genai
            client = genai.Client(api_key=self.api_key)
            response = client.models.generate_content(
                model=model,
                contents=user_prompt,
                config={"system_instruction": system_prompt},
            )
            return response.text.strip()
        except Exception as e:
            raise LLMError(f"Gemini API error: {e}") from e

class OpenAIProvider(LLMProvider):
    """OpenAI LLM provider."""
    def __init__(self, api_key: str):
        self.api_key = api_key

    async def generate(self, model: str, system_prompt: str, user_prompt: str) -> str:
        try:
            from openai import AsyncOpenAI
            client = AsyncOpenAI(api_key=self.api_key)
            response = await client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt},
                ],
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            raise LLMError(f"OpenAI API error: {e}") from e

def get_llm_provider(cfg: Settings) -> LLMProvider:
    """Returns the configured LLM provider instance."""
    providers = {
        "gemini": lambda: GeminiProvider(cfg.gemini_api_key),
        "openai": lambda: OpenAIProvider(cfg.openai_api_key),
    }
    provider_fn = providers.get(cfg.llm_provider)
    if not provider_fn:
        raise LLMError(f"Unknown LLM provider '{cfg.llm_provider}'")
    return provider_fn()
