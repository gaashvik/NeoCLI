from github import GithubIntegration, Github
import os
from ..configuration import config
APP_ID = config.APP_ID
with open(config.PRIVATE_KEY,"r") as f:
    PRIVATE_KEY = f.read()

integration = GithubIntegration(APP_ID, PRIVATE_KEY)

def get_github_client(installation_id):
    token_info = integration.get_access_token(installation_id)
    return Github(token_info.token)