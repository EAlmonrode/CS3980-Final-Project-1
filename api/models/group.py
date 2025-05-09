from beanie import Document
from pydantic import BaseModel, Field
from typing import List
from fastapi import HTTPException, status


async def ensure_group_owner(group, username: str):
    if group.owner != username:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only the group owner can perform this action."
        )


async def ensure_group_member(group, username: str):
    if username not in group.members:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You must be a group member to access this."
        )
        

class Group(Document):
    name: str
    description: str
    owner: str  # username of the owner
    members: List[str] = Field(default_factory=list)

    class Settings:
        name = "groups"


class GroupRequest(BaseModel):
    name: str
    description: str
