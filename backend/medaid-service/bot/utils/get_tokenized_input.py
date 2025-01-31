def get_tokenized_inputs(tokenizer,messages):
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token
    inputs = tokenizer.apply_chat_template(
        messages,
        tokenize = True,
        padding=True,
        truncate=True,
        add_generation_prompt = True, # Must add for generation
        return_tensors = "pt",
    ).to('cuda')
    
    # input_dict = {k: v.to('cuda') for k, v in inputs.items()}
    
    return inputs