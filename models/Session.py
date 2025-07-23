import pexpect

class ai_shell:
    def __init__(self):
        self.shell=pexpect.spawn("/bin/bash", encoding="utf-8")
        self.shell.expect(r"\$",timeout=5)
        print(self.shell)
        print("the shell session has started in the current working directory")

    def run(self,command):
        self.shell.sendline(command)
        self.shell.expect(r"\$",timeout=30)
        return(self.shell.before.strip())

    def close(self):
        self.shell.terminate()