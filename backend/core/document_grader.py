from pydantic import BaseModel, Field
from langgraph.graph import MessagesState
from typing import Literal
from .llm import llm_grader as grader_model
from langgraph.graph import END
from langchain_core.messages import SystemMessage, HumanMessage,AIMessage


GRADE_PROMPT = (
    "You are a strict grader assessing whether a retrieved document is relevant to a CLI Copilot user's error .\n\n"
    "---- Retrieved Document ----\n"
    "{context}\n"
    "----------------------------\n\n"
    "---- User Question ----\n"
    "{question}\n"
    "-----------------------\n\n"
    "Instructions:\n"
    "- Grade the document as 'yes' ONLY if it contains information, keywords, or meaning clearly related to answering the question.\n"
    "- Grade as 'no' ONLY if the content is clearly unrelated or unhelpful for the user's question.\n"
    "- If any part of the document helps answer the user's question, even partially, grade 'yes'.\n\n"
    "Output ONLY one word: 'yes' or 'no'."
)


class GradeDocuments(BaseModel):
    """Grade documents using a binary score for relevance check."""

    binary_score: str = Field(
        description="Relevance score: 'yes' if relevant, or 'no' if not relevant"
    )




def grade_documents(
    state: MessagesState,
) -> Literal["generate_answer", "rewrite_question"]:
    """Determine whether the retrieved code are relevant to the question."""
    print(state)
    question = state["messages"][-3].content
    context = state["messages"][-1].content
    print("------------context")
    print(question)
    print(context)
    prompt = GRADE_PROMPT.format(question=question, context=context)
    response = (
        grader_model
        .with_structured_output(GradeDocuments).invoke(
            [{"role": "user", "content": prompt}]
        )
    )
    print("--------------------------grade")
    print(response)
    score = response.binary_score

    if score == "yes":
        return "generate_answer"
    else:
        return "rewrite_question"
    