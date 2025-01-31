from models.Chat import Chat
from typing import List
async def insert_chat(db,chats:List[Chat]):
    collection = db['chats']
    chat_dicts = [chat.dict() for chat in chats]
    result = await collection.insert_many(chat_dicts)
    return {"message":"Chat inserted successgully","result":result}