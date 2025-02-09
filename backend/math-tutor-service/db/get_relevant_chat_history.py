from db.get_chat_history import get_chat_history
from db.get_query_based_history import get_relevant_past_messages

async def get_contextual_chat_history(db,chatCache, chatId, user_query):
    chat_history_cache = chatCache.get_chat_history(chatId=chatId)
    relevant_messages = await get_relevant_past_messages(db, chatId, user_query)
    if chat_history_cache:
        print("Fetched chat history from cache")
        combined_history = sorted(chat_history_cache + relevant_messages, key=lambda x: x["createdAt"]) 
    else:
        print("Fetching chat history from db")
        recent_messages = await get_chat_history(db, chatId)
        combined_history = sorted(recent_messages + relevant_messages, key=lambda x: x["createdAt"])
    
    return combined_history
