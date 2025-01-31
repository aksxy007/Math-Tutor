from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class Query(BaseModel):
    chatId: int
    userId: int
    query: str
    createdAt: Optional[datetime] = None  # Will be assigned automatically

    class Config:
        arbitrary_types_allowed = True