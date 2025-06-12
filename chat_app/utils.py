# backend/chat_app/utils.py
from django.core.cache import cache
from .types import ModelType
from .ai_providers.text_models import (
    query_deepseek,
    query_mistral,
    query_deephermes,
)
from .ai_providers.code_models import (
    query_qwen3_coder,
    query_llama3_coder,
    query_deepseek_prover
)

def query_provider(prompt: str, model_type: ModelType, model_name: str, language: str = "en"):
    cache_key = f"{model_type}_{model_name}_{hash(prompt)}"
    if cached := cache.get(cache_key):
        return cached  

    MODEL_MAPPING = {
        'deepseek_qwen3': query_deepseek,
        'mistral_devstral': query_mistral,
        'deephermes': query_deephermes,
        
        'llama3_coder': query_llama3_coder,
        'deepseek_prover': query_deepseek_prover,
        'qwen3_coder': query_qwen3_coder,
        }
    
    if model_name not in MODEL_MAPPING:
        return f"[Error] Unknown model: {model_name}", None
    
    text, tokens = MODEL_MAPPING[model_name](prompt, language)
    cache.set(cache_key, (text, tokens), timeout=3600)
    return MODEL_MAPPING[model_name](prompt)
