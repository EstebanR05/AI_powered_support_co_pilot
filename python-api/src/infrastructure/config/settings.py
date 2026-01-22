import os
from functools import lru_cache
from pydantic_settings import BaseSettings
from pydantic import ConfigDict
from typing import Optional

class Settings(BaseSettings):
    """
    Configuración de la aplicación
    Usa Pydantic Settings para validación y type hints
    """
    
    model_config = ConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False
    )
    
    # Environment
    environment: str = "development"
    
    # Server
    host: str = "0.0.0.0"
    port: int = 8000
    
    # Security
    secret_key: str = "your-secret-key-change-in-production"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    
    # Supabase
    supabase_url: Optional[str] = None
    supabase_key: Optional[str] = None
    supabase_service_key: Optional[str] = None
    
    # AI Configuration
    gemini_api_key: Optional[str] = None
    gemini_model: str = "gemini-pro"
    
    # External Services
    n8n_webhook_url: Optional[str] = None
    
    # Application
    use_in_memory_db: bool = True
    
    @property
    def is_development(self) -> bool:
        return self.environment == "development"
    
    @property
    def is_production(self) -> bool:
        return self.environment == "production"
    
    @property
    def has_supabase_config(self) -> bool:
        return bool(self.supabase_url and self.supabase_key)
    
    @property
    def has_gemini_config(self) -> bool:
        return bool(self.gemini_api_key and self.gemini_api_key != "your_gemini_api_key")

@lru_cache()
def get_settings() -> Settings:
    """
    Cached settings instance
    """
    return Settings()