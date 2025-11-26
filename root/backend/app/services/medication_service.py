from datetime import datetime
from uuid import uuid4
from fastapi import HTTPException, status

from app.db.repository_factory import get_repository

repo = get_repository()


async def add_medication(payload: dict):
    """
    Business rules:
    - name is required
    - medication is active by default
    """

    print(payload,"this is the payload")
    name = payload.get("name")
    if not name:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Medication name is required",
        )

    medication = {
        "id": str(uuid4()),
        "name": name,
        "instructions": payload.get("instructions"),
        "is_active": True,
        "created_at": datetime.utcnow(),
    }

    return await repo.create("medications", medication)


async def deactivate_medication(medication_id: str):
    medication = await repo.get_by_id("medications", medication_id)
    if not medication:
        raise HTTPException(404, "Medication not found")

    return await repo.update(
        "medications",
        medication_id,
        {"is_active": False},
    )


async def list_active_medications():
    return await repo.find("medications", {"is_active": True})
