import os
from dotenv import load_dotenv

load_dotenv()

RABBITMQ_HOST = os.getenv("RABBITMQ_HOST")
QUEUE_NAME = os.getenv("QUEUE_NAME")
API_URL = os.getenv("API_URL")
MODEL_NAME = os.getenv("MODEL_NAME")
OLLAMA_MODEL_NAME = os.getenv("OLLAMA_MODEL_NAME")
LLM_MODEL_HOST = os.getenv("LLM_MODEL_HOST")
USE_MOCK_LLM = os.getenv("USE_MOCK_LLM", "False") == "True"
