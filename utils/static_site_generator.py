import io
import os
import zipfile
from datetime import datetime
from typing import Any, Dict, List


class StaticSiteGenerator:
    """Generate a complete static site from converted files."""

    def __init__(
        self,
        template: str = "modern",
        color_scheme: str = "blue",
        font_family: str = None,
    ):
        self.site_name = "Converted Site"
        self.template = template
        self.color_scheme = color_scheme
        self.font_family = font_family

    def generate_site(
        self,
        converted_files: List[Dict[str, Any]],
        site_name: str = None,
        image_handler=None,
    ) -> io.BytesIO:
        """
        Generate a complete static site with navigation.

        Args:
            converted_files: List of converted file data with HTML content
            site_name: Name of the site
            image_handler: Optional ImageHandler with extracted images

        Returns:
            io.BytesIO: ZIP buffer containing the complete site
        """
        if site_name:
            self.site_name = site_name

        zip_buffer = io.BytesIO()

        with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zip_file:
            # Generate index page
            index_html = self._generate_index_page(converted_files)
            zip_file.writestr("index.html", index_html)

            # Generate individual pages with navigation
            for file_data in converted_files:
                if file_data.get("html_content"):
                    # Create sanitized filename
                    page_name = self._sanitize_filename(file_data["original_name"])
                    page_html = self._generate_page_with_nav(file_data, converted_files)
                    zip_file.writestr(f"pages/{page_name}.html", page_html)

            # Generate CSS file
            css_content = self._generate_site_css()
            zip_file.writestr("assets/style.css", css_content)

            # Generate navigation JS
            js_content = self._generate_site_js()
            zip_file.writestr("assets/script.js", js_content)

            # Add images if available
            if image_handler and hasattr(image_handler, "images"):
                images = image_handler.get_all_images()
                if images:
                    for image_hash, filename in images.items():
                        # Get the image data
                        if (
                            hasattr(image_handler, "image_data")
                            and image_hash in image_handler.image_data
                        ):
                            image_data = image_handler.image_data[image_hash]
                            zip_file.writestr(f"assets/{filename}", image_data)

            # Generate README
            readme = self._generate_readme(converted_files)
            zip_file.writestr("README.md", readme)

        zip_buffer.seek(0)
        return zip_buffer

    def _generate_index_page(self, converted_files: List[Dict[str, Any]]) -> str:
        """Generate the index/home page with links to all documents."""
        file_list_html = []

        for file_data in converted_files:
            page_name = self._sanitize_filename(file_data["original_name"])
            file_type = file_data.get("file_type", "unknown").upper()

            file_list_html.append(
                f"""
            <div class="file-card">
                <div class="file-icon">{self._get_file_icon(file_data.get('file_type'))}</div>
                <div class="file-info">
                    <h3><a href="pages/{page_name}.html">{file_data['original_name']}</a></h3>
                    <p class="file-meta">Type: {file_type}</p>
                </div>
            </div>
            """
            )

        html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{self.site_name}</title>
    <link rel="stylesheet" href="assets/style.css">
</head>
<body>
    <header class="site-header">
        <div class="container">
            <h1>{self.site_name}</h1>
            <p class="subtitle">Converted Documents</p>
        </div>
    </header>
    
    <main class="container">
        <section class="intro">
            <h2>Welcome</h2>
            <p>This site contains {len(converted_files)} converted document(s). Click on any document below to view it.</p>
        </section>
        
        <section class="file-list">
            <h2>Documents</h2>
            <div class="file-grid">
                {''.join(file_list_html)}
            </div>
        </section>
    </main>
    
    <footer class="site-footer">
        <div class="container">
            <p>Generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
            <p>Created with File to Markdown Converter</p>
        </div>
    </footer>
    
    <script src="assets/script.js"></script>
</body>
</html>"""

        return html

    def _generate_page_with_nav(
        self, current_file: Dict[str, Any], all_files: List[Dict[str, Any]]
    ) -> str:
        """Generate a page with navigation to other documents."""
        # The HTML content is already styled with the user's template
        # We'll inject a navigation sidebar into it
        content = current_file.get("html_content", "")

        # Fix image paths - pages are in pages/ subdirectory, so need ../ prefix
        content = content.replace('src="assets/', 'src="../assets/')
        content = content.replace("](assets/", "](../assets/")

        # Build navigation HTML
        nav_items = []
        current_page_name = self._sanitize_filename(current_file["original_name"])

        for file_data in all_files:
            page_name = self._sanitize_filename(file_data["original_name"])
            is_current = page_name == current_page_name
            active_class = ' class="active"' if is_current else ""
            nav_items.append(
                f'<li{active_class}><a href="{page_name}.html">{file_data["original_name"]}</a></li>'
            )

        nav_html = f"""
        <div class="site-nav-sidebar">
            <div class="nav-header">
                <a href="../index.html" class="home-link">← Home</a>
                <h3>Documents</h3>
            </div>
            <nav class="doc-nav">
                <ul>
                    {''.join(nav_items)}
                </ul>
            </nav>
        </div>
        <style>
            body {{ display: flex; gap: 2rem; max-width: 1400px; margin: 0 auto; padding: 2rem; }}
            .site-nav-sidebar {{ width: 250px; background: rgba(255,255,255,0.05); padding: 1.5rem; border-radius: 8px; height: fit-content; position: sticky; top: 20px; flex-shrink: 0; }}
            .nav-header h3 {{ margin: 1rem 0; }}
            .nav-header .home-link {{ display: block; margin-bottom: 1rem; opacity: 0.8; }}
            .doc-nav ul {{ list-style: none; padding: 0; }}
            .doc-nav li {{ margin-bottom: 0.5rem; }}
            .doc-nav a {{ display: block; padding: 0.5rem; border-radius: 4px; transition: background 0.2s; }}
            .doc-nav li.active a {{ font-weight: bold; }}
            @media (max-width: 768px) {{ body {{ flex-direction: column; }} .site-nav-sidebar {{ width: 100%; position: static; }} }}
        </style>
        """

        # Inject navigation after opening body tag
        if "<body>" in content:
            content = content.replace("<body>", f"<body>{nav_html}", 1)

        return content

    def _generate_site_css(self) -> str:
        """Generate CSS for the static site."""
        return """/* Reset and Base Styles */
* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

body {
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
    line-height: 1.6;
    color: #333;
    background-color: #f5f5f5;
}

.container {
    max-width: 1200px;
    margin: 0 auto;
    padding: 0 20px;
}

/* Header Styles */
.site-header {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    padding: 2rem 0;
    box-shadow: 0 2px 10px rgba(0,0,0,0.1);
}

.site-header h1 {
    font-size: 2.5rem;
    margin-bottom: 0.5rem;
}

.subtitle {
    font-size: 1.1rem;
    opacity: 0.9;
}

.page-header {
    background: #667eea;
    color: white;
    padding: 1rem 0;
    box-shadow: 0 2px 5px rgba(0,0,0,0.1);
}

.home-link {
    color: white;
    text-decoration: none;
    display: inline-block;
    margin-bottom: 0.5rem;
    opacity: 0.9;
    transition: opacity 0.2s;
}

.home-link:hover {
    opacity: 1;
}

/* Main Content */
main {
    padding: 3rem 0;
}

.intro {
    background: white;
    padding: 2rem;
    border-radius: 8px;
    margin-bottom: 2rem;
    box-shadow: 0 2px 5px rgba(0,0,0,0.05);
}

.intro h2 {
    color: #667eea;
    margin-bottom: 1rem;
}

/* File Grid */
.file-list {
    margin-top: 2rem;
}

.file-list h2 {
    margin-bottom: 1.5rem;
    color: #333;
}

.file-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
    gap: 1.5rem;
}

.file-card {
    background: white;
    border-radius: 8px;
    padding: 1.5rem;
    box-shadow: 0 2px 5px rgba(0,0,0,0.05);
    transition: transform 0.2s, box-shadow 0.2s;
    display: flex;
    align-items: center;
    gap: 1rem;
}

.file-card:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 15px rgba(0,0,0,0.1);
}

.file-icon {
    font-size: 2.5rem;
    width: 60px;
    height: 60px;
    display: flex;
    align-items: center;
    justify-content: center;
    background: #f0f0f0;
    border-radius: 8px;
}

.file-info h3 {
    margin-bottom: 0.5rem;
}

.file-info h3 a {
    color: #667eea;
    text-decoration: none;
}

.file-info h3 a:hover {
    text-decoration: underline;
}

.file-meta {
    color: #666;
    font-size: 0.9rem;
}

/* Page Layout */
.page-layout {
    display: flex;
    gap: 2rem;
    max-width: 1400px;
    margin: 2rem auto;
    padding: 0 20px;
}

.sidebar {
    width: 250px;
    background: white;
    padding: 1.5rem;
    border-radius: 8px;
    box-shadow: 0 2px 5px rgba(0,0,0,0.05);
    height: fit-content;
    position: sticky;
    top: 20px;
}

.sidebar h3 {
    margin-bottom: 1rem;
    color: #667eea;
}

.doc-nav ul {
    list-style: none;
}

.doc-nav li {
    margin-bottom: 0.5rem;
}

.doc-nav a {
    color: #333;
    text-decoration: none;
    display: block;
    padding: 0.5rem;
    border-radius: 4px;
    transition: background-color 0.2s;
}

.doc-nav a:hover {
    background-color: #f0f0f0;
}

.doc-nav li.active a {
    background-color: #667eea;
    color: white;
}

.page-content {
    flex: 1;
    background: white;
    padding: 2rem;
    border-radius: 8px;
    box-shadow: 0 2px 5px rgba(0,0,0,0.05);
}

/* Article Styles */
article h1, article h2, article h3, article h4, article h5, article h6 {
    margin-top: 1.5rem;
    margin-bottom: 1rem;
    color: #2c3e50;
}

article h1 {
    font-size: 2.25rem;
    border-bottom: 2px solid #eaecef;
    padding-bottom: 0.5rem;
}

article h2 {
    font-size: 1.75rem;
    border-bottom: 1px solid #eaecef;
    padding-bottom: 0.3rem;
}

article p {
    margin-bottom: 1rem;
}

article a {
    color: #667eea;
    text-decoration: none;
}

article a:hover {
    text-decoration: underline;
}

article ul, article ol {
    margin-bottom: 1rem;
    padding-left: 2rem;
}

article table {
    border-collapse: collapse;
    width: 100%;
    margin-bottom: 1rem;
}

article th, article td {
    padding: 0.75rem;
    text-align: left;
    border: 1px solid #dee2e6;
}

article th {
    background-color: #f8f9fa;
    font-weight: 600;
}

article tr:nth-child(even) {
    background-color: #f8f9fa;
}

article code {
    background-color: #f6f8fa;
    padding: 0.2em 0.4em;
    border-radius: 3px;
    font-size: 85%;
}

article pre {
    background-color: #f6f8fa;
    padding: 1rem;
    border-radius: 6px;
    overflow-x: auto;
    margin-bottom: 1rem;
}

article pre code {
    background-color: transparent;
    padding: 0;
}

article img {
    max-width: 100%;
    height: auto;
    border-radius: 4px;
    margin: 1rem 0;
}

article blockquote {
    border-left: 4px solid #667eea;
    padding-left: 1rem;
    margin: 1rem 0;
    color: #6a737d;
}

/* Footer */
.site-footer {
    background: #2c3e50;
    color: white;
    padding: 2rem 0;
    margin-top: 4rem;
    text-align: center;
}

.site-footer p {
    margin-bottom: 0.5rem;
    opacity: 0.9;
}

/* Responsive Design */
@media (max-width: 768px) {
    .page-layout {
        flex-direction: column;
    }
    
    .sidebar {
        width: 100%;
        position: static;
    }
    
    .file-grid {
        grid-template-columns: 1fr;
    }
    
    .site-header h1 {
        font-size: 2rem;
    }
}

/* Print Styles */
@media print {
    .site-header, .page-header, .sidebar, .site-footer, .home-link {
        display: none;
    }
    
    .page-content {
        box-shadow: none;
        padding: 0;
    }
}"""

    def _generate_site_js(self) -> str:
        """Generate JavaScript for the static site."""
        return """// Smooth scrolling for anchor links
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            target.scrollIntoView({
                behavior: 'smooth',
                block: 'start'
            });
        }
    });
});

// Add copy button to code blocks
document.querySelectorAll('pre code').forEach(block => {
    const button = document.createElement('button');
    button.textContent = 'Copy';
    button.className = 'copy-button';
    button.style.cssText = `
        position: absolute;
        top: 5px;
        right: 5px;
        padding: 4px 8px;
        font-size: 12px;
        border: 1px solid #ccc;
        background: #fff;
        cursor: pointer;
        border-radius: 3px;
    `;
    
    const pre = block.parentElement;
    pre.style.position = 'relative';
    pre.appendChild(button);
    
    button.addEventListener('click', () => {
        navigator.clipboard.writeText(block.textContent).then(() => {
            button.textContent = 'Copied!';
            setTimeout(() => {
                button.textContent = 'Copy';
            }, 2000);
        });
    });
});

// Initialize
document.addEventListener('DOMContentLoaded', function() {
    console.log('Static site loaded successfully');
});"""

    def _generate_readme(self, converted_files: List[Dict[str, Any]]) -> str:
        """Generate README for the static site."""
        file_list = "\n".join([f"- {f['original_name']}" for f in converted_files])

        return f"""# {self.site_name}

This is a static website generated from converted documents.

## Contents

{file_list}

## Structure

- `index.html` - Home page with list of all documents
- `pages/` - Individual document pages with navigation
- `assets/` - CSS and JavaScript files

## Usage

1. Open `index.html` in a web browser
2. Click on any document to view it
3. Use the sidebar navigation to browse between documents
4. Use the "Back to Home" link to return to the index

## Serving the Site

You can serve this site using any static web server:

### Python
```bash
python -m http.server 8000
```

### Node.js
```bash
npx http-server
```

### PHP
```bash
php -S localhost:8000
```

Then open http://localhost:8000 in your browser.

---

Generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
Created with File to Markdown Converter
"""

    def _sanitize_filename(self, filename: str) -> str:
        """Sanitize filename for use in URLs."""
        import re

        # Remove extension
        name = os.path.splitext(filename)[0]
        # Convert to lowercase and replace spaces/special chars with hyphens
        name = re.sub(r"[^\w\s-]", "", name.lower())
        name = re.sub(r"[-\s]+", "-", name)
        return name.strip("-")

    def _get_file_icon(self, file_type: str) -> str:
        """Get emoji icon for file type."""
        icons = {"docx": "📝", "csv": "📊", "txt": "📄", "wxr": "📰", "md": "📋"}
        return icons.get(file_type, "📄")
