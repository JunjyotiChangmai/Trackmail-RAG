from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional

class Settings(BaseSettings):
    OPENAI_API_KEY: Optional[str] = ""
    COLLECTION_NAME: str = "my_collection"
    DATASET_PATH: str = "TrackMail_RAG_Dataset.docx"
    
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

settings = Settings()