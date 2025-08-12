from langgraph.graph import StateGraph,MessagesState,START,END
from . import nodes
from langgraph.checkpoint.memory import InMemorySaver

checkpointer=InMemorySaver()


agent_builder = StateGraph(MessagesState)


agent_builder.add_node("llm_call", nodes.llm_call)
agent_builder.add_node("environment", nodes.tool_node)

agent_builder.add_edge(START, "llm_call")
agent_builder.add_conditional_edges(
    "llm_call",
    nodes.should_continue,
    {
        "Action": "environment",
        END: END,
    },
)
agent_builder.add_edge("environment", "llm_call")



workflow = agent_builder.compile(checkpointer=checkpointer)