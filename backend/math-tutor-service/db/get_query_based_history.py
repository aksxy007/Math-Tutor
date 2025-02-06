async def get_relevant_past_messages(db, chatId, query, limit=5):
    collection = db['messages']
    cursor = collection.find(
        {"chatId": chatId, "content": {"$regex": query, "$options": "i"}},  # Case-insensitive search
        {"_id": 0, "chatId": 0}
    ).limit(limit)
    relevant_messages = await cursor.to_list(length=limit)
    return relevant_messages
