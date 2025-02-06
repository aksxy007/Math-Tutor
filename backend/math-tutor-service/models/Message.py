from pydantic import BaseModel
from typing import Optional
from datetime import datetime

# Message Model
class Message(BaseModel):
    chatId: str
    role: str  # 'user' or 'assistant'
    content: str
    createdAt: Optional[datetime] = None  # Will be assigned automatically

    class Config:
        arbitrary_types_allowed = True