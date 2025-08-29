import subprocess
import os
from pathlib import Path



def run_git_cmd(args, cwd=None):
    """Run a git command in the repo root and return stripped output."""
    return subprocess.check_output(args, text=True, cwd=cwd).strip()

def find_git_root(start_path: Path) -> Path | None:
    """Walk up the directory tree until a .git folder is found."""
    current = start_path.resolve()
    while current != current.parent:  # Stop at filesystem root
        if (current / ".git").exists():
            return current
        current = current.parent
    return None

def init_repo_info():
    repo_info={}
    repo_root = find_git_root(Path.cwd())
    if repo_root is None:
        repo_info["is_git_repo"] = False
        return repo_info

    repo_info["is_git_repo"] = True
    repo_info["repo_root"] = str(repo_root)


    remote_url = run_git_cmd(["git", "config", "--get", "remote.origin.url"], cwd=repo_root)
    repo_info["remote_url"] = remote_url

    clean_url = remote_url[:-4] if remote_url.endswith(".git") else remote_url
    if clean_url.startswith("git@"):
        path = clean_url.split(":", 1)[1]
    elif clean_url.startswith("https://") or clean_url.startswith("http://"):
        path = clean_url.split("github.com/")[1]
    else:
        path = None
    repo_info["repo_full_name"] = path


    repo_info["current_branch"] = run_git_cmd(["git", "rev-parse", "--abbrev-ref", "HEAD"], cwd=repo_root)


    # try:
    #     head_ref = run_git_cmd(["git", "symbolic-ref", "refs/remotes/origin/HEAD"], cwd=repo_root)
    #     repo_info["default_branch"] = head_ref.split("/")[-1]
    # except subprocess.CalledProcessError as e:
    #     print(e)
    #     repo_info["default_branch"] = None

    return repo_info

if __name__ == "__main__":
    state=init_repo_info()
    print(state)