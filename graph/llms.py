from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv

load_dotenv()

def get_llm(model: str = "gemini-2.5-pro", temperature: float = 0.0):
    if model == "gemini-2.5-pro":
        return ChatGoogleGenerativeAI(model=model, temperature=temperature, thinking_budget=24576)
    
    if model == "gemini-2.5-flash":
        return ChatGoogleGenerativeAI(model=model, temperature=temperature, thinking_budget=24576)

    return None
