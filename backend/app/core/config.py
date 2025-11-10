from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    # Server
    host: str = "0.0.0.0"
    port: int = 8000
    debug: bool = False
    
    # gVisor
    gvisor_runtime_path: str = "/usr/local/bin/runsc"
    gvisor_timeout: int = 60  # Increased for C++ compilation
    gvisor_memory_limit: str = "512m"
    gvisor_cpu_limit: str = "1"
    gvisor_fallback_to_docker: bool = False  # Fallback to regular Docker if gVisor unavailable
    
    # Storage
    storage_path: str = "./storage"
    
    class Config:
        env_file = ".env"
        case_sensitive = False


settings = Settings()

