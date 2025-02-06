from models.Message import Message
from typing import List
async def insert_messages(db,messages:List[Message]):
    collection = db['messages']
    message_dicts = [message.dict() for message in messages]
    result = await collection.insert_many(message_dicts)
    return result