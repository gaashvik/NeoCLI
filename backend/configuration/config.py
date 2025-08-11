import os
from dotenv import load_dotenv
import sys
from langchain.chat_models import init_chat_model


load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
CUSTOM_PROMPT = "[🧠 AICopilot >>] "

META_DIR=sys.argv[1]
HUGGING_FACE_API=os.getenv("HUGGING_FACE_API")



os.environ["GOOGLE_API_KEY"]=GEMINI_API_KEY
LLM_REACT=init_chat_model("google_genai:gemini-2.5-flash")



