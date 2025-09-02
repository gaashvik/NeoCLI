from .configuration import config
from prompt_toolkit import PromptSession
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
from prompt_toolkit.completion import WordCompleter
from langchain_core.messages import HumanMessage
from .UI import terminal
from .core.agent import workflow
from .core.tools import shell
import os 
import sys
import traceback
import pexpect
from .core.error_handling_agent import graph
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
    auto=1

    while True:
        try:
            user_input = session.prompt("💬 > ")
            if user_input.strip() == ":exit":
                print("👋 Exiting...")
                break

            if (user_input.strip() == "::manual"):
                print("Entered Manual Exec Mode.")
                auto=0
                continue
            if (user_input.strip() == "::auto"):
                print("Entered Manual Exec Mode.")
                try:
                    while True:
                        shell.shell.read_nonblocking(size=1024, timeout=0.1)
                except pexpect.exceptions.TIMEOUT:
                    pass
                auto=1
                continue

            
            if (auto == 1):
                messages = [HumanMessage(content=user_input)]
                thread_config = {"configurable": {"thread_id": "some_id"}}
                input_state = {"messages": messages}
                terminal.stream_workflow(input_state,thread_config,workflow)
            else:
                error_c,text=shell.run_and_stream(user_input)
                if (error_c!=0):
                    print("here is the output:",text)
                    answer=input(f"[NEO] you must have encountered an error (code:{error_c}) would you like to get some suggestions on how to resolve it? (y/n) >>")
                    if (answer == 'y'):
                        messages = [HumanMessage(content=text)]
                        thread_config = {"configurable": {"thread_id": "some_id_2"}}
                        input_state = {"messages": messages}
                        terminal.stream_workflow(input_state,thread_config,graph)

        except KeyboardInterrupt:
            print("\n⏹️ Interrupted.")
        except EOFError:
            print("\n👋 Exiting (EOF).")
            break
        except Exception as e:
            print("Workflow failed",e)
            traceback.print_exc()
            sys.exit(1)
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
