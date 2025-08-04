from fastapi import FastAPI
from .router import router
from .database import engine, Base
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield

app = FastAPI(title="Mini Event Management System", lifespan=lifespan)
app.include_router(
    router,
    prefix="/event_management",
    tags=["Mini Event Management"],)
