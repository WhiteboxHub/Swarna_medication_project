from datetime import datetime, timedelta
from uuid import uuid4
from fastapi import HTTPException

from app.db.repository_factory import get_repository

repo = get_repository()

SUPPORTED_RECURRENCES = {"daily", "weekly", "multiple_times_per_day"}


async def create_schedule(payload: dict):
    """
    payload example:
    {
      "medication_id": "uuid",
      "recurrence": "daily",
      "times": ["08:00", "20:00"],
      "days_of_week": [0,1,2]   # only for weekly
    }
    """
    medication_id = payload.get("medication_id")
    recurrence = payload.get("recurrence")
    times = payload.get("times")

    if not medication_id:
        raise HTTPException(400, "medication_id is required")

    if recurrence not in SUPPORTED_RECURRENCES:
        raise HTTPException(400, "Unsupported recurrence type")

    if not times or not isinstance(times, list):
        raise HTTPException(400, "times must be a non-empty list")

    medication = await repo.get_by_id("medications", medication_id)
    if not medication or not medication["is_active"]:
        raise HTTPException(404, "Medication not found or inactive")

    schedule = {
        "id": str(uuid4()),
        "medication_id": medication_id,
        "recurrence": recurrence,
        "times": times,
        "days_of_week": payload.get("days_of_week"),
        "created_at": datetime.utcnow(),
    }

    return await repo.create("schedules", schedule)


async def list_schedules_for_medication(medication_id: str):
    return await repo.find(
        "schedules",
        {"medication_id": medication_id},
    )
