"""
Application configuration using Pydantic settings.
"""
from typing import List, Union
from pydantic_settings import BaseSettings
from pydantic import Field, field_validator


class Settings(BaseSettings):
    """Application settings."""

    PROJECT_NAME: str = Field(default="Firecracker Railway API", env="PROJECT_NAME")
    VERSION: str = Field(default="1.0.0", env="VERSION")
    API_V1_STR: str = Field(default="/api/v1", env="API_V1_STR")
    
    # CORS settings - must be set in .env
    CORS_ORIGINS: Union[List[str], str] = Field(
        default="",
        env="CORS_ORIGINS",
        description="Comma-separated list of allowed CORS origins"
    )
    
    # Server settings
    HOST: str = Field(default="0.0.0.0", env="HOST")
    PORT: int = Field(default=8000, env="PORT")
    DEBUG: bool = Field(default=False, env="DEBUG")

    @field_validator("CORS_ORIGINS", mode="before")
    @classmethod
    def parse_cors_origins(cls, v: Union[str, List[str]]) -> List[str]:
        """Parse CORS origins from string or list."""
        if isinstance(v, str):
            origins = [origin.strip() for origin in v.split(",") if origin.strip()]
            if not origins:
                raise ValueError("CORS_ORIGINS must be set in .env file")
            return origins
        if isinstance(v, list):
            if not v:
                raise ValueError("CORS_ORIGINS must be set in .env file")
            return v
        raise ValueError("CORS_ORIGINS must be set in .env file")

    class Config:
        """Pydantic config."""

        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True


settings = Settings()

