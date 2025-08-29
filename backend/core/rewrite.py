from langgraph.graph import MessagesState
from langchain_core.messages import HumanMessage
from .llm import llm_rewriter as response_model
REWRITE_PROMPT = (
    "Look at the input and try to reason about the underlying semantic intent / meaning.\n"
    "Here is the initial error info:"
    "\n ------- \n"
    "{question}"
    "\n ------- \n"
    "Formulate an improved question:"
)


def rewrite_question(state: MessagesState):
    """Rewrite the original user question."""
    messages = state["messages"]
    print("rewrite---------------------")
    print(messages)
    question = messages[0].content
    prompt = REWRITE_PROMPT.format(question=question)
    response = response_model.invoke([{"role": "user", "content": prompt}])
    return {
        "messages": [HumanMessage(content=response.content)]
    }