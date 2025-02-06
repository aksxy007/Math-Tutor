from models.Chat import Chat
from typing import List
import json
async def create_new_chat(db,chat:Chat):
    collection = db['chats']
    chatDoc = chat.dict()
    result = await collection.insert_one(chatDoc)
    chatId=str(result.inserted_id)
    return {"message":"Chat inserted successfully","chatId":chatId}