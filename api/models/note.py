import base64

from beanie import Document, PydanticObjectId
from pydantic import BaseModel
from typing import Optional
from bson import ObjectId

class Note(Document):
    name: str
    description: str
    created_by: str
    group_id: Optional[str] = None
    image_data: Optional[bytes] = None

    class Settings:
        name = "notes"

    model_config = {
        "json_encoders": {
            ObjectId: str,
            bytes: lambda b: base64.b64encode(b).decode('utf-8') if b else None
        }
    }



class NoteRequest(BaseModel):
    name: str
    description: str


