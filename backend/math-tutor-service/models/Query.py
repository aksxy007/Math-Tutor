from pydantic import BaseModel

class Query(BaseModel):
    chatId: str
    userId: str
    query: str