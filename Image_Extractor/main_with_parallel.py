
from support_files.utils import (
    clear_terminal,
    extract_filtered_urls,
    get_final_url_and_filename,
    download_image,
    replace_url_with_image_path  # Now imported from utils
)
from support_files.config import (
    USER_SESSION,
    BASE_URL,
    ASSETS_ENDPOINT,
    DEFAULT_FILE_PATH
)
import tkinter as tk
from tkinter import filedialog
from pathlib import Path
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.progress import Progress
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

def download_image_task(url, filename, images_dir, session):
    # Check if any file with this base name exists in the images directory (any extension)
    existing_files = list(images_dir.glob(f"{filename}.*"))
    if existing_files:
        return url, None, 'exists'
    # Now get the redirected URL and download
    final_url, redirected_filename, response = get_final_url_and_filename(url, session)
    ext = Path(redirected_filename).suffix if redirected_filename else ""
    image_path = images_dir / f"{filename}{ext}"
    image_rel_path = f"Images/{filename}{ext}"
    if final_url and response and download_image(response, image_path):
        if image_path.exists():
            return url, image_rel_path, 'downloaded'
    return url, None, 'failed'

# Progress bar for downloads
with Progress() as progress:
    task = progress.add_task(f"[cyan]Downloading images... ({total_urls} total)", total=total_urls)
    results = []
    # Prepare download tasks
    tasks = [(url, filename, images_dir, USER_SESSION) for url, filename in filtered_urls]
    with ThreadPoolExecutor(max_workers=4) as executor:
        futures = [executor.submit(download_image_task, *task) for task in tasks]
        for future in as_completed(futures):
            url, image_rel_path, status = future.result()
            results.append((url, image_rel_path, status))
            progress.update(task, advance=1)

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
