
async def get_chat_history(db,chatId):
    collection = db['chats']
    cursor = collection.find(
        {"chatId": chatId},  # Match the chatId
        {"_id":0,"chatId":0,"userId":0}  # Select fields: role, content, exclude _id
    ).sort("createdAt", -1)
    chat_history = await cursor.to_list(length=10)
    return {"message":"Chat inserted successgully","chat_history":chat_history}