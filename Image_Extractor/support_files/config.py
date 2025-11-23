
"""
File: config.py

Description:
    Configuration settings and helper functions for the Markdown Image Downloader.
    Defines constants such as BASE_URL, ASSETS_ENDPOINT, USER_SESSION, and
    provides a function to find the repository root directory.

Author: Richard Mulholland
Date: 2025-11-23

Dependencies:
    - pathlib

Usage:
    Import configuration variables and functions into other scripts as needed.


"""
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
