import os
from typing import Optional
from pydantic import BaseModel
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Settings(BaseModel):
    """Application settings loaded from environment variables"""
    
    def __init__(self, **kwargs):
        # Load all settings from environment variables
        super().__init__(
            # Azure OpenAI Settings
            AZURE_OPENAI_ENDPOINT=os.getenv('AZURE_OPENAI_ENDPOINT', ''),
            AZURE_OPENAI_KEY=os.getenv('AZURE_OPENAI_KEY', ''),
            AZURE_OPENAI_DEPLOYMENT_NAME=os.getenv('AZURE_OPENAI_DEPLOYMENT_NAME', 'gpt-4'),
            AZURE_OPENAI_API_VERSION=os.getenv('AZURE_OPENAI_API_VERSION', '2023-12-01-preview'),
            
            # Azure Search Settings
            AZURE_SEARCH_ENDPOINT=os.getenv('AZURE_SEARCH_ENDPOINT', ''),
            AZURE_SEARCH_KEY=os.getenv('AZURE_SEARCH_KEY', ''),
            AZURE_SEARCH_INDEX=os.getenv('AZURE_SEARCH_INDEX', 'retail-index'),
            
            # Application Settings
            LOG_LEVEL=os.getenv('LOG_LEVEL', 'INFO'),
            MAX_RETRIES=int(os.getenv('MAX_RETRIES', '3')),
            TIMEOUT_SECONDS=int(os.getenv('TIMEOUT_SECONDS', '30')),
            **kwargs
        )
    
    # Azure OpenAI Settings
    AZURE_OPENAI_ENDPOINT: str = ""
    AZURE_OPENAI_KEY: str = ""
    AZURE_OPENAI_DEPLOYMENT_NAME: str = "gpt-4"
    AZURE_OPENAI_API_VERSION: str = "2023-12-01-preview"
    
    # Azure Search Settings
    AZURE_SEARCH_ENDPOINT: str = ""
    AZURE_SEARCH_KEY: str = ""
    AZURE_SEARCH_INDEX: str = "retail-index"
    
    # Application Settings
    LOG_LEVEL: str = "INFO"
    MAX_RETRIES: int = 3
    TIMEOUT_SECONDS: int = 30

# Create a global settings instance
settings = Settings()