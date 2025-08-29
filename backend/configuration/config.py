import os
from dotenv import load_dotenv
import sys
from langchain.chat_models import init_chat_model
from ..utilities.intialise_git_state import init_repo_info

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
CUSTOM_PROMPT = "[🧠 AICopilot >>] "

META_DIR=sys.argv[1]
CWD=sys.argv[2]
HUGGING_FACE_API=os.getenv("HUGGING_FACE_API")

os.environ["GOOGLE_API_KEY"]=GEMINI_API_KEY
LLM_REACT=init_chat_model("google_genai:gemini-2.5-flash")

LLM_HELPER=init_chat_model("google_genai:gemini-2.5-flash")

GIT_STATE=init_repo_info()

APP_ID=os.getenv("GIT_APP_ID")
INSTALL_ID=os.getenv("GIT_INSTALL_ID")
PRIVATE_KEY=os.getenv("GIT_PRIVATE_KEY")
print(GIT_STATE)



