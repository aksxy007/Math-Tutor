from transformers import AutoTokenizer,AutoModelForCausalLM
import torch
# from unsloth import FastLanguageModel

model_path = r"bot\llama_3.2_3b_Instruct_MedAId_1"


def load_model():
    print("Loading the model")
    model = AutoModelForCausalLM.from_pretrained(
        model_path,
        torch_dtype=torch.float32,
        load_in_8bit=False,
        device_map='auto'
    )
    model.to("cuda")  
    tokenizer = AutoTokenizer.from_pretrained(
        model_path,max_length=2048
    )
    
    # model, tokenizer = FastLanguageModel.from_pretrained(
    #         model_name = model_path,
    #         max_seq_length = 2048,
    #         dtype = torch.float16,
    #         load_in_4bit = True
    # )
    
    
    return model,tokenizer


