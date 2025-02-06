from bson import ObjectId
async def get_chat_history(db,chatId):
    collection = db['messages']
    cursor = collection.find(
        {"chatId":chatId},  # Match the chatId
        {"_id":0,"chatId":0}  # Select fields: role, content, exclude _id
    ).sort("createdAt", -1)
    chat_history = await cursor.to_list(length=10)
    return chat_history