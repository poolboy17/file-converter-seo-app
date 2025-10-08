# Architecture Documentation

## Overview

This document describes the technical architecture of the File Converter with SEO Optimization application.

## System Architecture

### High-Level Design

```
┌─────────────────────────────────────────────────────────┐
│                    Streamlit Web UI                      │
│  (File Upload, Configuration, Preview, Download)        │
└──────────────────────┬──────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────┐
│                  Application Core                        │
│                    (app.py)                             │
└──────────────────────┬──────────────────────────────────┘
                       │
          ┌────────────┼────────────┐
          ▼            ▼            ▼
    ┌─────────┐  ┌─────────┐  ┌─────────┐
    │Converter│  │  Utils  │  │  Image  │
    │ System  │  │ System  │  │ Handler │
    └─────────┘  └─────────┘  └─────────┘
```

## Component Architecture

### 1. Presentation Layer (Streamlit)

**Responsibilities:**
- User interface rendering
- File upload handling
- Configuration management
- Result display and download

**Key Components:**
- Sidebar: Configuration options
- Main area: File list, preview, download tabs
- SEO Report tab: Validation results

### 2. Application Layer (app.py)

**Responsibilities:**
- Request handling
- Workflow orchestration
- Converter selection
- State management

**Process Flow:**
```
Upload → Validate → Convert → Generate HTML → Apply SEO → Package → Download
```

### 3. Converter Layer

**Architecture Pattern:** Strategy Pattern

Each converter implements a common interface:
```python
class BaseConverter:
    def __init__(self, file):
        self.file = file
    
    def convert(self) -> str:
        """Convert file to Markdown"""
        pass
```

**Converters:**

1. **DocxConverter**
   - Library: python-docx
   - Extracts: Text, formatting, images
   - Features: Heading detection, list handling

2. **CsvConverter**
   - Library: pandas
   - Converts: Tables to Markdown
   - Features: Auto-encoding detection

3. **TxtConverter**
   - Processing: Direct text reading
   - Features: Encoding fallback

4. **WxrConverter**
   - Library: BeautifulSoup4, ElementTree
   - Extracts: Posts, pages, metadata
   - Features: Image URL extraction

### 4. Processing Pipeline

```
┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐
│  Source  │───▶│ Markdown │───▶│   HTML   │───▶│   SEO    │
│   File   │    │Generation│    │Generation│    │Enhanced  │
└──────────┘    └──────────┘    └──────────┘    └──────────┘
                                      │
                                      ▼
                                ┌──────────┐
                                │ Template │
                                │  System  │
                                └──────────┘
```

### 5. Utility Layer

**HtmlGenerator:**
```python
class HtmlGenerator:
    - Markdown to HTML conversion
    - Template application
    - SEO enhancement integration
    - Validation triggering
```

**TemplateManager:**
```python
class TemplateManager:
    - Template selection
    - Color scheme application
    - Font customization
    - CSS generation
```

**ImageHandler:**
```python
class ImageHandler:
    - Image extraction (DOCX)
    - Image downloading (URLs)
    - Image optimization
    - Deduplication (MD5 hash)
    - Path management
```

**SEOValidator:**
```python
class SEOValidator:
    - 8-point validation
    - Scoring algorithm (0-100)
    - Grade assignment (A-F)
    - Issue detection
    - Recommendation generation
```

**SEOEnhancer:**
```python
class SEOEnhancer:
    - Meta tag injection
    - Open Graph addition
    - Twitter Card setup
    - Schema.org structured data
    - Semantic HTML improvements
```

**StaticSiteGenerator:**
```python
class StaticSiteGenerator:
    - Index page creation
    - Navigation generation
    - File organization
    - Asset bundling
```

**FrontmatterGenerator:**
```python
class FrontmatterGenerator:
    - Metadata extraction
    - SSG-specific formatting
    - YAML generation
```

## Data Flow

### Conversion Flow

```
1. User uploads files
2. app.py validates file types
3. For each file:
   a. Select appropriate converter
   b. Convert to Markdown
   c. Extract metadata
   d. Generate frontmatter (optional)
   e. Convert to HTML (if requested)
   f. Apply SEO enhancements (if enabled)
   g. Validate SEO (if enabled)
4. Package results
5. Offer download
```

### Image Processing Flow

```
1. Detect images in source
2. Extract/download images
3. Calculate MD5 hash
4. Check for duplicates
5. Optimize if new:
   - Resize (max 1200px)
   - Compress (85% quality)
6. Store in memory
7. Update references in content
8. Include in ZIP archive
```

### SEO Enhancement Flow

```
1. Parse HTML with BeautifulSoup
2. Run validation checks:
   - Title tag analysis
   - Meta description check
   - Heading structure review
   - Image alt text verification
   - Link analysis
   - Content length assessment
   - Open Graph validation
   - Structured data check
3. Calculate score
4. If enhancements enabled:
   - Inject missing meta tags
   - Add Open Graph tags
   - Insert Schema.org data
   - Apply semantic improvements
5. Generate report
6. Return enhanced HTML
```

## Design Patterns

### 1. Strategy Pattern
- **Usage**: Converter selection
- **Benefit**: Easy to add new file formats

### 2. Factory Pattern
- **Usage**: Converter instantiation
- **Benefit**: Centralized object creation

### 3. Template Method Pattern
- **Usage**: HTML generation
- **Benefit**: Consistent structure with customization

### 4. Singleton Pattern
- **Usage**: ImageHandler (per session)
- **Benefit**: Centralized image management

## State Management

### Session State (Streamlit)
```python
st.session_state = {
    'image_handler': ImageHandler instance,
    'converted_files': List of conversion results,
    # Other ephemeral state
}
```

### No Persistent Storage
- All data in memory
- No database required
- Stateless between sessions

## Security Architecture

### Input Validation
```
File Upload → Extension Check → Size Limit → Type Verification
```

### Output Sanitization
```
User Content → HTML Escape → Safe Attributes → XSS Prevention
```

### Image Security
```
URL → Validation → Size Check → Download → Verification → Processing
```

## Performance Considerations

### Optimization Strategies

1. **Image Processing:**
   - Lazy loading of images
   - Compression to reduce file size
   - Deduplication to avoid redundancy

2. **Memory Management:**
   - In-memory ZIP creation
   - Stream-based file handling
   - Efficient data structures

3. **Batch Processing:**
   - Parallel file reading
   - Sequential conversion (prevents memory spikes)

### Scalability

**Current Limitations:**
- Single-threaded processing
- Memory-bound for large files
- No caching between sessions

**Future Enhancements:**
- Multi-threaded conversion
- Redis caching for large batches
- Chunked file processing

## Technology Stack

### Core Technologies
- **Python 3.11**: Language
- **Streamlit 1.x**: Web framework
- **BeautifulSoup4**: HTML/XML parsing
- **Pillow**: Image processing

### Data Processing
- **python-docx**: DOCX parsing
- **pandas**: CSV processing
- **PyYAML**: YAML generation

### Content Generation
- **Python-Markdown**: HTML generation
- **markdown extensions**: Tables, code, TOC

## Deployment Architecture

### Replit Deployment
```
┌────────────────────────────────────┐
│         Replit Container           │
│  ┌──────────────────────────────┐  │
│  │   Streamlit Server (5000)    │  │
│  └──────────────────────────────┘  │
│  ┌──────────────────────────────┐  │
│  │   Python Application         │  │
│  └──────────────────────────────┘  │
│  ┌──────────────────────────────┐  │
│  │   File System (temp)         │  │
│  └──────────────────────────────┘  │
└────────────────────────────────────┘
```

### Docker Deployment
```
┌────────────────────────────────────┐
│        Docker Container            │
│  ┌──────────────────────────────┐  │
│  │   Streamlit (Port 5000)      │  │
│  ├──────────────────────────────┤  │
│  │   Python 3.11 Runtime        │  │
│  ├──────────────────────────────┤  │
│  │   Application Code           │  │
│  ├──────────────────────────────┤  │
│  │   Dependencies               │  │
│  └──────────────────────────────┘  │
└────────────────────────────────────┘
```

## Configuration Management

### Streamlit Configuration
File: `.streamlit/config.toml`
```toml
[server]
headless = true
address = "0.0.0.0"
port = 5000
```

### Application Configuration
- Hard-coded constants in modules
- No external config files
- Environment-agnostic

## Error Handling

### Strategy
```
Try-Catch at each layer:
1. File upload validation
2. Conversion error handling
3. Image processing failures
4. HTML generation errors
5. User-friendly error messages
```

### Logging
- Streamlit built-in error display
- No external logging service
- Console output for debugging

## Testing Strategy

### Manual Testing
- File conversion validation
- UI/UX verification
- Cross-browser testing
- SEO validation accuracy

### Future Automated Testing
- Unit tests for converters
- Integration tests for pipeline
- End-to-end UI tests
- Performance benchmarks

## Extension Points

### Adding New Features

1. **New File Format:**
   - Create converter class
   - Implement convert() method
   - Register in CONVERTERS dict

2. **New HTML Template:**
   - Add template to templates/
   - Register in TemplateManager
   - Add CSS styling

3. **New SEO Rule:**
   - Add validation method
   - Update scoring algorithm
   - Add enhancement logic

## Dependencies

### Production Dependencies
```
streamlit>=1.28.0
python-docx>=1.1.0
pandas>=2.1.0
beautifulsoup4>=4.12.0
lxml>=5.0.0
Pillow>=10.0.0
PyYAML>=6.0
markdown>=3.5.0
requests>=2.31.0
```

### Dependency Graph
```
app.py
├── streamlit
├── converters/
│   ├── python-docx
│   ├── pandas
│   ├── beautifulsoup4
│   └── lxml
├── utils/
│   ├── markdown
│   ├── Pillow
│   ├── PyYAML
│   └── requests
```

## Version History

- **v1.0.0** (2025-10-08): Initial architecture
  - Plugin-based converter system
  - Utility layer separation
  - SEO validation and enhancement
  - Static site generation

---

**Last Updated**: October 8, 2025  
**Version**: 1.0.0
