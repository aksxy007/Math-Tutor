def get_tokenized_inputs(tokenizer,messages,device='cuda'):
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token
    print(device)
    inputs = tokenizer.apply_chat_template(
        messages,
        tokenize = True,
        padding=True,
        truncate=True,
        add_generation_prompt = True, # Must add for generation
        return_tensors = "pt",
    ).to(device)
    
    # input_dict = {k: v.to('cpu') for k, v in inputs.items()}
    
    return inputs