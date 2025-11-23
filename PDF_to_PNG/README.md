# 📄 PDF to PNG Converter

A utility script for converting PDF files into individual PNG images and generating a Markdown file with image references.

## 🎯 Features

- 🖱️ **Interactive File Selection** - Select PDF files via graphical file dialog
- 📝 **Custom Naming** - Specify a base filename for output files
- 📁 **Flexible Output** - Choose any target directory for saving results
- 🖼️ **PDF Conversion** - Convert each PDF page into high-quality PNG images (300 DPI)
- 📚 **Organized Structure** - Saves images in a structured `Slides/{stem_name}/` subfolder
- 📋 **Markdown Generation** - Automatically creates a `.md` file with image links for easy documentation

## 🚀 Installation

### Prerequisites

- Python 3.7+
- `tkinter` (usually included with Python)
- `pdf2image`

### Install Dependencies

```bash
pip install pdf2image
```

**Note:** `pdf2image` requires Poppler. Installation varies by OS:

**Windows:**
```bash
pip install poppler-utils
```

**macOS:**
```bash
brew install poppler
```

**Linux:**
```bash
sudo apt-get install poppler-utils
```

## 💻 Usage

1. Run the script:
   ```bash
   python main.py
   ```

2. A dialog box will appear asking you to **select a PDF file**
   - Defaults to your Downloads folder

3. Enter a **base filename** for the output
   - This will be used to name the PNG files and output Markdown

4. Choose a **target directory** to save the results
   - Defaults to the script's folder

5. The script will:
   - ✅ Convert all PDF pages to PNG images
   - ✅ Save them in `Slides/{stem_name}/` subdirectory
   - ✅ Generate a Markdown file with image references

## 📤 Output Structure

```
target_folder/
├── {stem_name}_slides.md
└── Slides/
    └── {stem_name}/
        ├── {stem_name}_SLIDES_001.png
        ├── {stem_name}_SLIDES_002.png
        └── ...
```

## 📊 Example

After running the script on a PDF called `Presentation.pdf` with stem name `my_slides`:

**Generated Markdown** (`my_slides_slides.md`):
```markdown
![001](Slides/my_slides/my_slides_SLIDES_001.png)
![002](Slides/my_slides/my_slides_SLIDES_002.png)
![003](Slides/my_slides/my_slides_SLIDES_003.png)
...
```

## 🔧 Configuration

### Optional: Custom Poppler Path

If Poppler is installed in a custom location, uncomment and modify this line in `main.py`:

```python
poppler_path = r"C:\Path\To\poppler\bin"
pdf_images = convert_from_path(file_path, dpi=300, poppler_path=poppler_path)
```

### Adjust DPI

To change the image quality, modify the `dpi` parameter in the conversion step (default: 300):
```python
pdf_images = convert_from_path(file_path, dpi=150)  # Lower quality, smaller files
pdf_images = convert_from_path(file_path, dpi=600)  # Higher quality, larger files
```

## 📝 Logging

The script provides detailed logging information:
- ✨ Progress updates for each converted slide
- ⚠️ Warning and error messages
- ✅ Completion status

## 👤 Author

Richard Mulholland

## 📅 Version

- **v001** - Initial version (2025-11-23)

