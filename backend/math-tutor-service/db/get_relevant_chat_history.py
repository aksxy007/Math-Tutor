from db.get_chat_history import get_chat_history
from db.get_query_based_history import get_relevant_past_messages

async def get_contextual_chat_history(db, chatId, user_query):
    recent_messages = await get_chat_history(db, chatId)
    relevant_messages = await get_relevant_past_messages(db, chatId, user_query)
    
    # Merge and sort messages by createdAt
    combined_history = sorted(recent_messages + relevant_messages, key=lambda x: x["createdAt"])
    return combined_history
