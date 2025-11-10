from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1.router import api_router
from app.core.config import settings

app = FastAPI(
    title="Coding Assessment Platform",
    description="Online coding assessment platform with gVisor sandbox execution",
    version="1.0.0",
)

# CORS middleware - use environment variable for allowed origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API router
app.include_router(api_router, prefix="/api/v1")


@app.get("/")
async def root():
    return {
        "message": "Coding Assessment Platform API",
        "version": "1.0.0",
        "docs": "/docs",
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host=settings.host,
        port=settings.actual_port,  # Use actual_port to respect PORT env var
        reload=settings.debug,
    )

