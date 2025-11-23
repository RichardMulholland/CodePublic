

"""
main.py

A utility script for converting PDF files into a series of PNG images and generating a Markdown file referencing those images.

Author: Richard Mulholland
Date: 2025-11-23

Features:
- Prompts the user to select a PDF file via a graphical file dialog.
- Asks the user for a base filename for output files.
- Allows the user to choose a target directory for saving results.
- Converts each page of the selected PDF into a PNG image using pdf2image.
- Saves all images in a structured subfolder under the chosen directory.
- Generates a Markdown (.md) file with image links to the saved PNGs.
- Provides informative logging throughout the process.

Intended Usage:
Run this script in a terminal (preferably Bash) to interactively select a PDF, specify output options, and automatically generate slide images and a Markdown file for easy documentation or presentation sharing.

Dependencies:
- tkinter
- pdf2image
- pathlib
- logging
- os

Version: 
    001: Initial version
"""


import os
from pathlib import Path
import tkinter as tk
from tkinter import filedialog, simpledialog, ttk
from pdf2image import convert_from_path
import logging

#####################################
if os.name == 'nt':
    os.system('cls')
else:
    os.system('clear')

#####################################
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

GREEN = "\033[92m"
YELLOW = '\033[93m'
RED = "\033[91m"
RESET = "\033[0m"

#####################################


logger.info(f"{GREEN}PDF to PNG process started.{RESET}")
# Step 1: Select PDF File
file_path = filedialog.askopenfilename(
    initialdir = str(Path.home() / "Downloads"),  # Default to Downloads
    title="Select a PDF file",
    filetypes=[("PDF files", "*.pdf")]
)


if file_path:
    filename_without_ext = Path(file_path).stem
    logger.info(f"Selected file: {GREEN}{file_path}{RESET}")

else:
    logger.error(f"{RED}No filename provided. Exiting.{RESET}")
    exit()
#######################################
# Step 2: Ask for Base Filename
stem_name = simpledialog.askstring("Filename", "Enter a base filename:", initialvalue=filename_without_ext)

if not stem_name:
    logger.error(f"{RED}No filename provided. Exiting.{RESET}")
    exit()

logger.info(f"Selected stem name: {GREEN}{stem_name}{RESET}")
########################################
# Step 3: Choose folder to save file to, defaulting to script's folder
script_folder = os.path.dirname(os.path.abspath(__file__))

save_folder = filedialog.askdirectory(
    title="Select folder to save output file",
    initialdir=script_folder
)

if save_folder:
    logger.info(f"Target folder: {GREEN}{save_folder}{RESET}")
else:
    logger.error(f"{RED}No taget folder selected. Exiting.{RESET}")
    exit()

###########################################
# Step 4: Convert PDF to PNG images

# Optional: Set Poppler path here if needed
#poppler_path = r"C:\Path\To\poppler\bin"
#pdf_images = convert_from_path(file_path, dpi=300, poppler_path=poppler_path)

logger.info(f"Looking for slides in PDF.")
pdf_images = convert_from_path(file_path, dpi=300)
logger.info(f"Found {len(pdf_images)} slides in PDF.")

#########################################
# Step 5: Prepare output folder

markdown_path = Path(save_folder) / f"{stem_name}_slides.md"
Slides_dir = Path(save_folder) / "Slides" / stem_name
Slides_dir.mkdir(parents=True,exist_ok=True)
#########################################
# Step 6: Save each image
image_paths = []
total = len(pdf_images)

for i, img in enumerate(pdf_images, start=1):
    number = f"{i:03}"
    filename = f"{stem_name}_SLIDES_{number}.png"
    image_path = os.path.join(Slides_dir, filename)
    img.save(image_path, "PNG")
    image_paths.append(filename)
    logger.info(f"Saved slide {i:03}/{total:03}: {GREEN}{filename}{RESET}")
    
#########################################
# Step 7: Create Markdown file
markdown_lines = [
    f"![{name[-7:-4]}](Slides/{stem_name}/{name})"
    for name in image_paths
]

logger.info(f"Writing markdown lines to: {GREEN}{markdown_path}{RESET}")

with open(markdown_path, "w") as md_file:
    md_file.write("\n".join(markdown_lines))
    
logger.info(f"Finsihed writing markdown lines to: {GREEN}{markdown_path}{RESET}")

#########################################
logger.info(f"{GREEN}PDF to PNG process complete.{RESET}")