from fastapi import APIRouter
from app.services.schedule_service import (
    create_schedule,
    list_schedules_for_medication,
)

router = APIRouter(prefix="/schedules", tags=["Schedules"])


@router.post("/add")
async def create(payload: dict):
    print(payload)
    return await create_schedule(payload)


@router.get("/medication/{medication_id}")
async def list_for_medication(medication_id: str):
    return await list_schedules_for_medication(medication_id)
