
from unsloth.chat_templates import get_chat_template

def get_model_chat_template(tokenizer):
    
    tokenizer = get_chat_template(
        tokenizer,
        chat_template = "llama-3.1",
    )
    
    return tokenizer