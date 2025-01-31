from transformers import AutoTokenizer,AutoModelForCausalLM
import torch
# from unsloth import FastLanguageModel

model_path = "bot\llama_3b_math_puzzle_tutor"

import torch

torch.cuda.empty_cache()
torch.cuda.ipc_collect()

if torch.cuda.is_available():
    print("CUDA is available, but you are using CPU.")
else:
    print("CUDA is not available, and you are correctly using the CPU.")
from transformers import BitsAndBytesConfig

bnb_config = BitsAndBytesConfig(
    load_in_4bit=True,
    # load_in_8bit=False,
    bnb_4bit_quant_type="nf4",
    bnb_4bit_compute_dtype=torch.float16
)

device = torch.device('cpu')  
def load_model():
    print("Loading the model")
    model = AutoModelForCausalLM.from_pretrained(
        model_path,
        local_files_only=True, 
        torch_dtype=torch.float32,
        quantization_config=bnb_config,
        device_map=device,
        # low_cpu_mem_usage=True,
    )
    model.to(device)
    print("model parameter device",next(model.parameters()).device)
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


