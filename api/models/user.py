from beanie import Document
from pydantic import BaseModel


class User(Document):
    username: str
    email: str
    password: str  # hashed password
    is_admin: bool = False

    class Settings:
        name = "users"


class UserRequest(BaseModel):
    username: str
    email: str
    password: str  # plain text


class UserDto(BaseModel):
    id: str
    username: str
    email: str
