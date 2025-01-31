from fastapi import HTTPException,APIRouter,status
from fastapi.responses import JSONResponse
from models.Query import Query
from models.Chat import Chat
from bot.utils.inference import generate_response
from bot.utils.get_tokenized_input import get_tokenized_inputs
from bot.utils.get_system_prompt import get_system_prompt
from bot.utils.load_model import load_model
from db.mongo_connection import  MongoDBConnection
from db.get_chat_history import get_chat_history
from db.insert_chat import insert_chat
from datetime import datetime
# from bot.utils.get_model_chat_template import get_model_chat_template
import torch
router = APIRouter()

mongoClient = MongoDBConnection()
model,tokenizer  = load_model()
device = model.device
torch.cuda.empty_cache()
@router.post("/chat/mathtut")
async def medaid_response(query:Query):
    try:
        messages=[]
        print("Model device",device)
        db = mongoClient.get_database()
        collections  = await mongoClient.get_collections()
        system_prompt = get_system_prompt()
        try:
            result = await get_chat_history(db,query.chatId)
            messages = result['chat_history']
            if len(messages)==0:
                messages.append(system_prompt)
        except Exception as e:
            print("Error in getting chat history: ",e)
        print(messages)
        # tokenizer = get_model_chat_template(tokenizer)
        messages.append({"role":"user","content":query.query})
        tokenized_inputs = get_tokenized_inputs(tokenizer,messages,device)
        # print("tokenized inputs",tokenized_inputs["input_ids"].device)
        outputs = await generate_response(tokenized_inputs,tokenizer,model)
        response = tokenizer.batch_decode(outputs,skip_special_tokens=True)
        if "assistant" in response[0]:
            assistant_response = response[0].split("assistant")[-1].strip()
        else:
            assistant_response = response[0].strip()
        messages.append({"role":"assistant","content":assistant_response})
        try:
            user_chat = Chat(chatId=query.chatId,userId=query.userId,role="user",content=query.query,createdAt=datetime.now())
            assitant_chat = Chat(chatId=query.chatId,userId=query.userId,role="assistant",content=assistant_response,createdAt=datetime.now())
            chat_list = [user_chat,assitant_chat]
            results = await insert_chat(db,chats=chat_list)
            if results:
                print("chat inserted successfully")
        except Exception as e:
            print("Error in inserting chat",e)
        print(assistant_response)
        return JSONResponse(content={"message":str(assistant_response)},status_code=status.HTTP_200_OK)

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail = str(e))
        