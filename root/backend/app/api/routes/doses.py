from fastapi import APIRouter
from app.services.dose_service import (
    generate_doses,
    list_upcoming_doses,
    mark_dose_taken,
)

router = APIRouter(prefix="/doses", tags=["Doses"])


@router.post("/generate/{schedule_id}")
async def generate(schedule_id: str):
    return await generate_doses(schedule_id)


@router.get("/upcoming")
async def upcoming():
    return await list_upcoming_doses()


@router.post("/{dose_id}/take")
async def take(dose_id: str):
    return await mark_dose_taken(dose_id)
