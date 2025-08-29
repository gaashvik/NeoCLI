from langgraph.graph import MessagesState
from .llm import llm_class as response_model
from .tools import error_tool_list
from langchain_core.messages import SystemMessage, HumanMessage
from .document_grader import grade_documents
from .generate_answer import generate_answer
from .rewrite import rewrite_question

def generate_query_or_respond(state: MessagesState):
    """Call the model to generate a response based on the current state. Given
    the question, it will decide to retrieve using the retriever tool, or simply respond to the user.
    """
    response = (
        response_model
        .bind_tools(error_tool_list).invoke([ SystemMessage(content='''You are an expert error-handling assistant for developers. Your goal is to resolve errors efficiently using project-specific context. Follow these guidelines:

1. Assess Error Context:
   - Determine if the error can be resolved with general knowledge (syntax, Python, bash, common libraries, etc.).
   - If there is **any ambiguity or project-specific aspect**, immediately generate a **context retrieval query** using all relevant information from the error message: filenames, function names, variable names, error type, and stack trace.
   - Include the **file path** if present in the error, and any keywords that would help the retrieval system find matching code snippets or configurations in the project embeddings.

2. Use Project Context Effectively:
   - Retrieve project-specific files, code, or configurations whenever the error depends on code structure, dependencies, or project setup.
   - Clearly explain why context was required before providing a solution.
   - Always assume that the user **will not provide additional input** until you have finished retrieving and analyzing context.

3. Provide Clear and Actionable Advice:
   - Suggest exact code changes, configuration edits, or shell commands.
   - Include explanations when necessary.
   - Highlight possible runtime pitfalls or common errors.

4. Error Handling Best Practices:
   - For ambiguous errors, prioritize retrieval of relevant context over asking the user vague clarifying questions.
   - Use the context to verify assumptions, not just to copy files.

5. Response Format:
   - State whether project context was required.
   - Provide the recommended fix.
   - Optionally, include a short rationale.

'''),state["messages"][0]])
    )
    return {"messages": [response]}


from langgraph.graph import StateGraph, START, END
from langgraph.prebuilt import ToolNode
from langgraph.prebuilt import tools_condition
from langgraph.checkpoint.memory import InMemorySaver

checkpointer=InMemorySaver()
workflow = StateGraph(MessagesState)

workflow.add_node("generate_query_or_respond", generate_query_or_respond)
workflow.add_node("retrieve_context", ToolNode([error_tool_list[0]]))
workflow.add_node("rewrite_question",rewrite_question)
workflow.add_node("generate_answer",generate_answer)

# Graph edges
workflow.add_edge(START, "generate_query_or_respond")
workflow

# Conditional branching
workflow.add_conditional_edges(
    "generate_query_or_respond",
    tools_condition,
    {
        "tools": "retrieve_context",
        END: END,
    },
)

workflow.add_conditional_edges(
    "retrieve_context",
    # Assess agent decision
    grade_documents,
)
workflow.add_edge("generate_answer", END)
workflow.add_edge("rewrite_question", "generate_query_or_respond")

graph = workflow.compile(checkpointer=checkpointer)


