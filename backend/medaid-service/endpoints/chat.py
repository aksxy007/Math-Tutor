from fastapi import HTTPException,APIRouter,status
from fastapi.responses import JSONResponse
from models.Query import Query
from bot.utils.inference import generate_response
from bot.utils.get_tokenized_input import get_tokenized_inputs
from bot.utils.get_system_prompt import get_system_prompt
from bot.utils.load_model import load_model
# from bot.utils.get_model_chat_template import get_model_chat_template

router = APIRouter()


messages = []

model,tokenizer  = load_model()
@router.post("/chat/medaid")
async def medaid_response(query:Query):
    try:
        system_prompt = get_system_prompt()
        if len(messages)==0:
            messages.append(system_prompt)
            
        # tokenizer = get_model_chat_template(tokenizer)
        messages.append({"role":"user","content":query.query})
        tokenized_inputs = get_tokenized_inputs(tokenizer,messages)
        outputs = await generate_response(tokenized_inputs,tokenizer,model)
        response = tokenizer.batch_decode(outputs,skip_special_tokens=True)
        if "assistant" in response[0]:
            assistant_response = response[0].split("assistant")[-1].strip()
        else:
            assistant_response = response[0].strip()
        messages.append({"role":"assistant","content":assistant_response})
        print(assistant_response)
        return JSONResponse(content={"message":str(assistant_response)},status_code=status.HTTP_200_OK)

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail = str(e))
        