from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class Chat(BaseModel):
    chatId:int
    userId:int
    role:str
    content:str
    createdAt: Optional[datetime] = None  # Will be assigned automatically

    class Config:
        arbitrary_types_allowed = True