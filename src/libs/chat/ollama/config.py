from pydantic_settings import BaseSettings
from wireup import service


class OllamaAISettings(BaseSettings):
    base_url: str = "http://localhost:11434/"
    model: str = "gpt-oss:20b"


@service
def get_ollama_ai_settings() -> OllamaAISettings:
    return OllamaAISettings()
