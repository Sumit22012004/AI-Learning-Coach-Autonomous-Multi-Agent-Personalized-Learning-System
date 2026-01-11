from langchain_openai import ChatOpenAI
from src.core.config import settings

def get_llm_client(model: str = "mistralai/mistral-7b-instruct"):
    """
    Returns a LangChain ChatOpenAI instance configured for OpenRouter.
    """
    if not settings.OPENROUTER_API_KEY:
        # Fallback or error if key is missing
        print("Warning: OPENROUTER_API_KEY is not set.")
        
    return ChatOpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=settings.OPENROUTER_API_KEY,
        model=model,
        temperature=0.7
    )
