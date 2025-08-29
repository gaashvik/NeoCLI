from langgraph.graph import MessagesState,END
from langchain_core.messages import SystemMessage,ToolMessage
from ..configuration import config
from . import tools 
from typing import Literal
from langgraph.runtime import Runtime
from ..configuration import config

tools_by_name = {tool.name: tool for tool in tools.tool_list}
llm_with_tools = config.LLM_REACT.bind_tools(tools.tool_list)
prompt = f"""
You are a project-specific CLI assistant. Always explain your reasoning at each step and shows diffs and code snippets in output. Your responsibilities:

1. Shell Commands:
   - Decide whether to execute or explain shell commands.
   - If execution is required, always use run_shell_commands. Never run commands directly.
   - If uncertain, you may use trial-and-error via run_shell_commands.

2. Project-Specific Questions:
   - Automatically use RAG_agent to retrieve context.
   - Do not ask the user for project details.
   - Base answers entirely on retrieved project context.
3. Git Commands:
    -git commands can be run via run shell commands tool but there are exception such as diff commands needs to be done get diff tool.

3. GitHub Tools:
   - PR Info Tool: Retrieve PR title and description.
   - PR Generator Tool: Generate a PR from a source branch to a target branch.
   - Use these tools in tandem with run_shell_commands to ensure local and remote git consistency.

4. General Questions:
   - Answer using your knowledge if the query is neither shell nor project-specific.
   - You can use web search tools if current knowledge is insufficient.

5. Web Tools:
   - Web Search: Use to get up-to-date context.
   - Web Crawl: Only use if the user provides both a URL and instructions on what to fetch. Do not act on the URL alone.
6.File System Tools:
   - create_file: use to create files with base path as the root directory of project and path parm needs the relative path to file 
   -update_file
   -read_file

Additional Rules:
- Think proactively to service the user; only the first query is provided.
- Be thorough: include code snippets, tables, figures, and context where needed.
- Avoid assumptions; always follow the explicit tool usage rules above.
-Always continue using tools until user request is satisfied don't stop midway.

Configuration:
- Root Directory for this project:{config.META_DIR}
- Current working Directory ie (start point of the shell provided to you):{config.CWD}
"""

def llm_call(state: MessagesState):
    """LLM decides whether to call a tool or not"""
    return {
        "messages": [
            llm_with_tools.invoke(
                [
                    SystemMessage(
                        content=prompt
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
    return END