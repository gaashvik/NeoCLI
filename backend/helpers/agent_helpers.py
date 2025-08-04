
from ..configuration import config

from langchain_google_genai import ChatGoogleGenerativeAI

llm = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash",
    temperature=0,
    max_tokens=None,
    timeout=40,
    max_retries=2,
    google_api_key=config.GEMINI_API_KEY
)

def explain_bash_command(command: str) -> str:
    prompt = f"Explain this bash command step by step:\n{command}"
    return llm.predict(prompt)
