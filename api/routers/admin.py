from fastapi import APIRouter, Depends, HTTPException, status
from beanie import PydanticObjectId
from typing import Annotated

from auth.jwt_auth import TokenData
from routers.user import get_user
from models.user import User
from models.group import Group
from models.note import Note
from logs.logging import logger

admin_router = APIRouter(prefix="/admin", tags=["Admin"])

async def ensure_admin(user: TokenData):
    db_user = await User.find_one(User.username == user.username)
    if not db_user or not db_user.is_admin:
        logger.info(f"Non-Admin {user.username} tried to go to admin page")
        raise HTTPException(status_code=403, detail="Admin access only")


@admin_router.get("/users")
async def get_all_users(user: Annotated[TokenData, Depends(get_user)]):
    await ensure_admin(user)
    return await User.find_all().to_list()


@admin_router.get("/groups")
async def get_all_groups(user: Annotated[TokenData, Depends(get_user)]):
    await ensure_admin(user)
    return await Group.find_all().to_list()


@admin_router.get("/notes")
async def get_all_notes(user: Annotated[TokenData, Depends(get_user)]):
    await ensure_admin(user)
    return await Note.find_all().to_list()

@admin_router.delete("/notes/{note_id}")
async def delete_note_by_id(
    note_id: PydanticObjectId, 
    user: Annotated[TokenData, Depends(get_user)]
) -> dict:
    await ensure_admin(user)

    note = await Note.get(note_id)
    if not note:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"The note with ID={note_id} is not found.",
        )

    await note.delete()

    logger.info(f"User {user.username} deleted note with id {note_id}")

    return {"message": f"Note with ID={note_id} deleted successfully."}

