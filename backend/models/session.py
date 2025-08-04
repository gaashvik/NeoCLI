import pexpect
import re
from prompt_toolkit.history import InMemoryHistory


class ai_shell:
    def __init__(self):
        self.shell = pexpect.spawn("/bin/bash", ["-i", "-l"], encoding="utf-8",timeout=10)
        self.shell.expect(r"\$ ", timeout=30)
        print("the shell session has started in the current working directory")
        self.mem_history = InMemoryHistory()

    def run(self,command):
        self.shell.sendline(command)
        self.shell.expect(r"\$ ", timeout=30)
        self.mem_history.append_string(command.strip())
        lines = self.shell.before.strip().splitlines()

        if lines and lines[0].strip() == command.strip():
            lines = lines[1:]

        clean_output = [line for line in lines if line.strip()]
        clean_output=clean_output[1:]
        return '\n'.join(clean_output).strip()



    def close(self):
        self.shell.terminate()