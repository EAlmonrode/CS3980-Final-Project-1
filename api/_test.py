import pytest
from httpx import AsyncClient
from httpx._transports.asgi import ASGITransport
from main import app
from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
from models.note import Note
from models.group import Group
from models.user import User
from datetime import datetime, timezone, timedelta
from auth.jwt_auth import TokenData
from routers.user import get_user
from models.my_config import get_settings

def override_get_user():
    return TokenData(
        username="testuser",
        role="user",
        exp_datetime=datetime.now(timezone.utc) + timedelta(hours=1)
    )

app.dependency_overrides[get_user] = override_get_user
transport = ASGITransport(app=app)

async def manual_db_init():
    my_config = get_settings()
    client = AsyncIOMotorClient(my_config.connection_string)
    db = client["finalProject"]
    await init_beanie(database=db, document_models=[Note, Group, User])

@pytest.mark.asyncio
async def test_create_note():
    await manual_db_init()
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.post("/notes", data={  
            "name": "Test Note",
            "description": "This is a test note.",
            "group_id": ""
        })
    assert response.status_code in [200, 201]

@pytest.mark.asyncio
async def test_get_notes():
    await manual_db_init()
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get("/notes/my") 
    assert response.status_code == 200
    assert isinstance(response.json(), list)

@pytest.mark.asyncio
async def test_create_group():
    await manual_db_init()
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.post("/groups", json={
            "name": "Test Group",
            "description": "For testing"
        })
    assert response.status_code in [200, 201]

@pytest.mark.asyncio
async def test_get_groups():
    await manual_db_init()
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get("/groups/my")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

@pytest.mark.asyncio
async def test_get_users():
    await manual_db_init()
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get("/users")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert any(user["username"] == "testuser" for user in data)



