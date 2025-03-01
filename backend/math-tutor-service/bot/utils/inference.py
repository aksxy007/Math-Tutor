from services.logger import logger

async def generate_response(messages,model):
    logger.info("Generating response")
    
    response =  model.create_chat_completion(
    	messages,
        max_tokens = 2048
    )
    logger.info("Response generated")
    return response['choices'][0]['message']
    