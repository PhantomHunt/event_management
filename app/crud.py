from sqlalchemy.future import select
from sqlalchemy import func
from sqlalchemy.ext.asyncio import AsyncSession
from . import models, schemas
from sqlalchemy.orm import selectinload
from typing import Optional, Tuple

async def create_event(db: AsyncSession, event: schemas.EventCreate) -> models.Event:
    """
    Create a new event in the database.

    Args:
        db (AsyncSession): The database session.
        event (schemas.EventCreate): The event details to be created.

    Returns:
        models.Event: The newly created event instance.
    """
    db_event = models.Event(**event.dict())
    db.add(db_event)
    await db.commit()
    await db.refresh(db_event)
    return db_event


async def get_upcoming_events(db: AsyncSession) -> list[models.Event]:
    """
    Fetch all upcoming events (start time in the future), ordered chronologically.

    Args:
        db (AsyncSession): The database session.

    Returns:
        list[models.Event]: A list of upcoming event objects.
    """
    stmt = select(models.Event).where(models.Event.start_time > func.now()).order_by(models.Event.start_time)
    result = await db.execute(stmt)
    return result.scalars().all()


async def get_event_by_id(db: AsyncSession, event_id: int) -> Optional[models.Event]:
    """
    Retrieve an event by its ID.

    Args:
        db (AsyncSession): The database session.
        event_id (int): The ID of the event to retrieve.

    Returns:
        Optional[models.Event]: The event object if found, else None.
    """
    stmt = select(models.Event).filter_by(id=event_id)
    result = await db.execute(stmt)
    return result.scalar_one_or_none()


async def register_attendee(
    db: AsyncSession,
    event_id: int,
    attendee: schemas.AttendeeCreate
) -> Tuple[Optional[models.Attendee], Optional[str]]:
    """
    Register a new attendee to an event, ensuring constraints are respected.

    This function registers an attendee to the given event if:
    - The event exists
    - The event has not reached max capacity
    - The attendee is not already registered with the same email

    Args:
        db (AsyncSession): The database session.
        event_id (int): The ID of the event.
        attendee (schemas.AttendeeCreate): The attendee details.

    Returns:
        Tuple[Optional[models.Attendee], Optional[str]]:
            - On success: (attendee object, None)
            - On failure: (None, error message)
    """
    result = await db.execute(
        select(models.Event).options(selectinload(models.Event.attendees)).where(models.Event.id == event_id)
    )
    event = result.scalars().first()

    if not event:
        return None, "Event not found"

    if len(event.attendees) >= event.max_capacity:
        return None, "Event is full"

    # Check for duplicate registration
    for existing in event.attendees:
        if existing.email == attendee.email:
            return None, "Attendee already registered"

    new_attendee = models.Attendee(event_id=event_id, **attendee.dict())
    db.add(new_attendee)
    await db.commit()
    await db.refresh(new_attendee)
    return new_attendee, None

async def get_event_attendees(
    db: AsyncSession,
    event_id: int,
    skip: int = 0,
    limit: int = 10
) -> list[models.Attendee]:
    """
    Retrieve attendees for a given event with pagination support.

    Args:
        db (AsyncSession): The database session.
        event_id (int): The ID of the event.
        skip (int, optional): Number of records to skip. Defaults to 0.
        limit (int, optional): Maximum number of records to return. Defaults to 10.

    Returns:
        list[models.Attendee]: A list of attendee objects.
    """
    stmt = select(models.Attendee).filter_by(event_id=event_id).offset(skip).limit(limit)
    result = await db.execute(stmt)
    return result.scalars().all()
