from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    pinecone_api_key: str
    pinecone_environment: str
    pinecone_index_name: str = "personal-assistant"
    llm_api_url: Optional[str] = None
    llm_api_key: Optional[str] = None
    openai_api_key: Optional[str] = None
    embedding_model: str = "sentence-transformers/all-MiniLM-L6-v2"
    
    class Config:
        env_file = ".env"

settings = Settings()
