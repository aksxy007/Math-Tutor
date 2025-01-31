from motor.motor_asyncio import AsyncIOMotorClient
import os
from fastapi import FastAPI
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file

# MongoDB URI from environment variables
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
MONGO_DB_NAME = os.getenv("MONGO_DB_NAME", "medaid")
client = None


class MongoDBConnection:
    def __init__(self):
        self.db=self.connectDB()

    def connectDB(self):
        global client
        if client is None:
            client = AsyncIOMotorClient(MONGO_URI)
        db = client[MONGO_DB_NAME]  # Get default database
        print("connected to mongo db")
        return db
    
    def get_database(self):
        return self.db
    
    async def get_collections(self):
        collections = await self.db.list_collection_names()
        print(f"Collections: {collections}")
        return collections
        
