# 🖼️ Image Extractor

A Python utility that automatically extracts and downloads images from GitHub markdown files.

## 🚀 Overview

Image Extractor is a command-line tool designed to scan markdown files, identify image URLs hosted on GitHub's user attachments, and download them locally into an `Images` folder within the markdown file's directory.

## 📚 Table of Contents

- #-overview
- [✨ Features](#-features)
- [🛠️ Requirements](#️-requirements)
- [📦 Installation](#-Installation)
- [⚡ Usage](#-usage)
- [🗂️ Project Structure](#️-project-structure)
- [⚙️ Configuration](#️-configuration)
  - [🔑 Getting Your GitHub User Session Token](#-getting-your-github-user-session-token)
- [🧠 How It Works](#-how-it-works)
- [📊 Example Output](#-Example-Output)
- [📝 Notes](#-notes)

## ✨ Features

- **Interactive File Selection**: Opens a file dialog to select markdown files from your system
- **Smart URL Extraction:** Finds and filters GitHub asset URLs from markdown content.
- **Automatic Directory Management**: Creates an `Images` folder automatically if it doesn't exist
- **Duplicate Detection**: Skips images that already exist locally (by filename)
- **Progress Tracking**: Displays a real-time progress bar during downloads
- **Error Handling**: Gracefully handles failed downloads and provides a summary report
- **Rich Console Output**: Beautiful, formatted output with tables and panels using the `rich` library

## 🛠️ Requirements

- Python 3.6+
- Dependencies:
  - `requests` - For HTTP requests and file downloads
  - `rich` - For formatted console output
  - `tkinter` - For file dialog (usually included with Python)

## 📦 Installation

1. Clone or download this project
2. Install required dependencies:
   ```bash
   pip install requests rich
   ```

## ⚡ Usage

Run the main script:

```bash
python main.py
```

The program will:
1. Open a file dialog to select a markdown file
2. Parse the markdown content for GitHub image URLs
3. Create an `Images` directory in the same folder as the markdown file
4. Download all images to the `Images` directory
5. Display a summary showing:
   - Number of URLs found
   - Number of images successfully downloaded
   - Number of images that already existed
   - Number of failed downloads (if any)

## 🗂️ Project Structure

```
Image_Extractor/
├── main.py              # Main entry point
├── config/
│   └── config.py        # Configuration settings (URLs, session token, etc.)
└── utils/
    └── utils.py         # Utility functions for URL extraction and downloading
```

## ⚙️ Configuration

The `config/config.py` file contains:

- `BASE_URL`: GitHub domain (https://github.com)
- `ASSETS_ENDPOINT`: GitHub user attachments endpoint (/user-attachments/assets)
- `DEFAULT_FILE_PATH`: Default directory for file picker
- `USER_SESSION`: Session token for authenticated requests (required for private images)

### 🔑 Getting Your GitHub User Session Token

To download images (especially private ones), you need to provide your GitHub `user_session` token:

1. **Log in to GitHub** in your web browser
2. **Open Developer Tools**:
   - Press `F12` (or `Ctrl+Shift+I` on Windows/Linux, `Cmd+Option+I` on Mac)
   - Navigate to the **Application** or **Storage** tab
3. **Find Cookies**:
   - In the left sidebar, expand **Cookies**
   - Click on `https://github.com`
4. **Locate the Token**:
   - Look for the cookie named `user_session`
   - Copy the entire value
5. **Update Configuration**:
   - Open `config/config.py`
   - Replace the `USER_SESSION` value with your token:
     ```python
     USER_SESSION = "your_copied_token_here"
     ```

#### 🚨🚨🚨 Security Note 🚨🚨🚨
Keep your session token private. Do not commit it to public repositories or share it with others.

## 🧠 How It Works

1. **URL Extraction**: Regex pattern finds all HTTP/HTTPS URLs in the markdown file
2. **Filtering**: Identifies only GitHub asset URLs matching the base URL and assets endpoint
3. **Filename Extraction**: Parses the filename from the URL path
4. **Duplicate Check**: Searches for any file with the same base name in the Images directory
5. **Download**: Follows redirects and downloads the image with proper authentication headers
6. **Error Tracking**: Records any failed downloads for user reference

## 📊 Example Output

```
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ Markdown Image Downloader                 ┃
├────────────────────────────────────────-──┤
│ Markdown file:     document.md            │
│ URLs found:        15                     │
│ Images downloaded: 12                     │
│ Already existed:   2                      │
│ Failed downloads:  1                      │
└──────────────────────────────────────-────┘
```

## 📝 Notes

- Images are saved to `Images/` subdirectory of the markdown file's location
- The tool uses HTTP sessions and user agent headers to handle authenticated downloads
- File extensions are automatically detected from the final redirected URL
- Existing images are preserved and not overwritten
