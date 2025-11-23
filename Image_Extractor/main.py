#import os 
from support_files.utils import (
    clear_terminal,
    extract_filtered_urls,
    get_final_url_and_filename,
    download_image,
    replace_url_with_image_path
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
#console.print(f"[bold green]Total filtered URLs: {total_urls}[/bold green]")

# Prepare images directory
md_dir = Path(file_path).parent
images_dir = md_dir / "Images"
images_dir.mkdir(exist_ok=True)

# Tracking variables
downloaded = 0
already_exists = 0
failed_images = []

# Progress bar for downloads
with Progress() as progress:
    task = progress.add_task(f"[cyan]Downloading images... ({total_urls} total)", total=total_urls)

    for url, filename in filtered_urls:
        # Check if any file with this base name exists in the images directory (any extension)
        existing_files = list(images_dir.glob(f"{filename}.*"))
        if existing_files:
            already_exists += 1
            progress.update(task, advance=1)
            continue  # Skip download if file exists

        # Now get the redirected URL and download
        final_url, redirected_filename, response = get_final_url_and_filename(url, USER_SESSION)
        if not final_url or not response:
            failed_images.append(filename)
            progress.update(task, advance=1)
            continue

        # Use the original filename, but try to get the extension from the redirected URL
        ext = Path(redirected_filename).suffix if redirected_filename else ""
        image_path = images_dir / f"{filename}{ext}"

        if download_image(response, image_path):
            downloaded += 1
        
            # Check if image exists
            if image_path.exists():
                # Compute relative path from Markdown file to image
                #image_rel_path = os.path.relpath(image_path, md_dir)
                image_rel_path = f"Images/{filename}{ext}"
                # Replace the URL in the Markdown content
                content = replace_url_with_image_path(content, url, image_rel_path)
                
        else:
            failed_images.append(f"{filename}{ext}")
        progress.update(task, advance=1)

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
