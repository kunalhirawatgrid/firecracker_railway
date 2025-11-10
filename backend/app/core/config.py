from pydantic_settings import BaseSettings
from typing import Optional, List


class Settings(BaseSettings):
    # Server
    host: str = "0.0.0.0"
    port: int = 8000
    debug: bool = False
    
    # CORS - in production, set specific origins
    cors_origins: str = "*"  # Comma-separated list of allowed origins
    
    # gVisor
    gvisor_runtime_path: str = "/usr/local/bin/runsc"
    gvisor_timeout: int = 60  # Increased for C++ compilation
    gvisor_memory_limit: str = "512m"
    gvisor_cpu_limit: str = "1"
    gvisor_fallback_to_docker: bool = False  # Fallback to regular Docker if gVisor unavailable
    
    # Storage
    storage_path: str = "./storage"
    
    @property
    def allowed_origins(self) -> List[str]:
        """Parse CORS origins from environment variable"""
        if self.cors_origins == "*":
            return ["*"]
        return [origin.strip() for origin in self.cors_origins.split(",") if origin.strip()]
    
    @property
    def actual_port(self) -> int:
        """Get port from PORT env var (for Railway/cloud) or use configured port"""
        import os
        return int(os.getenv("PORT", self.port))
    
    class Config:
        env_file = ".env"
        case_sensitive = False


settings = Settings()

