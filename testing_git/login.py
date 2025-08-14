import os
import pexpect
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs

# Assuming InMemoryHistory is defined elsewhere or not strictly needed for this demo
class InMemoryHistory:
    def __init__(self):
        self.history = []
    def append_string(self, command):
        self.history.append(command)

class ai_shell:
    def __init__(self):
        self.shell = pexpect.spawn("/bin/bash", ["-i", "-l"], encoding="utf-8", timeout=10)
        self.shell.expect(r"\\$ ", timeout=30)
        print("the shell session has started in the current working directory")
        self.mem_history = InMemoryHistory()

    def run(self, command):
        self.shell.sendline(command)
        self.shell.expect(r"\\$ ", timeout=30)
        self.mem_history.append_string(command.strip())
        lines = self.shell.before.strip().splitlines()

        if lines and lines[0].strip() == command.strip():
            lines = lines[1:]

        clean_output = [line for line in lines if line.strip()]
        clean_output=clean_output[1:]
        return \n.join(clean_output).strip()

    def close(self):
        self.shell.terminate()

class LoginHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == /:
            self.send_response(200)
            self.send_header(Content-type, text/html)
            self.end_headers()
            with open(os.path.join(testing_git, index.html), rb) as f:
                self.wfile.write(f.read())
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b404 Not Found)

    def do_POST(self):
        if self.path == /login:
            content_length = int(self.headers[Content-Length])
            post_data = self.rfile.read(content_length).decode(utf-8)
            params = parse_qs(post_data)

            username = params.get(username, [])[0]
            password = params.get(password, [])[0]

            if username == root and password == admin:
                self.send_response(200)
                self.send_header(Content-type, text/html)
                self.end_headers()
                self.wfile.write(b"<h1>Login Successful!</h1>")
                self.wfile.write(f"<p>Welcome, {username}!</p>".encode(utf-8))

                # Start the ai_shell session and echo username
                try:
                    shell_session = ai_shell()
                    echo_output = shell_session.run(f"echo User {username} logged in successfully!")
                    self.wfile.write(f"<pre>Shell Output:\n{echo_output}</pre>".encode(utf-8))
                    shell_session.close()
                except Exception as e:
                    self.wfile.write(f"<p>Error starting shell session: {e}</p>".encode(utf-8))

            else:
                self.send_response(401)
                self.send_header(Content-type, text/html)
                self.end_headers()
                self.wfile.write(b"<h1>Login Failed!</h1><p>Invalid username or password.</p>")
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b404 Not Found)

def run_server(server_class=HTTPServer, handler_class=LoginHandler, port=8000):
    server_address = (, port)
    httpd = server_class(server_address, handler_class)
    print(fStarting httpd server on port {port}...)
    httpd.serve_forever()

if __name__ == __main__:
    # Ensure the directory exists for index.html
    os.makedirs(testing_git, exist_ok=True)
    run_server()

