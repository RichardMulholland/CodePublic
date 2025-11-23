
"""
File: utils.py

Description:
    Contains utility functions for the Markdown Image Downloader, including:
    - Clearing the terminal
    - Extracting and filtering image URLs
    - Handling HTTP requests and downloads
    - Replacing URLs in Markdown content with local image paths

Author: Richard Mulholland
Date: 2025-11-23

Dependencies:
    - os
    - requests
    - re
    - urllib.parse
    - pathlib

Usage:
    Import these functions into main.py or other scripts as needed.


"""
import os
import requests
import re
from urllib.parse import urlparse
from pathlib import Path
#####################################
def clear_terminal():
    # For Windows
    if os.name == 'nt':
        os.system('cls')
    # For macOS/Linux
    else:
        os.system('clear')

#####################################

def extract_filtered_urls_OLD(content, base_url, assets_endpoint):
    #urls = re.findall(r'https?://[^\s\)]+', content)
    urls = re.findall(r'https?://[^\s\)"]+', content)  # Exclude closing parenthesis and double quote
    filtered = [u for u in urls if base_url in u and assets_endpoint in u]
    # Remove any trailing double quotes (just in case)
    filtered = [u.rstrip('"') for u in filtered]

    return list(set(filtered))

#####################################
def get_final_url_and_filename(url,user_session):

    headers = {
        "User-Agent": "Mozilla/5.0",
        "Cookie": f"user_session={user_session}; logged_in=yes"
    }
    response = requests.get(url, allow_redirects=True, stream=True, headers=headers)
    #response = requests.get(url, allow_redirects=True,headers=headers)

    if response.status_code == 200:
        final_url = response.url
        filename = Path(urlparse(final_url).path).name
        return final_url, filename, response
    return None, None, None

#####################################
def download_image(response, image_path):
    try:
        with open(image_path, "wb") as img_file:
            for chunk in response.iter_content(1024):
                img_file.write(chunk)
        # with open(image_path, "wb") as img_file:
        #     img_file.write(response.content)
        return True
    except Exception as e:
        print(f"Error saving {image_path}: {e}")
        return False

#################################


def extract_filtered_urls(content, base_url, assets_endpoint):
    # Find all URLs, excluding closing parenthesis and double quote
    urls = re.findall(r'https?://[^\s\)"]+', content)
    filtered = [u.rstrip('"') for u in urls if base_url in u and assets_endpoint in u]
    result = []
    for url in set(filtered):
        parsed = urlparse(url)
        # Get the last part of the path, split by '/' and take the last segment
        filename = parsed.path.rstrip('/').split('/')[-1]
        result.append((url, filename))
    return result

######################################

def replace_url_with_image_path(content, url, image_rel_path):

    """
    Replace all occurrences of the given URL in the content with the relative image path.
    Works for Markdown, HTML, or plain text.
    """
    return content.replace(url, image_rel_path)

