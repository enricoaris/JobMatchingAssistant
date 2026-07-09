import os
from .interface import LLMProvider
from .ollama_provider import OllamaProvider
from .mock_provider import MockProvider

class LLMFactory:
    @staticmethod
    def create_provider() -> LLMProvider:
        use_mock = os.getenv("USE_MOCK_LLM", "true").lower() == "true"

        if use_mock:
            return MockProvider(
                delay=float(os.getenv("MOCK_DELAY", "1.0"))
            )
        
        host = os.getenv("LLM_MODEL_HOST", "http://ollama:11434")
        model = os.getenv("OLLAMA_MODEL_NAME", "phi3")

        provider = OllamaProvider(host=host, model_name=model)

        if not provider.is_available():
            return MockProvider(delay=0.5)
        
        print(f"Using Ollama provider with model: {model}")
        return provider
        