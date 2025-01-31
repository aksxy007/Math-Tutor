from transformers import TextStreamer
# from unsloth import FastLanguageModel
async def generate_response(tokenized_inputs,tokenizer,model):
    # FastLanguageModel.for_inferenece(model)
    # tokenized_inputs = tokenized_inputs.to(model.device)
    # text_streamer = TextStreamer(tokenizer, skip_prompt=False, skip_special_tokens=True)
    print("Generating response")
    response = model.generate(tokenized_inputs, max_new_tokens = 150)
    print("Response generated")
    return response
    