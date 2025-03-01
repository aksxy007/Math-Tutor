
from huggingface_hub import hf_hub_download
from services.logger import logger

def download_or_cache_model():
    
    repo_id = "Atul06/llama_3b_math_puzzle_tutor_gguf_4bit"
    model_file ="unsloth.Q4_K_M.gguf"
    model_path = hf_hub_download(repo_id, filename=model_file,local_dir="bot\model_cache")
    logger.info(f"Model cached to: {model_path}")
    
    return model_path