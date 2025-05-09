from beanie import PydanticObjectId
from fastapi import APIRouter, Depends, Path, HTTPException, status
from fastapi import UploadFile, File, Form, Depends
from auth.jwt_auth import TokenData
from models.note import Note, NoteRequest
from models.group import Group  # Import your Group model
import base64
from typing import Annotated
from typing import Optional
import traceback
from routers.user import get_user
from logs.logging import logger
import uuid
import os

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

note_router = APIRouter()

@note_router.post("")
async def add_new_note(
    user: Annotated[TokenData, Depends(get_user)],
    name: Annotated[str, Form()],
    description: Annotated[str, Form()],
    group_id: Annotated[Optional[str], Form()] = None,
    file: Annotated[UploadFile | None, File()] = None,
) -> Note:
    image_data = await file.read() if file else None

    new_note = Note(
        name=name,
        description=description,
        group_id=group_id,
        created_by=user.username,
        image_data=image_data
    )

    await new_note.create()
    logger.info(f"User {user.username} created note '{name}' in group '{group_id}'")
    return {
        "message": "Note created successfully",
        "note_id": str(new_note.id),
        "name": new_note.name,
        "description": new_note.description,
        "group_id": new_note.group_id,
        "created_by": new_note.created_by,
        "has_image": bool(image_data)
    }


@note_router.get("")
async def get_all_notes(user: Annotated[TokenData, Depends(get_user)]) -> list[Note]:
    return await Note.find_all().to_list()


@note_router.get("/my")
async def get_my_notes(user: Annotated[TokenData, Depends(get_user)]) -> list[dict]:
    if not user or not user.username:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Please login.",
        )

    notes = await Note.find(Note.created_by == user.username).to_list()

    return [
        {
            **note.model_dump(mode="json", exclude={"image_data"}),
            "image_data": base64.b64encode(note.image_data).decode("utf-8") if note.image_data else None
        }
        for note in notes
    ]

@note_router.get("/{id}")
async def get_note_by_id(
    id: PydanticObjectId, user: Annotated[TokenData, Depends(get_user)]
) -> Note:
    note = await Note.get(id)
    if note:
        return note
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"The note with ID={id} is not found.",
    )


@note_router.delete("/{id}")
async def delete_note_by_id(
    id: PydanticObjectId, user: Annotated[TokenData, Depends(get_user)]
) -> dict:
    note = await Note.get(id)
    if not note:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"The note with ID={id} is not found.",
        )

    # Check if user is creator of note
    if note.created_by == user.username:
        await note.delete()
        logger.info(f"User {user.username} deleted note with id {id}")
        return {"message": "Note deleted."}

    # If not creator, check if user is owner of the group
    if note.group_id:
        group = await Group.get(note.group_id)
        if group and group.owner == user.username:
            await note.delete()
            logger.info(f"Owner user {user.username} deleted note with id {id}")
            return {"message": "Note deleted by group owner."}

    logger.error(f"User {user.username} attempted to delete note with id {id}")
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="You do not have permission to delete this note.",
    )
