from pydantic import BaseModel, validator
from datetime import datetime
import pytz
import os

TIMEZONE = os.getenv("TIMEZONE", "Asia/Kolkata")

class EventCreate(BaseModel):
    name: str
    location: str
    start_time: datetime
    end_time: datetime
    max_capacity: int

    @validator("start_time", "end_time", pre=True)
    def convert_ist(cls, v):
        if isinstance(v, str):
            v = datetime.fromisoformat(v)
        if v.tzinfo is None:
            return pytz.timezone(TIMEZONE).localize(v)
        return v.astimezone(pytz.timezone(TIMEZONE))

class EventOut(BaseModel):
    id: int
    name: str
    location: str
    start_time: datetime
    end_time: datetime
    max_capacity: int

    class Config:
        orm_mode = True

class AttendeeCreate(BaseModel):
    name: str
    email: str

class AttendeeOut(BaseModel):
    id: int
    name: str
    email: str

    class Config:
        orm_mode = True