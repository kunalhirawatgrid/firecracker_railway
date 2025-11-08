"""
Example endpoints.
"""
from fastapi import APIRouter
from typing import Dict

router = APIRouter()


@router.get("/example")
async def get_example() -> Dict[str, str]:
    """Example GET endpoint."""
    return {"message": "This is an example endpoint"}


@router.post("/example")
async def post_example(data: Dict) -> Dict:
    """Example POST endpoint."""
    return {"received": data, "message": "Data received successfully"}

