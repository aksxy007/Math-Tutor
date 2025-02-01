
async def generate_response(messages,model):
    print("Generating response")
    
    response =  model.create_chat_completion(
    	messages,
        max_tokens = 2048
    )
    print("Response generated")
    return response['choices'][0]['message']
    