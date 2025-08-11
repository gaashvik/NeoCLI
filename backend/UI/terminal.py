from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage,ToolMessage
import sys
from langgraph.types import  Command


console = Console()



def normalize_message_content(content):
    """Ensure message content is always a single string for Rich printing."""
    if isinstance(content, list):
        # Join all elements into a single string
        return "\n".join(
            str(item.get("text", item)) if isinstance(item, dict) else str(item)
            for item in content
        )
    return str(content)


def rich_pretty_print_message(msg):
    is_tool=False
    if isinstance(msg, HumanMessage):
        sender = "[bold green]Human"
    elif isinstance(msg, AIMessage):
        sender = "[bold cyan]NEO"
    elif isinstance(msg, SystemMessage):
        sender = "[bold yellow]System"
    elif isinstance(msg,ToolMessage):
        sender = "[bold magenta]TOOL"
        is_tool=True
    else:
        sender="[bold red]APPROVAL"

    # Render message content as markdown if possible
    content = normalize_message_content(getattr(msg, "content", str(msg)))
    additional_args = getattr(msg, "additional_kwargs", {})
    function_details = additional_args.get("function_call", None)
    user_question=""
    if (function_details):
        user_question=(f"""
### 🛠️ Shell Command Execution
\n\n
You are about to run the following command via `{function_details.get('name')}`:

```bash
{function_details.get('arguments')}
Do you want to proceed? (y/n)
""")

    
    
    try:
        if (is_tool):
            md = content
        else:
            md=Markdown(content+user_question)
        console.print(Panel(md, title=sender, expand=True, border_style="blue"))
    except Exception:
        console.print(Panel(content, title=sender, expand=True, border_style="red"))


def stream_workflow(input_state,thread_config,workflow):
    try:
        events = workflow.stream(input_state, config=thread_config, stream_mode="values")
        for event in events:
                    for key, value in event.items():
                                rich_pretty_print_message(value[-1])
    except Exception as e:
        logger.exception("Workflow failed")
        sys.exit(1)


    # Get latest state snapshot
    snapshot = workflow.get_state(thread_config)

    # Handle tool call interruptions
    while snapshot.next:
        user_input = input("Approve tool call? (y/n): ").strip().lower()

        if user_input == "y":
            ev=workflow.stream(Command(resume=[{"type": "accept"}]), thread_config,stream="values")
            for event in ev:
                for key, value in event.items():
                    if key == "__interrupt__":
                        continue
                    else:
                        # value should be a dict with a 'messages' list
                        messages = value.get("messages", [])
                        for msg in messages:
                            rich_pretty_print_message(msg)
        else:
            tool_call_id = snapshot.values["messages"][-1].tool_calls[0]["id"]
            workflow.invoke(
                {
                    "messages": [
                        ToolMessage(
                            tool_call_id=tool_call_id,
                            content=f"Tool call denied by user. Reason: '{user_input}'"
                        )
                    ]
                },
                thread_config
            )

        # Refresh state after invoke
        snapshot = workflow.get_state(thread_config)
        # message=snapshot.values.get("messages")[-1]
        # message.pretty_print()