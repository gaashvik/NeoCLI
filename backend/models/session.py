import pexpect
import re
from prompt_toolkit.history import InMemoryHistory
import sys
import os
class ai_shell:
    def __init__(self):
        user_env = os.environ.copy()
        # Remove virtualenv variables
        user_env.pop("VIRTUAL_ENV", None)
        user_env.pop("PYTHONHOME", None)
        
        # Remove venv from PATH
        venv_path = os.environ.get("VIRTUAL_ENV")
        if venv_path:
            user_env["PATH"] = ":".join(
                p for p in user_env["PATH"].split(":") if not p.startswith(venv_path)
            )

        self.shell = pexpect.spawn("/bin/bash", ["-i", "-l"], env=user_env, encoding="utf-8", timeout=10)
        self.shell.setecho(False)
        self.shell.expect(r"\$ ", timeout=120)
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

    def run_and_stream(self, command):
        """Run interactively and stream output, capturing exit code for agent."""
        self.shell.logfile = sys.stdout  # stream live
        # Run command and append 'echo $?'
        self.shell.sendline(f"{command}; echo __EXIT_CODE__$?")
        self.shell.expect(r"__EXIT_CODE__\d+", timeout=None)
        exit_code_line = self.shell.match.group(0)
        exit_code = int(exit_code_line.replace("__EXIT_CODE__", ""))
        self.shell.logfile = None
        try:
            while True:
                self.shell.read_nonblocking(size=1024, timeout=0.1)
        except pexpect.exceptions.TIMEOUT:
            pass
        if exit_code!=0:
            lines = self.shell.before.strip().splitlines()

            if lines and lines[0].strip() == command.strip():
                lines = lines[1:]

            clean_output = [line for line in lines if line.strip()]
            clean_output=clean_output[1:]
            return exit_code,'\n'.join(clean_output).strip()
        
        return exit_code,None



    def close(self):
        self.shell.terminate()