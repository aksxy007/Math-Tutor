from pydantic import BaseModel,Field
from datetime import datetime
from typing import Optional,List

class Chat(BaseModel):
    userId:str
    title: Optional[str]
    createdAt: Optional[datetime] = None  # Will be assigned automatically
    messages: List[str]
    class Config:
        arbitrary_types_allowed = True