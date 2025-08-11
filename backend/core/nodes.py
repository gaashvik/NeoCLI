from langgraph.graph import MessagesState,END
from langchain_core.messages import SystemMessage,ToolMessage
from ..configuration import config
from . import tools 
from typing import Literal



tools_by_name = {tool.name: tool for tool in tools.tool_list}
llm_with_tools = config.LLM_REACT.bind_tools(tools.tool_list)


def llm_call(state: MessagesState):
    """LLM decides whether to call a tool or not"""
    return {
        "messages": [
            llm_with_tools.invoke(
                [
                    SystemMessage(
                        content="You are a helpful project-specific CLI assistant. Your responsibilities: 1) Shell Commands: If the user’s request involves running shell commands, decide whether to execute or explain. If execution is required, use the run_shell_commands tool to run the command. 2) Project-Specific Questions: If the user asks anything that relates to a specific project’s implementation, configuration, or behavior, you must automatically use the RAG_agent tool to retrieve the necessary project context. Do not ask the user for project details — the RAG_agent will provide them. Always base your answer on the retrieved project context. 3) General Questions: If the question is not about shell commands or project context, answer normally using your own knowledge. Important Rules: For project-specific queries: Immediately call RAG_agent with relevant keywords from the user’s question. For shell execution: Always use run_shell_commands to run commands, never execute them directly. Never ask for project clarification if RAG_agent can be used to determine context.user will not provide any input except the first query after that it is your responsibility to think about how to best service the user make use of all tools available to you to complete the task.if there is ambiguity then use hit and trail via the run_shell_commands tool to figure out what can be done.Answer as in depth as possible and use figure, context content ie code snippets (important), tables etc if necessary"
                    )
                ]
                + state["messages"]
            )
        ]
    }


def tool_node(state: MessagesState):
    """Performs the tool call"""

    result = []
    for tool_call in state["messages"][-1].tool_calls:
        tool = tools_by_name[tool_call["name"]]
        observation = tool.invoke(tool_call["args"])
        result.append(ToolMessage(content=observation, tool_call_id=tool_call["id"]))
    return {"messages": result}



def should_continue(state: MessagesState) -> Literal["environment", END]:
    """Decide if we should continue the loop or stop based upon whether the LLM made a tool call"""

    messages = state["messages"]
    last_message = messages[-1]
    # If the LLM makes a tool call, then perform an action
    if last_message.tool_calls:
        return "Action"
    # Otherwise, we stop (reply to the user)
    return END