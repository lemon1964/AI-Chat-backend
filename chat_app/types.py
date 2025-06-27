# backend/chat_app/types.py
from enum import Enum

class ModelType(str, Enum):
    TEXT = "text"
    CODE = "code"
    # IMAGE = "image"
