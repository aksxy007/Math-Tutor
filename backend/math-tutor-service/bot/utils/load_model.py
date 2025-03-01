from llama_cpp import Llama
from bot.utils.download_or_cache_model import download_or_cache_model
import torch
from services.logger import logger

def load_model():
    logger.info("Loading the model")
    if torch.cuda.is_available():
        use_gpu=-1
    else:
        use_gpu=0
    model_path = download_or_cache_model()
    model = Llama(
        model_path=model_path,
        chat_format="llama-3",
        n_ctx=2048,      # Max tokens for in + out
        n_threads=4,     # CPU cores used
        n_gpu_layers=use_gpu, # dydnamically choose to load layers on gpu if available
        verbose=False  # no logs
    )    
    return model


