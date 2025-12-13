from chromadb import Settings, Client, PersistentClient
from pydantic_settings import BaseSettings
from wireup import service

class ChromaConfig(BaseSettings):
    chroma_db_impl: str = "duckdb+parquet"
    persist_directory: str = "./chroma_db"
    anonymized_telemetry: bool = False

@service
def chroma_config() -> ChromaConfig:
    return ChromaConfig()

@service
class ChromaClient:
    def __init__(self, chroma_config: ChromaConfig):
        self.config = chroma_config
        self.connection: PersistentClient = PersistentClient(
            path=chroma_config.persist_directory
        )

