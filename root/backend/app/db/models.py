from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime


class Medication(BaseModel):
    id: str
    name: str
    instructions: Optional[str]
    is_active: bool = True
    created_at: datetime = Field(default_factory=datetime.utcnow)


class MedicationSchedule(BaseModel):
    id: str
    medication_id: str
    recurrence: str  # daily | weekly | times_per_day
    times: List[str]  # "08:00", "13:00" ...
    days_of_week: Optional[List[int]] = None  # for weekly
    created_at: datetime = Field(default_factory=datetime.utcnow)


class DoseEvent(BaseModel):
    id: str
    medication_id: str
    schedule_id: str
    dose_time: datetime
    taken: bool = False
    taken_at: Optional[datetime] = None
