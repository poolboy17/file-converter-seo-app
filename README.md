# File to Markdown Converter

A powerful Python web application for converting multiple document formats (DOCX, CSV, TXT, WordPress WXR) into clean Markdown. Built with Streamlit for an intuitive user experience.

## Features

### Core Conversion

- **Multi-Format Support**: Convert DOCX, CSV, TXT, and WordPress WXR files
- **Batch Processing**: Handle multiple files simultaneously
- **Format Preservation**: Maintains document structure and formatting
- **Clean Markdown Output**: Professional, well-formatted Markdown files

### Image Management

- **Automatic Extraction**: Pulls embedded images from DOCX files
- **Remote Downloads**: Fetches images from WordPress exports
- **Smart Optimization**: Resizes (max 1200px) and compresses (85% quality)
- **Deduplication**: Content-based hashing prevents duplicate storage

### Static Site Generator Support

- **SSG Frontmatter**: Generate frontmatter for Jekyll, Hugo, Astro
- **Quick Presets**: One-click configuration for popular SSGs
- **Metadata Extraction**: Automatically extract and format document metadata
- **ZIP Downloads**: Package all files and images for easy deployment

## Installation

### Requirements

- Python 3.11 or higher
- pip or uv package manager

### Setup

1. Clone the repository:

```bash
git clone https://github.com/poolboy17/file-converter-seo-app.git
cd file-converter-seo-app
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

Or using uv:

```bash
uv sync
```

3. Run the application:

```bash
streamlit run app.py --server.port 5000
```

4. Open your browser to `http://localhost:5000`

## Usage

### Basic Conversion

1. **Upload Files**: Click "Browse files" and select one or more documents
1. **Configure Options** (optional):
   - Include metadata in output
   - Add frontmatter for static site generators (Jekyll, Hugo, Astro)
   - Select quick presets for common use cases
1. **Convert**: Click "Convert All Files"
1. **Download**: Get individual Markdown files or create a ZIP archive

### Static Site Generator Frontmatter

Add YAML frontmatter to your Markdown files for popular static site generators:

- **Jekyll**: Includes layout, title, date, categories, and tags
- **Hugo**: Includes title, date, draft status, and taxonomies
- **Astro**: Includes title, description, pubDate, and layout

Quick preset options:
- Jekyll Blog
- Hugo Docs
- Astro Site
- Plain Markdown (no frontmatter)

## Project Structure

```
file-converter-seo-app/
├── app.py                      # Main Streamlit application
├── converters/                 # Format-specific converters
│   ├── __init__.py
│   ├── docx_converter.py      # Word document converter
│   ├── csv_converter.py       # CSV table converter
│   ├── txt_converter.py       # Plain text converter
│   └── wxr_converter.py       # WordPress export converter
├── utils/                      # Utility modules
│   ├── frontmatter_generator.py   # SSG frontmatter creation
│   ├── template_manager.py        # HTML template system
│   ├── html_generator.py          # Markdown to HTML conversion
│   ├── image_handler.py           # Image extraction and optimization
│   ├── static_site_generator.py   # Complete site generation
│   ├── seo_validator.py           # SEO analysis and scoring
│   ├── seo_enhancer.py            # Automatic SEO improvements
│   └── file_utils.py              # File packaging utilities
├── templates/                  # HTML templates
│   └── html_template.html
├── .streamlit/                 # Streamlit configuration
│   └── config.toml
├── pyproject.toml             # Python dependencies
└── README.md                  # This file
```

## Technology Stack

- **Framework**: [Streamlit](https://streamlit.io/) - Web application framework
- **Document Parsing**:
  - [python-docx](https://python-docx.readthedocs.io/) - DOCX files
  - [pandas](https://pandas.pydata.org/) - CSV files
  - [BeautifulSoup4](https://www.crummy.com/software/BeautifulSoup/) - HTML/XML parsing
- **Content Processing**:
  - [markdown](https://python-markdown.github.io/) - Markdown to HTML conversion
  - [Pillow](https://pillow.readthedocs.io/) - Image processing
  - [PyYAML](https://pyyaml.org/) - YAML frontmatter generation

## Configuration

### Streamlit Settings

Edit `.streamlit/config.toml` to customize:

```toml
[server]
headless = true
address = "0.0.0.0"
port = 5000

[theme]
# Add custom theme settings if desired
```

### SEO Configuration

SEO validation rules are configured in `utils/seo_validator.py`:

- Title length: 30-60 characters (optimal)
- Meta description: 120-160 characters (optimal)
- Minimum content length: 300 words
- Required heading structure: Single H1, hierarchical H2-H6

## Development

### Running Tests

```bash
# Run with test files in the uploads folder
streamlit run app.py --server.port 5000
```

### VS Code (local development)

If you're migrating from Replit to VS Code, the repo includes a small helper to create a virtual environment and install dependencies.

1. Run the setup task (or run the PowerShell script):

```powershell
.\scripts\setup.ps1
```

2. Activate the virtual environment and run the app:

```powershell
.\.venv\Scripts\Activate.ps1
streamlit run app.py --server.port 5000
```

3. You can also use the included VS Code tasks: open the Command Palette -> Tasks: Run Task -> choose "Python: Create venv and install deps" or "Streamlit: Run app".

### Adding New Converters

1. Create a new converter in `converters/`:

```python
class NewFormatConverter:
    def __init__(self, file):
        self.file = file
    
    def convert(self):
        # Conversion logic
        return markdown_content
```

2. Register in `app.py`:

```python
CONVERTERS = {
    '.newformat': NewFormatConverter,
    # ... existing converters
}
```

### Extending SEO Rules

Add new validation rules in `utils/seo_validator.py`:

```python
def validate_new_rule(self, soup):
    # Validation logic
    if condition:
        self.issues.append("Issue description")
        return 0
    return 10  # Points for passing
```

## Deployment

### Replit

This application is optimized for Replit deployment:

1. Fork or import the repository
2. Configure environment variables if needed
3. Click "Run" or "Deploy"

### Docker

```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY . .

RUN pip install -r requirements.txt

EXPOSE 5000

CMD ["streamlit", "run", "app.py", "--server.port=5000", "--server.address=0.0.0.0"]
```

### Heroku

```bash
# Create Procfile
echo "web: streamlit run app.py --server.port=\$PORT" > Procfile

# Deploy
git push heroku main
```

## Security Considerations

- No sensitive data is stored or logged
- File uploads are processed in memory
- Generated HTML is sanitized
- External image URLs are validated before download
- No code execution in user-provided content

## Performance

- Batch processing: Multiple files converted simultaneously
- Image optimization: Automatic resizing and compression
- Memory efficient: In-memory ZIP generation
- No external API calls: All processing done locally

## Browser Support

- Chrome/Edge (recommended)
- Firefox
- Safari
- Opera

## License

This project is available under the MIT License. See [LICENSE](LICENSE) for details.

## Contributing

Contributions are welcome! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## Support

For issues, questions, or suggestions:

- Open an issue on GitHub
- Check existing documentation
- Review the project structure

## Changelog

See [CHANGELOG.md](CHANGELOG.md) for version history and updates.

## Acknowledgments

- Built with [Streamlit](https://streamlit.io/)
- Inspired by the need for clean, SEO-optimized document conversion
- Community feedback and contributions

---

**Made with ❤️ for content creators, bloggers, and web developers**
