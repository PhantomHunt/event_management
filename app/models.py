from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base

class Event(Base):
    __tablename__ = "events"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    location = Column(String)
    start_time = Column(DateTime(timezone=True))
    end_time = Column(DateTime(timezone=True))
    max_capacity = Column(Integer)
    attendees = relationship("Attendee", back_populates="event", cascade="all, delete")

class Attendee(Base):
    __tablename__ = "attendees"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    email = Column(String, index=True)
    event_id = Column(Integer, ForeignKey("events.id"))
    event = relationship("Event", back_populates="attendees")
