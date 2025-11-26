from datetime import datetime, timedelta
from uuid import uuid4
from fastapi import HTTPException

from app.db.repository_factory import get_repository

repo = get_repository()


async def generate_doses(schedule_id: str, days: int = 7):
    """
    Generates upcoming doses for a schedule
    """
    schedule = await repo.get_by_id("schedules", schedule_id)
    if not schedule:
        raise HTTPException(404, "Schedule not found")

    medication_id = schedule["medication_id"]
    times = schedule["times"]
    recurrence = schedule["recurrence"]
    days_of_week = schedule.get("days_of_week")

    now = datetime.utcnow()
    doses_created = []

    for day_offset in range(days):
        current_day = now + timedelta(days=day_offset)

        if recurrence == "weekly":
            if current_day.weekday() not in (days_of_week or []):
                continue

        for time_str in times:
            hour, minute = map(int, time_str.split(":"))
            dose_time = current_day.replace(
                hour=hour, minute=minute, second=0, microsecond=0
            )

            if dose_time < now:
                continue

            dose = {
                "id": str(uuid4()),
                "medication_id": medication_id,
                "schedule_id": schedule_id,
                "dose_time": dose_time,
                "taken": False,
                "taken_at": None,
            }

            doses_created.append(
                await repo.create("doses", dose)
            )

    return doses_created


async def list_upcoming_doses(limit: int = 20):
    now = datetime.utcnow()
    doses = await repo.find("doses", {"taken": False})
    upcoming = [d for d in doses if d["dose_time"] >= now]
    return sorted(upcoming, key=lambda x: x["dose_time"])[:limit]


async def mark_dose_taken(dose_id: str):
    dose = await repo.get_by_id("doses", dose_id)
    if not dose:
        raise HTTPException(404, "Dose not found")

    if dose["taken"]:
        raise HTTPException(409, "Dose already marked as taken")

    return await repo.update(
        "doses",
        dose_id,
        {
            "taken": True,
            "taken_at": datetime.utcnow(),
        },
    )
