from fastapi import APIRouter
from app.api.v1.endpoints import health, assessments, execute

api_router = APIRouter()

api_router.include_router(health.router, prefix="/health", tags=["health"])
api_router.include_router(assessments.router, prefix="/assessments", tags=["assessments"])
api_router.include_router(execute.router, prefix="/execute", tags=["execute"])

