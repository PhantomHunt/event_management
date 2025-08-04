from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from . import schemas, crud
from .database import get_db

router = APIRouter()

@router.post("/events", response_model=schemas.EventOut)
async def create_event(
    event: schemas.EventCreate,
    db: AsyncSession = Depends(get_db)
) -> schemas.EventOut:
    """
    Create a new event.

    Args:
    -----
        event (schemas.EventCreate): Event details from the request body.
        db (AsyncSession): Injected database session.

    Returns:
    --------
        schemas.EventOut: The created event's data.
    """
    return await crud.create_event(db, event)


@router.get("/events", response_model=List[schemas.EventOut])
async def list_events(
    db: AsyncSession = Depends(get_db)
) -> List[schemas.EventOut]:
    """
    Get a list of all upcoming events (future start times only).

    Args:
    -----
        db (AsyncSession): Injected database session.

    Returns:
    --------
        List[schemas.EventOut]: List of upcoming events.
    """
    return await crud.get_upcoming_events(db)


@router.post("/events/{event_id}/register", response_model=schemas.AttendeeOut)
async def register(
    event_id: int,
    attendee: schemas.AttendeeCreate,
    db: AsyncSession = Depends(get_db)
) -> schemas.AttendeeOut:
    """
    Register an attendee for a specific event.

    Args:
    -----
        event_id (int): The ID of the event.
        attendee (schemas.AttendeeCreate): Attendee information from the request body.
        db (AsyncSession): Injected database session.

    Raises:
    -------
        HTTPException: If event is not found, full, or attendee is already registered.

    Returns:
    --------
        schemas.AttendeeOut: The newly registered attendee.
    """
    result, error = await crud.register_attendee(db, event_id, attendee)
    if error:
        raise HTTPException(status_code=400, detail=error)
    return result


@router.get("/events/{event_id}/attendees", response_model=List[schemas.AttendeeOut])
async def get_attendees(
    event_id: int,
    skip: int = 0,
    limit: int = 10,
    db: AsyncSession = Depends(get_db)
) -> List[schemas.AttendeeOut]:
    """
    Get a paginated list of attendees for a specific event.

    Args:
    -----
        event_id (int): The ID of the event.
        skip (int, optional): Number of records to skip. Defaults to 0.
        limit (int, optional): Maximum number of records to return. Defaults to 10.
        db (AsyncSession): Injected database session.

    Returns:
    --------
        List[schemas.AttendeeOut]: List of attendees for the event.
    """
    return await crud.get_event_attendees(db, event_id, skip, limit)
