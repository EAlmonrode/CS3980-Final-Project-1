from fastapi import APIRouter, Depends, HTTPException, status
from typing import Annotated, List

from auth.jwt_auth import TokenData
from models.group import Group, GroupRequest
from routers.user import get_user
# from utils.group_permissions import ensure_group_owner, ensure_group_member
from logs.logging import logger

group_router = APIRouter()


@group_router.post("", status_code=status.HTTP_201_CREATED)
async def create_group(
    req: GroupRequest, user: Annotated[TokenData, Depends(get_user)]
) -> Group:
    new_group = Group(
        name=req.name,
        description=req.description,
        owner=user.username,
        members=[user.username],
    )
    await new_group.create()
    logger.info(f"User {user.username} created group {req.name}")
    return new_group


@group_router.get("/my", response_model=List[Group])
async def get_my_groups(user: Annotated[TokenData, Depends(get_user)]):
    return await Group.find(Group.members == user.username).to_list()


@group_router.post("/{group_id}/join")
async def join_group(
    group_id: str, user: Annotated[TokenData, Depends(get_user)]
):
    group = await Group.get(group_id)
    if not group:
        raise HTTPException(status_code=404, detail="Group not found.")
    
    if user.username not in group.members:
        group.members.append(user.username)
        await group.save()

    logger.info(f"User {user.username} joined {group.name}")
    return {"message": f"{user.username} joined {group.name}."}


@group_router.delete("/{group_id}")
async def delete_group(
    group_id: str, user: Annotated[TokenData, Depends(get_user)]
):
    group = await Group.get(group_id)
    if not group:
        raise HTTPException(status_code=404, detail="Group not found.")
    
    # await ensure_group_owner(group, user.username)
    await group.delete()
    
    logger.info(f"User {user.username} deleted {group.name}")
    return {"message": f"{group.name} deleted."}
