from motor.motor_asyncio import AsyncIOMotorClient
import os
from fastapi import FastAPI
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file

# MongoDB URI from environment variables
MONGO_URI = os.getenv("MONGODB_URL", "mongodb://localhost:27017")
MONGO_DB_NAME = os.getenv("MONGO_DB_NAME", "medaid")
client = None


class MongoDBConnection:
    def __init__(self):
        self.client = self.connectClient()
        self.db = self.connectDB()
    def connectClient(self):
        global client
        if client is None:
            client = AsyncIOMotorClient(MONGO_URI)
        print("Connected to mongoDB")
        return client
    
    def connectDB(self):
        db = self.client[MONGO_DB_NAME]  # Get default database
        return db 
    
    def get_database(self):
        return self.db
    
    async def get_server_info(self):
        info = await self.client.server_info()
        return info
    
    async def get_collections(self):
        collections = await self.db.list_collection_names()
        print(f"Collections: {collections}")
        return collections
        
    # async def delete_collection(self,collection_name: str):
    #     collection = self.db[collection_name]
    #     await collection.drop()
            
    #     print(f"Collection '{collection_name}' has been deleted.")
        
    