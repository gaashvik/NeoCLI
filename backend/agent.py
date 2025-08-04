from langchain.agents import initialize_agent
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents.agent import AgentExecutor
from langchain.agents.agent_types import AgentType
from tools import tools
from configuration import config

llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0.2,
    google_api_key=config.GEMINI_API_KEY,
    max_retries=2
)

agent_executor = initialize_agent(
    tools=tools.list,
    llm=llm,
    agent=AgentType.CHAT_ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True
)
from langchain.schema import AgentAction, AgentFinish
def run_agent_goal(user_input, dry_run=False, plan=None, intermediate_steps=None):
    intermediate_steps = intermediate_steps or []
    print("debug 1")

    if dry_run:
        # ✅ FIXED: Pass inputs as a dict with key 'input'
        return agent_executor.agent.plan(
            intermediate_steps=intermediate_steps,
            input={"input": user_input}
        )

    elif plan:
        print("debug 2")
        tool_dict = {t.name: t for t in agent_executor.tools}
        tool = tool_dict.get(plan.tool)

        if not tool:
            return f"❌ Unknown tool: {plan.tool}"

        return tool.run(plan.tool_input)

    else:
        print("debug 2")
        return agent_executor.run(user_input)
    
    
