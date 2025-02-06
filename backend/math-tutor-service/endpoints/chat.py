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
from datetime import datetime

import torch
router = APIRouter()

mongoClient = MongoDBConnection()
# model,tokenizer  = load_model()
model  = load_model()
torch.cuda.empty_cache()


@router.post("/chat/mathtut/create")
async def create_chat(chat:Chat):
    try:
        db = mongoClient.get_database()
        chat.createdAt = datetime.now()
        chat.messages=[]
        print("create chat",chat)
        result = await create_new_chat(db,chat=chat)
        print("result insert chat",result)
        return JSONResponse(content={"success":True,"message":str("Chat created successfully"),"chatId":result['chatId']},status_code=status.HTTP_200_OK)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail = str(e))
    
    
    
    
@router.post("/chat/mathtut/send")
async def medaid_response(query:Query):
    try:
        messages=[]
        db = mongoClient.get_database()
        print(f"FastAPI connected to DB: {db.name}")
        await mongoClient.get_collections()
        system_prompt = get_system_prompt()
        try:
            result = await get_contextual_chat_history(db,query.chatId,query.query)
            messages =  [system_prompt]+ result
            
        except Exception as e:
            print("Error in getting chat history: ",e)
        
        messages.append({"role":"user","content":query.query})
        print(messages)
        response = await generate_response(messages,model)
        assistant_response = response['content']
        messages.append({"role":"assistant","content":assistant_response})
        try:
            user_chat = Message(chatId=query.chatId,role="user",content=query.query,createdAt=datetime.now())
            assistant_chat = Message(chatId=query.chatId,role="assistant",content=assistant_response,createdAt=datetime.now())
            message_list = [user_chat,assistant_chat]
            results = await insert_messages(db,messages=message_list)
            
            if results:
                try:
                    chat_updation = await update_current_chat_messages(db,chatId=query.chatId,messageIds=results.inserted_ids)
                    if chat_updation:
                        print("chat inserted successfully")
                except Exception as e:
                    print("Error in append message ids in chat",e)
                    
        except Exception as e:
            print("Error in inserting chat",e)
        print(assistant_response)
        return JSONResponse(content={"success":True,"message":str(assistant_response),"chatId":query.chatId},status_code=status.HTTP_200_OK)

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail = str(e))
    
