from .configuration import config
from prompt_toolkit import PromptSession
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
from prompt_toolkit.completion import WordCompleter
from langchain_core.messages import HumanMessage
from .UI import terminal
from .core.agent import workflow
from .core.tools import shell
import os

# Persistent file path
history_file = os.path.expanduser(f"{config.META_DIR}/.neocli/.neocli_history")

try:
    loaded_history_lines = 0
    with open(history_file, 'r') as f:
        for line in f:
            clean_line = line.strip()
            if clean_line:
                shell.mem_history.append_string(clean_line)
                loaded_history_lines+=1
except FileNotFoundError:
    pass

completer = WordCompleter(
    ['help', 'exit', 'restart', 'status'],
    ignore_case=True
)
session = PromptSession(
    history=shell.mem_history,
    auto_suggest=AutoSuggestFromHistory(),
    completer=completer,
    enable_history_search=True
)
def repl():
    print("\n AI Shell Copilot (Approval Mode)")
    print("Type ':exit' to quit\n")

    while True:
        try:
            user_input = session.prompt("💬 > ")

            if user_input.strip() == ":exit":
                print("👋 Exiting...")
                break

            

            messages = [HumanMessage(content=user_input)]
            thread_config = {"configurable": {"thread_id": "some_id"}}
            input_state = {"messages": messages}
            terminal.stream_workflow(input_state,thread_config,workflow)
            

        except KeyboardInterrupt:
            print("\n⏹️ Interrupted.")
        except EOFError:
            print("\n👋 Exiting (EOF).")
            break
        except Exception as e:
            print(f"❌ Error: {e}")

    # Save history
    try:
        all_entries = shell.mem_history.get_strings()
        new_entries = all_entries[loaded_history_lines:]
        with open(history_file, 'a') as f:
            for entry in new_entries:
                f.write(entry + '\n')
    except Exception as e:
        print(f"⚠️ Failed to write history: {e}")


if __name__ == "__main__":
    repl()
