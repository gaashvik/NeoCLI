import os
from dotenv import load_dotenv
import sys
load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
CUSTOM_PROMPT = "[🧠 AICopilot >>] "

META_DIR=sys.argv[1]
HUGGING_FACE_API=os.getenv("HUGGING_FACE_API")



