from langchain.tools import Tool
from ..helpers import agent_helpers
from ..models import session

session = session.ai_shell()

shell_run_tool = Tool.from_function(
    name="shell",
    description="Run bash shell commands. Input should be a valid shell command. and a single invocation can run a single command",
    func=session.run,
)

explain_tool = Tool.from_function(
    name="explain",
    description="Explain what a shell command does.",
    func=agent_helpers.explain_bash_command,
)

print("tools created")

list = [shell_run_tool, explain_tool]
