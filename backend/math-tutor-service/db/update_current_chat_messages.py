from models.Chat import Chat
from typing import List
from bson import ObjectId

async def update_current_chat_messages(db,chatId:str,messageIds:List[ObjectId]):
    collection = db['chats']
    # messageObjectIds = [ObjectId(msg_id) for msg_id in messageIds]
    result = await collection.find_one_and_update(
        {"_id":ObjectId(chatId)},
        {"$push":{"messages":{"$each":messageIds}}},
    )
    return {"message":"Chat fetched successfully","current_chat":result}