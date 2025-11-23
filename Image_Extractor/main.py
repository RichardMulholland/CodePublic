
"""
File: main.py

Description:
    Entry point for the Markdown Image Downloader.
    Allows the user to select a Markdown file, extracts image URLs, downloads images,
    updates the Markdown file to use local image paths, and provides a summary of the process.

Author: Richard Mulholland
Date: 2025-11-23

Dependencies:
    - tkinter
    - rich
    - requests
    - utils.py
    - config.py

Usage:
    Run this script to select a Markdown file and automatically download and relink images.
    I found it best to run from a bash terminal and not from PowerShell.

Version:
    003 - main_parallel_multi_progress
"""

from support_files.utils import (
    clear_terminal,
    extract_filtered_urls,
    get_final_url_and_filename,
    replace_url_with_image_path,
)
from support_files.config import (
    USER_SESSION,
    BASE_URL,
    ASSETS_ENDPOINT,
    DEFAULT_FILE_PATH,
)
import tkinter as tk
from tkinter import filedialog
from pathlib import Path
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.progress import (
    Progress,
    BarColumn,
    TextColumn,
    TimeElapsedColumn,
    DownloadColumn,
    TaskProgressColumn,
)
from concurrent.futures import ThreadPoolExecutor, as_completed
import os

# Clear terminal at the start
clear_terminal()
console = Console()

# Create a hidden root window for file dialog
root = tk.Tk()
root.withdraw()

# Open file picker for .md files
file_path = filedialog.askopenfilename(
    initialdir=DEFAULT_FILE_PATH,
    title="Select a Markdown file",
    filetypes=[("Markdown files", "*.md")]
)
if not file_path:
    console.print("[red]No file selected. Exiting.[/red]")
    exit()

# Read the file content
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

# Extract and filter URLs (returns list of (url, filename) tuples)
filtered_urls = extract_filtered_urls(content, BASE_URL, ASSETS_ENDPOINT)
total_urls = len(filtered_urls)

# Prepare images directory
md_dir = Path(file_path).parent
images_dir = md_dir / "Images"
images_dir.mkdir(exist_ok=True)

# Tracking variables
downloaded = 0
already_exists = 0
failed_images = []

def download_image_task(url, filename, images_dir, session, progress, task_id):
    # Check if any file with this base name exists in the images directory (any extension)
    existing_files = list(images_dir.glob(f"{filename}.*"))
    if existing_files:
        progress.update(task_id, completed=1)
        return url, None, 'exists'
    # Get the redirected URL and download
    final_url, redirected_filename, response = get_final_url_and_filename(url, session)
    ext = Path(redirected_filename).suffix if redirected_filename else ""
    image_path = images_dir / f"{filename}{ext}"
    image_rel_path = f"Images/{filename}{ext}"
    if final_url and response:
        total = int(response.headers.get('content-length', 0))
        progress.update(task_id, total=total)
        try:
            with open(image_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
                        progress.update(task_id, advance=len(chunk))
            if image_path.exists():
                progress.update(task_id, completed=total)
                return url, image_rel_path, 'downloaded'
        except Exception as e:
            pass
    progress.update(task_id, completed=1)
    return url, None, 'failed'

# Progress bars for each image, elapsed time only
with Progress(
    TextColumn("[progress.description]{task.description}"),
    BarColumn(),
    TaskProgressColumn(),
    DownloadColumn(),
    TimeElapsedColumn(),  # Only elapsed time
    console=console,
    transient=False,
) as progress:
    # Prepare download tasks and progress bars
    task_ids = [
        progress.add_task(f"Downloading {filename}", total=1)
        for url, filename in filtered_urls
    ]
    results = []
    # Submit download tasks in parallel
    with ThreadPoolExecutor(max_workers=4) as executor:
        futures = [
            executor.submit(
                download_image_task, url, filename, images_dir, USER_SESSION, progress, task_id
            )
            for (url, filename), task_id in zip(filtered_urls, task_ids)
        ]
        for future in as_completed(futures):
            url, image_rel_path, status = future.result()
            results.append((url, image_rel_path, status))

# After all downloads, update the Markdown content
for url, image_rel_path, status in results:
    if status == 'downloaded' and image_rel_path:
        content = replace_url_with_image_path(content, url, image_rel_path)
        downloaded += 1
    elif status == 'exists':
        already_exists += 1
    else:
        failed_images.append(url)

# Write the updated content back to the Markdown file
with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)

# Logging output
summary = Table(show_header=False, box=None)
summary.add_row("Markdown file:", Path(file_path).name)
summary.add_row("URLs found:", str(total_urls))
summary.add_row("Images downloaded:", str(downloaded))
summary.add_row("Already existed:", str(already_exists))
summary.add_row("Failed downloads:", str(len(failed_images)))
console.print(Panel(summary, title="Markdown Image Downloader", expand=False))
if failed_images:
    failed_panel = Panel(
        "\n".join(str(img) for img in failed_images),
        title="Images Not Downloaded",
        expand=False,
        style="red"
    )
    console.print(failed_panel)
