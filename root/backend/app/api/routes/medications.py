from fastapi import APIRouter, Depends
from app.services.medication_service import add_medication

router = APIRouter()

@router.post("/medications")
async def create_medication(payload: dict):
    return await add_medication(payload)
