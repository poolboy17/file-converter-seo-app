# Overview

This is a file conversion application that transforms various document formats (DOCX, CSV, TXT, WordPress WXR) into clean Markdown and static HTML. Built with Streamlit, it provides a web interface for batch converting files while preserving formatting, automatically extracting/downloading images, and generating static site generator-compatible frontmatter. The application can produce individual converted files or complete static websites with navigation and customizable styling.

# User Preferences

Preferred communication style: Simple, everyday language.

# System Architecture

## Application Framework
**Problem**: Need an accessible web interface for file conversion without requiring users to install software locally.

**Solution**: Streamlit-based web application that runs in the browser.

**Rationale**: Streamlit provides rapid development of data applications with minimal frontend code. Users can upload files, configure conversion options, and download results through a simple web UI.

## Converter Architecture
**Problem**: Different file formats require specialized parsing and conversion logic.

**Solution**: Plugin-based converter system with dedicated converter classes for each file type (DOCX, CSV, TXT, WXR).

**Design Pattern**: Each converter implements a common `convert()` method interface, making it easy to add new file format support. Converters are registered in a dictionary and selected based on file extension.

- **DocxConverter**: Uses python-docx library to parse Word documents, extracting text, formatting, and embedded images
- **CsvConverter**: Leverages pandas for CSV parsing with automatic encoding detection and markdown table generation
- **TxtConverter**: Plain text processor with encoding fallback support
- **WxrConverter**: XML parser for WordPress export files using ElementTree and BeautifulSoup

## Content Processing Pipeline
**Problem**: Need flexible output supporting multiple formats and use cases.

**Solution**: Multi-stage conversion pipeline: File → Markdown → HTML → Static Site

**Flow**:
1. File upload and format detection
2. Conversion to Markdown (base format)
3. Optional HTML generation from Markdown
4. Optional static site generation with navigation

## Image Handling
**Problem**: Embedded and remote images need to be extracted and properly referenced in converted content.

**Solution**: Centralized ImageHandler class that manages image extraction, downloading, optimization, and local storage.

**Implementation**:
- **DOCX Extraction**: Accesses document relationship parts to extract embedded images with their binary data
- **WXR Download**: Parses img tags from HTML content and downloads images from URLs
- **Optimization**: Uses Pillow to resize (max 1200px width) and compress images (85% JPEG quality)
- **Deduplication**: Content-based MD5 hashing prevents duplicate storage
- **Path Management**: Images stored with unique filenames in assets/ folder
- **Archive Integration**: Binary data bundled into ZIP downloads and static sites
- **Relative Paths**: Static site pages use ../assets/ to correctly reference images from pages/ subdirectory

**Recent Change (2025-10-08)**: Completed full image extraction pipeline with proper path handling for static sites.

## HTML Generation
**Problem**: Users need visually appealing HTML output with customization options.

**Solution**: Template-based HTML generator with multiple themes and color schemes.

**Components**:
- **HtmlGenerator**: Converts markdown to HTML using Python-Markdown with extensions (tables, code highlighting, TOC)
- **TemplateManager**: Provides 4 template styles (modern, minimal, classic, dark) and 5 color schemes
- Templates use pure CSS for styling without external dependencies

## Static Site Generator Support
**Problem**: Users may want to import converted content into Jekyll, Hugo, or Astro sites.

**Solution**: Frontmatter generator that creates SSG-compatible metadata headers.

**Implementation**: 
- Extracts metadata from source files (dates, authors, categories)
- Formats as YAML frontmatter specific to each SSG's conventions
- Prepends frontmatter to markdown output

## Static Site Generation
**Problem**: Multiple converted files should be navigable as a cohesive website.

**Solution**: StaticSiteGenerator creates a complete site structure with index page and navigation.

**Output Structure**:
```
site.zip
├── index.html (listing page)
├── pages/
│   ├── document1.html
│   └── document2.html
└── assets/
    ├── style.css
    └── images/
```

## SEO Optimization
**Problem**: Generated HTML pages need search engine optimization for better discoverability and ranking.

**Solution**: Comprehensive SEO validation and enhancement system with automatic meta tag injection and semantic improvements.

**Components**:
- **SEOValidator**: Analyzes HTML for 8 key SEO factors with scoring (0-100) and grading (A-F)
- **SEOEnhancer**: Automatically injects missing SEO elements into HTML output
- **UI Integration**: Toggle control in sidebar, dedicated SEO Report tab showing detailed analysis

**Validation Checks**:
1. **Title Tags**: Length optimization (30-60 characters)
2. **Meta Description**: Presence and length (120-160 characters)
3. **Heading Structure**: H1-H6 hierarchy and proper usage
4. **Image Alt Text**: Accessibility and SEO coverage
5. **Link Quality**: Internal/external link presence and attributes
6. **Content Length**: Minimum 300 words recommended
7. **Open Graph Tags**: Social media sharing metadata
8. **Structured Data**: Schema.org JSON-LD markup

**Enhancement Features**:
- Meta tags (description, keywords, author, viewport, robots)
- Open Graph protocol tags (og:title, og:description, og:type, og:url)
- Twitter Card metadata
- Schema.org structured data (Article format with JSON-LD)
- Canonical URL links
- Semantic HTML5 elements (header, main, article, footer)
- Image lazy loading attributes
- Link security attributes (rel="noopener" for external links)

**Scoring System**:
- 90-100: Grade A (🟢) - Excellent SEO
- 80-89: Grade B (🟡) - Good SEO
- 70-79: Grade C (🟠) - Fair SEO
- 60-69: Grade D (🔴) - Poor SEO
- Below 60: Grade F (⚫) - Critical issues

**User Interface**:
- Sidebar checkbox: "Enable SEO enhancements" (default: enabled)
- SEO Report tab displays: score metric, letter grade, issues, warnings, successes, recommendations
- Reports generated per file during HTML conversion
- Toggle on/off to compare SEO-enhanced vs basic HTML

**Recent Change (2025-10-08)**: Completed SEO optimization system with validation, enhancement, and reporting. E2E tested and verified working correctly.

## File Packaging
**Problem**: Users need all converted files and assets bundled for easy download.

**Solution**: ZIP file generation that packages markdown, HTML, images, and metadata.

**Implementation**: Uses Python's zipfile module to create in-memory ZIP archives with organized folder structure.

# External Dependencies

## Core Libraries
- **Streamlit**: Web application framework for the user interface
- **python-docx**: DOCX file parsing and structure extraction
- **pandas**: CSV file parsing and data manipulation
- **markdown**: Markdown to HTML conversion with extensions
- **BeautifulSoup4**: HTML/XML parsing for WordPress exports
- **Pillow (PIL)**: Image processing and format conversion

## Data Formats Supported
- DOCX (Microsoft Word)
- CSV (Comma-separated values)
- TXT (Plain text with encoding detection)
- WXR (WordPress eXtended RSS export format)

## Output Formats
- Markdown (.md) - Universal format
- HTML (.html) - Standalone web pages
- Static sites (ZIP) - Complete website bundles

## Static Site Generators
- Jekyll (Ruby-based)
- Hugo (Go-based)
- Astro (JavaScript-based)

Frontmatter is generated in formats compatible with each platform's conventions.

## Image Processing
- Supports common formats: PNG, JPEG, GIF, BMP, SVG
- Extracts embedded images from DOCX files
- Downloads remote images from URLs in WordPress exports
- Content-based hashing prevents duplicate storage