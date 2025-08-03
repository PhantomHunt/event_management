from sqlalchemy.future import select
from sqlalchemy import and_, func
from sqlalchemy.ext.asyncio import AsyncSession
from . import models, schemas

async def create_event(db: AsyncSession, event: schemas.EventCreate):
    db_event = models.Event(**event.dict())
    db.add(db_event)
    await db.commit()
    await db.refresh(db_event)
    return db_event

async def get_upcoming_events(db: AsyncSession):
    stmt = select(models.Event).where(models.Event.start_time > func.now()).order_by(models.Event.start_time)
    result = await db.execute(stmt)
    return result.scalars().all()

async def get_event_by_id(db: AsyncSession, event_id: int):
    stmt = select(models.Event).filter_by(id=event_id)
    result = await db.execute(stmt)
    return result.scalar_one_or_none()

async def register_attendee(db: AsyncSession, event_id: int, attendee: schemas.AttendeeCreate):
    event = await get_event_by_id(db, event_id)
    if not event:
        return None, "Event not found"

    if len(event.attendees) >= event.max_capacity:
        return None, "Event is full"

    stmt = select(models.Attendee).where(and_(models.Attendee.email == attendee.email, models.Attendee.event_id == event_id))
    existing = await db.execute(stmt)
    if existing.scalar_one_or_none():
        return None, "Duplicate registration"

    db_attendee = models.Attendee(**attendee.dict(), event_id=event_id)
    db.add(db_attendee)
    await db.commit()
    await db.refresh(db_attendee)
    return db_attendee, None

async def get_event_attendees(db: AsyncSession, event_id: int, skip: int = 0, limit: int = 10):
    stmt = select(models.Attendee).filter_by(event_id=event_id).offset(skip).limit(limit)
    result = await db.execute(stmt)
    return result.scalars().all()