"""
API v1 router.
"""
from fastapi import APIRouter
from app.api.v1.endpoints import health, example

api_router = APIRouter()

# Include endpoint routers
api_router.include_router(health.router, tags=["health"])
api_router.include_router(example.router, tags=["example"])

