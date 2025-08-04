from .agent import run_agent_goal
from .configuration import config
from prompt_toolkit import PromptSession
from langchain.schema import AgentAction, AgentFinish
from langchain.agents.agent import AgentExecutor
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
from prompt_toolkit.completion import WordCompleter
from .tools import tools
import os

# Persistent file path
history_file = os.path.expanduser(f"{config.META_DIR}/.neocli/.neocli_history")

try:
    loaded_history_lines = 0
    with open(history_file, 'r') as f:
        for line in f:
            clean_line = line.strip()
            if clean_line:
                tools.session.mem_history.append_string(clean_line)
                loaded_history_lines+=1
except FileNotFoundError:
    pass

completer = WordCompleter(
    ['help', 'exit', 'restart', 'status'],
    ignore_case=True
)
session = PromptSession(
    history=tools.session.mem_history,
    auto_suggest=AutoSuggestFromHistory(),
    completer=completer,
    enable_history_search=True
)
def repl():
    print("\n🤖 AI Shell Copilot (Approval Mode)")
    print("Type ':exit' to quit\n")

    while True:
        try:
            user_input = session.prompt("💬 > ")

            if user_input.strip() == ":exit":
                print("👋 Exiting...")
                break

            intermediate_steps = []

            while True:
                print("⚙️ Agent thinking...")
                plan = run_agent_goal(
                    user_input,
                    dry_run=True,
                    intermediate_steps=intermediate_steps
                )

                if isinstance(plan, AgentFinish):
                    print("✅ Final answer:", plan.return_values['output'])
                    break

                print(f"\n🤖 Agent proposes tool: {plan.tool}")
                print(f"🧾 Input: {plan.tool_input}")

                approval = input("✅ Proceed? (y/n): ").strip().lower()
                if approval != 'y':
                    print("⏹️ Tool execution cancelled.")
                    break  # or continue, if you want agent to try another plan

                result = run_agent_goal(
                    user_input,
                    plan=plan,
                    intermediate_steps=intermediate_steps
                )

                print(f"🔍 Tool result: {result}")

                # Store this tool step in the agent’s state
                intermediate_steps.append((plan, result))

        except KeyboardInterrupt:
            print("\n⏹️ Interrupted.")
        except EOFError:
            print("\n👋 Exiting (EOF).")
            break
        except Exception as e:
            print(f"❌ Error: {e}")

    # Save history
    try:
        all_entries = tools.session.mem_history.get_strings()
        new_entries = all_entries[loaded_history_lines:]
        with open(history_file, 'a') as f:
            for entry in new_entries:
                f.write(entry + '\n')
    except Exception as e:
        print(f"⚠️ Failed to write history: {e}")


if __name__ == "__main__":
    repl()
