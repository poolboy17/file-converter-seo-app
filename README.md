# File Converter with SEO Optimization

A powerful Python web application for converting multiple document formats (DOCX, CSV, TXT, WordPress WXR) into clean Markdown and SEO-optimized HTML. Built with Streamlit for an intuitive user experience.

## Features

### Core Conversion
- **Multi-Format Support**: Convert DOCX, CSV, TXT, and WordPress WXR files
- **Batch Processing**: Handle multiple files simultaneously
- **Format Preservation**: Maintains document structure and formatting
- **Universal Output**: Generate Markdown, HTML, or both

### Image Management
- **Automatic Extraction**: Pulls embedded images from DOCX files
- **Remote Downloads**: Fetches images from WordPress exports
- **Smart Optimization**: Resizes (max 1200px) and compresses (85% quality)
- **Deduplication**: Content-based hashing prevents duplicate storage

### HTML Generation
- **4 Template Styles**: Modern, Minimal, Classic, Dark
- **5 Color Schemes**: Blue, Green, Purple, Red, Orange
- **Font Customization**: Sans-serif, Serif, Monospace options
- **Pure CSS**: No external dependencies

### SEO Optimization
- **8-Point Validation**: Comprehensive SEO analysis with scoring (0-100)
- **Automatic Enhancement**: Injects meta tags, Open Graph, Schema.org structured data
- **Detailed Reporting**: Grade-based feedback with actionable recommendations
- **Toggle Control**: Enable/disable SEO features as needed

**SEO Checks:**
- Title tags (30-60 characters)
- Meta descriptions (120-160 characters)
- Heading hierarchy (H1-H6)
- Image alt text coverage
- Internal/external links
- Content length (300+ words)
- Open Graph tags
- Structured data (JSON-LD)

### Static Site Generation
- **SSG Support**: Generate frontmatter for Jekyll, Hugo, Astro
- **Complete Sites**: Create navigable static websites with index pages
- **Clean Structure**: Organized folders (pages/, assets/)
- **ZIP Downloads**: Package everything for easy deployment

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
2. **Choose Output Format**: Select Markdown, HTML, or Both
3. **Configure Options** (optional):
   - Select HTML template and color scheme
   - Choose font family
   - Enable/disable SEO enhancements
   - Add frontmatter for static site generators
4. **Convert**: Click "Convert All Files"
5. **Download**: Get individual files or create a ZIP archive

### SEO Optimization

Enable SEO enhancements in the sidebar to automatically add:
- Essential meta tags (description, keywords, viewport, robots)
- Open Graph tags for social media sharing
- Twitter Card metadata
- Schema.org structured data (Article format)
- Semantic HTML5 elements
- Image lazy loading attributes
- Link security attributes

View detailed SEO reports in the "SEO Report" tab with:
- Overall score (0-100) and letter grade (A-F)
- Critical issues requiring attention
- Warnings for improvements
- Successful elements
- Actionable recommendations

### Static Site Generation

1. Select HTML or Both output format
2. Convert your files
3. Navigate to the "Download" tab
4. Enter a site name
5. Click "Generate Static Site"
6. Download the complete website as a ZIP file

The generated site includes:
- `index.html` - Navigation page listing all documents
- `pages/` - Individual HTML pages for each converted file
- `assets/` - Images, CSS, and other resources

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
