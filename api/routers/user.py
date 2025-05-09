from typing import Annotated
from beanie import PydanticObjectId
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from passlib.context import CryptContext
from models.note import Note, NoteRequest
from models.group import Group

from auth.jwt_auth import (
    Token,
    TokenData,
    create_access_token,
    decode_jwt_token,
)
from models.user import User, UserDto, UserRequest
from logs.logging import logger

pwd_context = CryptContext(schemes=["bcrypt"])


class HashPassword:
    def create_hash(self, password: str):
        return pwd_context.hash(password)

    def verify_hash(self, input_password: str, hashed_password: str):
        return pwd_context.verify(input_password, hashed_password)


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="users/sign-in")
hash_password = HashPassword()


def get_user(token: Annotated[str, Depends(oauth2_scheme)]) -> TokenData:
    return decode_jwt_token(token)


user_router = APIRouter()

@user_router.get("/admin/overview")
async def admin_dashboard(user: Annotated[TokenData, Depends(get_user)]):
    db_user = await User.find_one(User.username == user.username)
    if not db_user or not db_user.is_admin:
        raise HTTPException(status_code=403, detail="Admins only.")

    users = await User.find_all().to_list()
    notes = await Note.find_all().to_list()
    groups = await Group.find_all().to_list()

    return {
        "users": [u.dict() for u in users],
        "notes": [n.dict() for n in notes],
        "groups": [g.dict() for g in groups],
    }


@user_router.post("/signup")
async def sign_up(user: UserRequest):
    existing_user = await User.find_one(User.username == user.username)

    if existing_user:
        logger.error(f"User with {user.username} already created")
        raise HTTPException(status_code=400, detail="User already exists.")        

    hashed_pwd = hash_password.create_hash(user.password)
    new_user = User(username=user.username, email=user.email, password=hashed_pwd)
    await new_user.create()
    logger.info(f"User {user.username} created successfully")
    return {"message": "User created successfully."}


@user_router.post("/sign-in")
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
) -> Token:
    username = form_data.username
    existing_user = await User.find_one(User.username == username)
    if not existing_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
        )

    authenticated = hash_password.verify_hash(
        form_data.password, existing_user.password
    )
    if authenticated:
        access_token = create_access_token(
            {"username": username, "is_admin": existing_user.is_admin}
        )
        logger.info(f"User {username} logged in successfully")
        return Token(access_token=access_token)
    
    logger.error(f"User unsuccessfully attempted to login with username {username}")
    raise HTTPException(status_code=401, detail="Invalid username or password")


@user_router.get("")
async def get_all_users(user: Annotated[TokenData, Depends(get_user)]) -> list[UserDto]:
    users = await User.find_all().to_list()
    return [
        UserDto(id=str(u.id), username=u.username, email=u.email)
        for u in users
    ]

@user_router.get("/me")
async def get_current_user(user: Annotated[TokenData, Depends(get_user)]):
    db_user = await User.find_one(User.username == user.username)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found.")
    
    return {
        "username": db_user.username,
        "email": db_user.email,
        "is_admin": db_user.is_admin,
    }

