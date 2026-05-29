from __future__ import annotations
from pathlib import Path
from typing import Optional
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    """
    MoTeDico Configuration settings using Pydantic Settings V2.
    Loads values from environment variables or a .env file.
    """

    # === LLM Provider ===
    llm_provider: str = Field(
        default="gemini",
        description="LLM provider: gemini, openai, anthropic, ollama",
    )

    # Gemini
    gemini_api_key: str = Field(default="", description="Google Gemini API Key")
    gemini_model: str = Field(default="gemini-2.0-flash")

    # OpenAI
    openai_api_key: str = Field(default="", description="OpenAI API Key")
    openai_model: str = Field(default="gpt-4o-mini")

    # Anthropic
    anthropic_api_key: str = Field(default="", description="Anthropic API Key")
    anthropic_model: str = Field(default="claude-3-5-haiku-latest")

    # Ollama
    ollama_base_url: str = Field(default="http://localhost:11434")
    ollama_model: str = Field(default="llama3")

    # === Network ===
    nostr_relays: list[str] = Field(
        default_factory=lambda: ["wss://relay.damus.io", "wss://nos.lol", "wss://relay.snort.social"],
        description="List of Nostr relays for decentralized communication"
    )

    # === Storage ===
    ipfs_gateway_url: str = Field(
        default="https://ipfs.infura.io:5001/api/v0/add",
        description="IPFS API endpoint for uploading files"
    )
    ipfs_project_id: str = Field(default="", description="IPFS Project ID (e.g. Infura)")
    ipfs_project_secret: str = Field(default="", description="IPFS Project Secret")
    output_dir: Path = Field(default=Path("./output"), description="Directory for local data storage")

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        case_sensitive=False,
    )

    def validate(self):
        """Validates that necessary API keys are present based on the selected provider."""
        missing = []
        if self.llm_provider == "gemini" and not self.gemini_api_key:
            missing.append("GEMINI_API_KEY")
        elif self.llm_provider == "openai" and not self.openai_api_key:
            missing.append("OPENAI_API_KEY")
        elif self.llm_provider == "anthropic" and not self.anthropic_api_key:
            missing.append("ANTHROPIC_API_KEY")
        if missing:
            raise ValueError(f"Missing required env vars: {', '.join(missing)}")
