from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from . import schemas, crud
from .database import get_db

router = APIRouter()

@router.post("/events", response_model=schemas.EventOut)
async def create_event(event: schemas.EventCreate, db: AsyncSession = Depends(get_db)):
    return await crud.create_event(db, event)

@router.get("/events", response_model=List[schemas.EventOut])
async def list_events(db: AsyncSession = Depends(get_db)):
    return await crud.get_upcoming_events(db)

@router.post("/events/{event_id}/register", response_model=schemas.AttendeeOut)
async def register(event_id: int, attendee: schemas.AttendeeCreate, db: AsyncSession = Depends(get_db)):
    result, error = await crud.register_attendee(db, event_id, attendee)
    if error:
        raise HTTPException(status_code=400, detail=error)
    return result

@router.get("/events/{event_id}/attendees", response_model=List[schemas.AttendeeOut])
async def get_attendees(event_id: int, skip: int = 0, limit: int = 10, db: AsyncSession = Depends(get_db)):
    return await crud.get_event_attendees(db, event_id, skip, limit)
