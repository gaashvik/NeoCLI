from langchain.agents import initialize_agent
from langchain_google_genai import ChatGoogleGenerativeAI

from langchain.agents.agent_types import AgentType
from tools import tools
from configuration import config

llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0.2,
    google_api_key=config.GEMINI_API_KEY,
        max_retries=2,
)

agent = initialize_agent(
    tools=tools.tools,
    llm=llm,
     agent=AgentType.CHAT_ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True
)

def run_agent_goal(goal: str) -> str:
    return agent.invoke({
        "input": goal,
        "chat_history": []
    })
