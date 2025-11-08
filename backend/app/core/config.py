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
    
    # Storage settings (JSON file storage)
    STORAGE_FILE: str = Field(
        default="data.json",
        env="STORAGE_FILE"
    )
    
    # Firecracker settings
    FIRECRACKER_SOCKET_PATH: str = Field(
        default="/tmp/firecracker.socket",
        env="FIRECRACKER_SOCKET_PATH"
    )
    FIRECRACKER_KERNEL_PATH: str = Field(
        default="/opt/firecracker/vmlinux.bin",
        env="FIRECRACKER_KERNEL_PATH"
    )
    FIRECRACKER_ROOTFS_PATH: str = Field(
        default="/opt/firecracker/rootfs.ext4",
        env="FIRECRACKER_ROOTFS_PATH"
    )
    FIRECRACKER_VM_TIMEOUT_SECONDS: int = Field(
        default=30,
        env="FIRECRACKER_VM_TIMEOUT_SECONDS"
    )
    FIRECRACKER_MAX_MEMORY_MB: int = Field(
        default=512,
        env="FIRECRACKER_MAX_MEMORY_MB"
    )
    FIRECRACKER_VCPU_COUNT: int = Field(
        default=2,
        env="FIRECRACKER_VCPU_COUNT"
    )
    
    # Code execution settings
    MAX_CODE_LENGTH: int = Field(default=50000, env="MAX_CODE_LENGTH")  # 50KB max
    MAX_EXECUTION_TIME_MS: int = Field(default=10000, env="MAX_EXECUTION_TIME_MS")  # 10 seconds
    MAX_STDOUT_SIZE: int = Field(default=100000, env="MAX_STDOUT_SIZE")  # 100KB max stdout

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

