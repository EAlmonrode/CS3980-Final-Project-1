from beanie import init_beanie
from models.note import Note
from models.my_config import get_settings
from motor.motor_asyncio import AsyncIOMotorClient

from models.user import User
from models.group import Group


async def init_database():
    my_config = get_settings()
    client = AsyncIOMotorClient(my_config.connection_string)
    db = client["finalProject"]
    await init_beanie(database=db, document_models=[Note, User, Group])