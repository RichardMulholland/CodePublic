from pathlib import Path

######################################################################
def find_repo_root(start_path):
    path = Path(start_path).resolve()
    for parent in [path] + list(path.parents):
        if (parent / ".git").is_dir():
            return str(parent)
    return str(path)  # fallback
######################################################################
BASE_URL = "https://github.com"

ASSETS_ENDPOINT = "/user-attachments/assets"

USER_SESSION = "your_copied_token_here"

DEFAULT_FILE_PATH = find_repo_root(__file__)
