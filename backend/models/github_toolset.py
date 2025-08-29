import os
import time
import base64
from typing import Dict, List, Optional, Union
from dataclasses import dataclass
import subprocess
from github import Github, GithubException, RateLimitExceededException
from github.Repository import Repository
from github.GitRef import GitRef
from github.GitCommit import GitCommit
from github.GitTree import GitTree
from github.GitBlob import GitBlob
from github.PullRequest import PullRequest
from github.Workflow import Workflow
from github.WorkflowRun import WorkflowRun
from ..configuration import config
from ..utilities import github_client




# ------------------------------
# Config / constants
# ------------------------------

DEFAULT_BASE_BRANCH = "main"
POLL_INTERVAL_SEC = 5
WORKFLOW_TIMEOUT_SEC = 25 * 60 



class GitHubToolset:
    """
    High-level, agent-friendly wrapper around PyGithub.
    """

    def __init__(self, token: Optional[str] = None):
        
        self.gh = github_client.get_github_client(config.INSTALL_ID)
        self.repo=self.gh.get_repo(config.GIT_STATE["repo_full_name"])
        self.helper_llm=config.LLM_HELPER

    def generate_PR_title_and_desc(self,source_branch:str,target_branch:str):
        """Generate a PR title and description from a git diff which it find based on source and target_branch mentioned using LLM."""
        diff=subprocess.run(
            ["git", "diff", f"{target_branch}...{source_branch}"],
            capture_output=True,
            text=True
        ).stdout
        response=self.helper_llm.invoke(f'''Create a concise PR title (1 line) and in depth description
        based on this git diff:{diff}''')
        return response
    
        


    def create_PR(self,source_branch:str,target_branch:str,title:str=None,description:str=None):
        pr=self.repo.create_pull(head=source_branch,base=target_branch,title=title,body=description)
        return f"PR created successfully: {pr.html_url}"


        

if __name__ == "__main__":
    g=GitHubToolset()
    print(g.ensure_branch("dev"))
