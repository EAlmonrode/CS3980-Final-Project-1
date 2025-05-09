from contextlib import asynccontextmanager
import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from starlette.responses import StreamingResponse
from io import BytesIO
from routers.admin import admin_router
from db.db_context import init_database
from routers.note import note_router
from routers.user import user_router
from routers.group import group_router
from models.my_config import get_settings
from models.note import Note 
from beanie import PydanticObjectId

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Application starts...")
    await init_database()
    yield
    print("Application shuts down...")

app = FastAPI(title="CS3980 | Group 4 | Final Project", version="2.0.0", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

app.include_router(note_router, tags=["Notes"], prefix="/notes")
app.include_router(user_router, tags=["Users"], prefix="/users")
app.include_router(group_router, tags=["Groups"], prefix="/groups")
app.include_router(admin_router)

@app.get("/todos/{note_id}/image")
async def get_note_image(note_id: PydanticObjectId):
    note = await Note.get(note_id)
    if not note or not note.image_data:
        raise HTTPException(status_code=404, detail="Image not found.")
    return StreamingResponse(BytesIO(note.image_data), media_type="image/png")

if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)

