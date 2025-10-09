import os
from datetime import datetime

import markdown
from bs4 import BeautifulSoup

from utils.seo_enhancer import SEOEnhancer
from utils.seo_validator import SEOValidator
from utils.template_manager import TemplateManager


class HtmlGenerator:
    """Generate static HTML from markdown content."""

    def __init__(
        self,
        template: str = "modern",
        color_scheme: str = "blue",
        font_family: str | None = None,
        enable_seo: bool = True,
    ):
        """Initialize HTML generator with markdown extensions and template options."""
        self.markdown_extensions = [
            "tables",
            "codehilite",
            "fenced_code",
            "toc",
            "attr_list",
        ]
        self.template = template
        self.color_scheme = color_scheme
        self.font_family = font_family
        self.template_manager = TemplateManager()
        self.enable_seo = enable_seo
        self.seo_enhancer = SEOEnhancer() if enable_seo else None
        self.seo_validator = SEOValidator() if enable_seo else None

    def generate(
        self, markdown_content, original_filename, metadata: dict | None = None
    ):
        """
        Generate HTML from markdown content.

        Args:
            markdown_content: Markdown text content
            original_filename: Original filename for title
            metadata: Optional metadata dict with description, keywords, author

        Returns:
            str: Complete HTML document (or tuple with SEO report if enabled)
        """
        try:
            # Convert markdown to HTML
            md = markdown.Markdown(extensions=self.markdown_extensions)
            content_html = md.convert(markdown_content)

            # Get title from filename
            title = os.path.splitext(original_filename)[0]

            # Use template manager for customizable templates
            html_document = self.template_manager.generate_html(
                content_html,
                title,
                self.template,
                self.color_scheme,
                self.font_family or "Arial",
            )

            # Apply SEO enhancements if enabled
            if self.enable_seo and self.seo_enhancer:
                description = None
                keywords = None
                author = None

                # Extract metadata if provided
                if metadata:
                    description = metadata.get("description")
                    keywords = metadata.get("keywords", [])
                    author = metadata.get("author")

                # Generate description from content if not provided
                if not description:
                    # Extract first paragraph as description
                    text = BeautifulSoup(
                        content_html, "html.parser"
                    ).get_text()  # noqa: E501
                    words = text.split()[:30]
                    description = " ".join(words) + (  # noqa: E501
                        "..." if len(words) >= 30 else ""
                    )

                # Enhance HTML with SEO optimizations
                html_document = self.seo_enhancer.enhance(
                    html_document,
                    title=title,
                    description=description,
                    keywords=keywords if keywords else [],
                    author=author if author else "",
                )

            return html_document

        except Exception as e:
            raise RuntimeError(f"Error generating HTML: {str(e)}") from e

    def validate_seo(self, html_content: str, title: str | None = None):
        """
        Validate HTML for SEO best practices.

        Args:
            html_content: HTML to validate
            title: Optional title for context

        Returns:
            Dict with SEO score and recommendations
        """
        if not self.seo_validator:
            return None

        return self.seo_validator.validate(html_content, title)

    def _create_html_document(self, content_html, filename, toc=None):
        """Create complete HTML document with styling."""
        title = os.path.splitext(filename)[0]

        html_template = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <style>
        {self._get_css_styles()}
    </style>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.8.0/styles/github.min.css">
    <script src="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.8.0/highlight.min.js"></script>
</head>
<body>
    <div class="container">
        <header class="header">
            <h1 class="site-title">{title}</h1>
            <p class="generated-info">Generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
        </header>

        {self._generate_toc_html(toc) if toc else ''}

        <main class="content">
            {content_html}
        </main>

        <footer class="footer">
            <p>Converted from: {filename}</p>
            <p>Generated by File to Markdown Converter</p>
        </footer>
    </div>

    <script>
        hljs.highlightAll();
        {self._get_javascript()}
    </script>
</body>
</html>"""

        return html_template

    def _generate_toc_html(self, toc):
        """Generate table of contents HTML."""
        if not toc:
            return ""

        return f"""
        <nav class="toc">
            <h2>Table of Contents</h2>
            {toc}
        </nav>
        """

    def _get_css_styles(self):
        """Get CSS styles for the HTML document."""
        return """
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
            line-height: 1.6;
            color: #333;
            background-color: #fff;
        }

        .container {
            max-width: 1000px;
            margin: 0 auto;
            padding: 20px;
        }

        .header {
            border-bottom: 2px solid #e1e5e9;
            margin-bottom: 2rem;
            padding-bottom: 1rem;
        }

        .site-title {
            color: #2c3e50;
            margin-bottom: 0.5rem;
            font-size: 2.5rem;
        }

        .generated-info {
            color: #666;
            font-size: 0.9rem;
        }

        .toc {
            background-color: #f8f9fa;
            border: 1px solid #e9ecef;
            border-radius: 0.25rem;
            padding: 1rem;
            margin-bottom: 2rem;
        }

        .toc h2 {
            color: #495057;
            margin-bottom: 0.5rem;
            font-size: 1.25rem;
        }

        .toc ul {
            list-style-type: none;
            padding-left: 0;
        }

        .toc li {
            margin: 0.25rem 0;
        }

        .toc a {
            color: #007bff;
            text-decoration: none;
        }

        .toc a:hover {
            text-decoration: underline;
        }

        .content {
            margin-bottom: 3rem;
        }

        .content h1, .content h2, .content h3, .content h4, .content h5, .content h6 {
            margin-top: 2rem;
            margin-bottom: 1rem;
            color: #2c3e50;
            line-height: 1.2;
        }

        .content h1 {
            font-size: 2.25rem;
            border-bottom: 1px solid #eaecef;
            padding-bottom: 0.3rem;
        }

        .content h2 {
            font-size: 1.75rem;
            border-bottom: 1px solid #eaecef;
            padding-bottom: 0.3rem;
        }

        .content h3 {
            font-size: 1.5rem;
        }

        .content h4 {
            font-size: 1.25rem;
        }

        .content h5 {
            font-size: 1.1rem;
        }

        .content h6 {
            font-size: 1rem;
        }

        .content p {
            margin-bottom: 1rem;
        }

        .content a {
            color: #007bff;
            text-decoration: none;
        }

        .content a:hover {
            text-decoration: underline;
        }

        .content ul, .content ol {
            margin-bottom: 1rem;
            padding-left: 2rem;
        }

        .content li {
            margin-bottom: 0.25rem;
        }

        .content table {
            border-collapse: collapse;
            width: 100%;
            margin-bottom: 1rem;
            border: 1px solid #dee2e6;
        }

        .content th, .content td {
            padding: 0.75rem;
            text-align: left;
            border-bottom: 1px solid #dee2e6;
        }

        .content th {
            background-color: #f8f9fa;
            font-weight: 600;
            border-bottom: 2px solid #dee2e6;
        }

        .content tr:nth-child(even) {
            background-color: #f8f9fa;
        }

        .content blockquote {
            border-left: 0.25rem solid #007bff;
            margin: 1rem 0;
            padding: 0 1rem;
            color: #6a737d;
        }

        .content code {
            background-color: #f6f8fa;
            border-radius: 0.25rem;
            font-size: 85%;
            margin: 0;
            padding: 0.2em 0.4em;
        }

        .content pre {
            background-color: #f6f8fa;
            border-radius: 0.375rem;
            font-size: 85%;
            line-height: 1.45;
            overflow: auto;
            padding: 1rem;
            margin-bottom: 1rem;
        }

        .content pre code {
            background-color: transparent;
            border: 0;
            font-size: 100%;
            margin: 0;
            padding: 0;
        }

        .content img {
            max-width: 100%;
            height: auto;
            margin: 1rem 0;
        }

        .footer {
            border-top: 1px solid #e1e5e9;
            padding-top: 1rem;
            text-align: center;
            color: #666;
            font-size: 0.9rem;
        }

        .footer p {
            margin-bottom: 0.5rem;
        }

        /* Responsive design */
        @media (max-width: 768px) {
            .container {
                padding: 10px;
            }

            .site-title {
                font-size: 2rem;
            }

            .content h1 {
                font-size: 1.75rem;
            }

            .content h2 {
                font-size: 1.5rem;
            }
        }

        /* Print styles */
        @media print {
            .container {
                max-width: none;
                padding: 0;
            }

            .header {
                border-bottom: 1px solid #000;
            }

            .footer {
                border-top: 1px solid #000;
            }

            a {
                color: #000 !important;
                text-decoration: none !important;
            }

            .toc {
                break-inside: avoid;
            }
        }
        """

    def _get_javascript(self):
        """Get JavaScript for enhanced functionality."""
        return """
        // Smooth scrolling for anchor links
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
            button.style.position = 'absolute';
            button.style.top = '5px';
            button.style.right = '5px';
            button.style.padding = '4px 8px';
            button.style.fontSize = '12px';
            button.style.border = '1px solid #ccc';
            button.style.backgroundColor = '#fff';
            button.style.cursor = 'pointer';
            button.style.borderRadius = '3px';

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
        """
