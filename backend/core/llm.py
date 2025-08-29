import os
from langchain.chat_models import init_chat_model
from langchain_google_genai import ChatGoogleGenerativeAI
from ..configuration import config
os.environ["GOOGLE_API_KEY"] = config.GEMINI_API_KEY

llm_class = init_chat_model("google_genai:gemini-2.5-flash")

llm_grader=init_chat_model("google_genai:gemini-2.5-flash")

llm_rewriter=init_chat_model("google_genai:gemini-2.5-flash")

llm_answere=init_chat_model("google_genai:gemini-2.5-flash")

llm_react=init_chat_model("google_genai:gemini-2.5-flash")

llm_supervisor=init_chat_model("google_genai:gemini-2.5-flash-lite")