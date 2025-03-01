from dotenv import load_dotenv

load_dotenv() 
import os
import redis
import json
from typing import List, Dict
from datetime import timedelta
from services.logger import logger
from zlib import compress, decompress

REDIS_URL = os.getenv("REDIS_URL","redis://localhost:6379")

class ChatCache:
    def __init__(self):
        # Initialize Redis connection
        self.redis_client = redis.StrictRedis.from_url(REDIS_URL, decode_responses=True)
        if self.redis_client!=None:
            logger.info("Connected to redis")

    def compress_data(self, data: List[Dict]) -> bytes:
        # Compress data before storing it in Redis
        return compress(json.dumps(data).encode('utf-8'))

    def decompress_data(self, data: bytes) -> List[Dict]:
        # Decompress data when retrieving it from Redis
        return json.loads(decompress(data).decode('utf-8'))

    def set_chat_history(self, chat_id: str, messages: List[Dict], max_messages: int = 10) -> None:
        # Compress the new messages before storing
        compressed_data = self.compress_data(messages)
        
        # Store the compressed messages in a Redis list
        # Push the new message to the left side of the list
        self.redis_client.lpush(chat_id, compressed_data)

        # Trim the list to keep only the latest 'max_messages' messages
        self.redis_client.ltrim(chat_id, 0, max_messages - 1)

        logger.info(f"Chat history for {chat_id} updated in Redis")

    def get_chat_history(self, chat_id: str) -> List[Dict]:
        # Get all messages for the chat from Redis
        stored_messages = self.redis_client.lrange(chat_id, 0, -1)

        if not stored_messages:
            logger.info(f"No chat history found in Redis for {chat_id}")
            return []

        # Decompress the stored messages
        return [self.decompress_data(message.encode('utf-8')) for message in stored_messages]

    def clear_chat_history(self, chat_id: str) -> None:
        # Clear the chat history for the given chat ID in Redis
        self.redis_client.delete(chat_id)
        logger.info(f"Chat history for {chat_id} cleared in Redis")
