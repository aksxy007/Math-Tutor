from fastapi import HTTPException,APIRouter,status
from fastapi.responses import JSONResponse
from models.Query import Query
from models.Chat import Chat
from models.Message import Message
from bot.utils.inference import generate_response
from bot.utils.get_system_prompt import get_system_prompt
from bot.utils.load_model import load_model
from db.mongo_connection import  MongoDBConnection
from db.get_relevant_chat_history import get_contextual_chat_history
from db.insert_messages import insert_messages
from db.create_new_chat import create_new_chat
from db.update_current_chat_messages import update_current_chat_messages
from services.logger import logger
from services.ChatCache import ChatCache
from datetime import datetime

import torch
router = APIRouter()

mongoClient = MongoDBConnection()
chatCache = ChatCache()
model  = load_model()
torch.cuda.empty_cache()


@router.post("/chat/mathtut/create")
async def create_chat(chat:Chat):
    try:
        db = mongoClient.get_database()
        chat.createdAt = datetime.now()
        chat.messages=[]
        logger.info("create chat",chat)
        result = await create_new_chat(db,chat=chat)
        logger.info("result insert chat",result)
        return JSONResponse(content={"success":True,"message":str("Chat created successfully"),"chatId":result['chatId']},status_code=status.HTTP_200_OK)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail = str(e))
    
    
    
    
@router.post("/chat/mathtut/send")
async def medaid_response(query:Query):
    try:
        messages=[]
        db = mongoClient.get_database()
        logger.info(f"FastAPI connected to DB: {db.name}")
        await mongoClient.get_collections()
        system_prompt = get_system_prompt()
        try:
            result = await get_contextual_chat_history(db,chatCache ,query.chatId,query.query)
            messages =  [system_prompt]+ result
            logger.info(f"messages: {messages}")
        except Exception as e:
            messages.append(system_prompt)
            logger.info(f"Error in getting chat history: {e}")
        
        messages.append({"role":"user","content":query.query})
        logger.info(messages)
        response = await generate_response(messages,model)
        assistant_response = response['content']
        messages.append({"role":"assistant","content":assistant_response})
        try:
            user_chat = Message(chatId=query.chatId,role="user",content=query.query,createdAt=datetime.now())
            assistant_chat = Message(chatId=query.chatId,role="assistant",content=assistant_response,createdAt=datetime.now())
            message_list = [user_chat,assistant_chat]
            results = await insert_messages(db,messages=message_list)
            user_chat_dict = {"role":"user","content":query.query}
            assistant_chat_dict = {"role":"assistant","content":assistant_response}
            if results:
                try:
                    chat_updation = await update_current_chat_messages(db,chatId=query.chatId,messageIds=results.inserted_ids)
                    if chat_updation:
                        logger.info("chat inserted successfully")
                    try:
                        logger.info(f"Caching messages from chatid: {query.chatId}")
                        chatCache.set_chat_history(chat_id=query.chatId,messages=[user_chat_dict,assistant_chat_dict])
                    except Exception as e:
                        logger.info(f"Failed to cache mesasges in chatId: {query.chatId} , error: {e}")
                except Exception as e:
                    logger.info(f"Error in append message ids in chat: {e}")
                    
        except Exception as e:
            logger.info("Error in inserting chat",e)
        logger.info(assistant_response)
        return JSONResponse(content={"success":True,"message":str(assistant_response),"chatId":query.chatId},status_code=status.HTTP_200_OK)

    except Exception as e:
        logger.info(f"Error in chat: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail = str(e))
    
