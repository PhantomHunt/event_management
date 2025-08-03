import pytest
from httpx import AsyncClient
from app.main import app

@pytest.mark.asyncio
async def test_create_event():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        res = await ac.post("/events", json={
            "name": "Test_event",
            "location": "Bangalore",
            "start_time": "2025-09-01T10:00:00",
            "end_time": "2025-09-01T18:00:00",
            "max_capacity": 100
        })
        assert res.status_code == 200
        assert res.json()["name"] == "Test_event"