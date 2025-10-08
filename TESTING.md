# Testing Documentation

Complete guide to testing the File Converter with SEO Optimization application.

## Table of Contents
1. [Testing Strategy](#testing-strategy)
2. [Test Suite Setup](#test-suite-setup)
3. [Unit Tests](#unit-tests)
4. [Integration Tests](#integration-tests)
5. [End-to-End Tests](#end-to-end-tests)
6. [Manual Testing](#manual-testing)
7. [Performance Tests](#performance-tests)
8. [Security Tests](#security-tests)
9. [CI/CD Integration](#cicd-integration)
10. [Test Coverage](#test-coverage)

---

## Testing Strategy

### Testing Pyramid

```
        /\
       /  \        E2E Tests (10%)
      /----\       - Full user workflows
     /      \      - Browser automation
    /--------\     Integration Tests (30%)
   /          \    - Component interaction
  /------------\   - API testing
 /______________\  Unit Tests (60%)
                   - Individual functions
                   - Converters
                   - Utilities
```

### Testing Philosophy

1. **Test Early, Test Often** - Catch bugs before they reach production
2. **Automated Where Possible** - Reduce manual testing burden
3. **Meaningful Tests** - Focus on behavior, not implementation
4. **Fast Feedback** - Tests should run quickly
5. **Maintainable** - Keep tests simple and clear

### Test Categories

| Type | Purpose | Frequency | Tool |
|------|---------|-----------|------|
| Unit | Test individual functions | On every commit | pytest |
| Integration | Test component interaction | Daily | pytest |
| E2E | Test user workflows | Before release | Playwright |
| Manual | Exploratory testing | Weekly | Human |
| Performance | Check speed/resources | Monthly | locust/pytest-benchmark |
| Security | Find vulnerabilities | Before release | bandit/safety |

---

## Test Suite Setup

### Prerequisites

```bash
# Install Python 3.11+
python --version

# Clone repository
git clone https://github.com/poolboy17/file-converter-seo-app.git
cd file-converter-seo-app
```

### Install Testing Dependencies

Create `requirements-dev.txt`:
```txt
# Core dependencies
-r requirements.txt

# Testing frameworks
pytest>=7.4.0
pytest-cov>=4.1.0
pytest-mock>=3.11.0
pytest-asyncio>=0.21.0
pytest-benchmark>=4.0.0

# End-to-End testing
playwright>=1.40.0
selenium>=4.15.0

# Performance testing
locust>=2.16.0

# Security testing
bandit>=1.7.5
safety>=2.3.5

# Code quality
pylint>=3.0.0
black>=23.10.0
mypy>=1.6.0

# Coverage reporting
coverage[toml]>=7.3.0
```

Install:
```bash
pip install -r requirements-dev.txt

# Install Playwright browsers
playwright install
```

### Configure pytest

Create `pytest.ini`:
```ini
[pytest]
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
addopts = 
    -v
    --strict-markers
    --cov=.
    --cov-report=html
    --cov-report=term-missing
    --cov-branch
markers =
    unit: Unit tests
    integration: Integration tests
    e2e: End-to-end tests
    slow: Slow running tests
    security: Security tests
```

### Directory Structure

```
tests/
├── __init__.py
├── conftest.py              # Shared fixtures
├── unit/                    # Unit tests
│   ├── __init__.py
│   ├── test_converters.py
│   ├── test_html_generator.py
│   ├── test_seo_validator.py
│   ├── test_seo_enhancer.py
│   └── test_image_handler.py
├── integration/             # Integration tests
│   ├── __init__.py
│   ├── test_conversion_pipeline.py
│   ├── test_static_site_gen.py
│   └── test_file_packaging.py
├── e2e/                     # End-to-end tests
│   ├── __init__.py
│   ├── test_user_workflows.py
│   └── test_seo_workflow.py
├── performance/             # Performance tests
│   ├── __init__.py
│   └── test_benchmarks.py
├── security/                # Security tests
│   ├── __init__.py
│   └── test_security.py
└── fixtures/                # Test data
    ├── sample.docx
    ├── sample.csv
    ├── sample.txt
    └── sample.wxr
```

---

## Unit Tests

### Purpose
Test individual functions and classes in isolation.

### Example: Test DOCX Converter

Create `tests/unit/test_converters.py`:

```python
"""Unit tests for file converters."""
import pytest
from io import BytesIO
from converters.docx_converter import DocxConverter
from converters.csv_converter import CsvConverter


class TestDocxConverter:
    """Test DOCX converter functionality."""
    
    @pytest.fixture
    def sample_docx(self):
        """Provide sample DOCX file."""
        # Load from fixtures
        with open('tests/fixtures/sample.docx', 'rb') as f:
            return BytesIO(f.read())
    
    def test_docx_converter_initialization(self, sample_docx):
        """Test converter initializes correctly."""
        converter = DocxConverter(sample_docx)
        assert converter.file is not None
        assert converter.content == ""
    
    def test_docx_to_markdown_conversion(self, sample_docx):
        """Test DOCX converts to valid Markdown."""
        converter = DocxConverter(sample_docx)
        result = converter.convert()
        
        assert result is not None
        assert isinstance(result, str)
        assert len(result) > 0
    
    def test_docx_preserves_headings(self, sample_docx):
        """Test heading structure is preserved."""
        converter = DocxConverter(sample_docx)
        result = converter.convert()
        
        # Check for markdown heading syntax
        assert '# ' in result or '## ' in result
    
    def test_docx_handles_lists(self, sample_docx):
        """Test lists are converted correctly."""
        converter = DocxConverter(sample_docx)
        result = converter.convert()
        
        # Check for list markers
        assert '- ' in result or '* ' in result or any(
            line.strip().startswith(('1.', '2.', '3.'))
            for line in result.split('\n')
        )
    
    def test_docx_empty_file_handling(self):
        """Test handling of empty DOCX file."""
        # Create minimal DOCX structure
        empty_docx = BytesIO(b'PK\x03\x04...')  # Simplified
        
        converter = DocxConverter(empty_docx)
        result = converter.convert()
        
        # Should not crash, might return empty or minimal content
        assert isinstance(result, str)
    
    def test_docx_invalid_file_raises_error(self):
        """Test invalid file raises appropriate error."""
        invalid_file = BytesIO(b'Not a DOCX file')
        
        with pytest.raises(Exception):
            converter = DocxConverter(invalid_file)
            converter.convert()


class TestCsvConverter:
    """Test CSV converter functionality."""
    
    def test_csv_to_markdown_table(self):
        """Test CSV converts to Markdown table."""
        csv_content = BytesIO(b"Name,Age,City\nJohn,30,NYC\nJane,25,LA")
        
        converter = CsvConverter(csv_content)
        result = converter.convert()
        
        # Check for table format
        assert '|' in result
        assert 'Name' in result
        assert 'Age' in result
        assert 'John' in result
    
    def test_csv_handles_quotes(self):
        """Test CSV with quoted values."""
        csv_content = BytesIO(b'Name,Quote\nJohn,"Hello, World"')
        
        converter = CsvConverter(csv_content)
        result = converter.convert()
        
        assert 'Hello, World' in result
    
    def test_csv_encoding_detection(self):
        """Test automatic encoding detection."""
        # UTF-8 content with special characters
        csv_content = BytesIO('Name,City\nJosé,São Paulo'.encode('utf-8'))
        
        converter = CsvConverter(csv_content)
        result = converter.convert()
        
        assert 'José' in result
        assert 'São Paulo' in result
```

### Example: Test SEO Validator

Create `tests/unit/test_seo_validator.py`:

```python
"""Unit tests for SEO validator."""
import pytest
from utils.seo_validator import SEOValidator, get_seo_grade


class TestSEOValidator:
    """Test SEO validation functionality."""
    
    @pytest.fixture
    def validator(self):
        """Provide SEO validator instance."""
        return SEOValidator()
    
    def test_title_tag_validation_optimal(self, validator):
        """Test optimal title length passes."""
        html = '<html><head><title>This is an optimal title length</title></head></html>'
        
        result = validator.validate(html)
        
        assert result['score'] > 0
        assert not any('title' in issue.lower() for issue in result['issues'])
    
    def test_title_tag_validation_too_short(self, validator):
        """Test short title fails."""
        html = '<html><head><title>Short</title></head></html>'
        
        result = validator.validate(html)
        
        assert any('title' in warning.lower() for warning in result['warnings'])
    
    def test_title_tag_missing(self, validator):
        """Test missing title is flagged."""
        html = '<html><head></head><body>Content</body></html>'
        
        result = validator.validate(html)
        
        assert any('title' in issue.lower() for issue in result['issues'])
    
    def test_meta_description_validation(self, validator):
        """Test meta description validation."""
        html = '''
        <html>
        <head>
            <meta name="description" content="This is a well-written meta description that provides a good summary of the page content and is within optimal length.">
        </head>
        </html>
        '''
        
        result = validator.validate(html)
        
        assert result['score'] > 0
    
    def test_heading_structure(self, validator):
        """Test heading hierarchy validation."""
        html = '''
        <html><body>
            <h1>Main Title</h1>
            <h2>Section</h2>
            <h3>Subsection</h3>
        </body></html>
        '''
        
        result = validator.validate(html)
        
        # Should have success for proper structure
        assert any('heading' in success.lower() for success in result['successes'])
    
    def test_multiple_h1_tags(self, validator):
        """Test multiple H1 tags flagged."""
        html = '''
        <html><body>
            <h1>First Title</h1>
            <h1>Second Title</h1>
        </body></html>
        '''
        
        result = validator.validate(html)
        
        assert any('h1' in warning.lower() for warning in result['warnings'])
    
    def test_image_alt_text(self, validator):
        """Test image alt text validation."""
        html = '''
        <html><body>
            <img src="image1.jpg" alt="Descriptive alt text">
            <img src="image2.jpg">
        </body></html>
        '''
        
        result = validator.validate(html)
        
        # Should warn about missing alt
        assert any('alt' in warning.lower() for warning in result['warnings'])
    
    def test_seo_grade_calculation(self):
        """Test grade assignment."""
        assert get_seo_grade(95) == 'A'
        assert get_seo_grade(85) == 'B'
        assert get_seo_grade(75) == 'C'
        assert get_seo_grade(65) == 'D'
        assert get_seo_grade(50) == 'F'
    
    def test_open_graph_tags(self, validator):
        """Test Open Graph validation."""
        html = '''
        <html><head>
            <meta property="og:title" content="Page Title">
            <meta property="og:description" content="Description">
            <meta property="og:type" content="website">
        </head></html>
        '''
        
        result = validator.validate(html)
        
        # Should have success for OG tags
        assert any('open graph' in success.lower() for success in result['successes'])


class TestSEOScoring:
    """Test SEO scoring algorithm."""
    
    def test_perfect_score_structure(self):
        """Test HTML that should score 100."""
        perfect_html = '''
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Perfect SEO Page Title Example</title>
            <meta name="description" content="This is a perfectly optimized meta description that provides comprehensive information about the page content.">
            <meta name="keywords" content="test, seo, optimization">
            <meta property="og:title" content="Perfect SEO Page">
            <meta property="og:description" content="Description for social sharing">
            <meta property="og:type" content="website">
            <link rel="canonical" href="https://example.com">
        </head>
        <body>
            <header>
                <h1>Main Page Heading</h1>
            </header>
            <main>
                <article>
                    <h2>Section One</h2>
                    <p>Content paragraph with at least 300 words of meaningful text goes here...</p>
                    <p>More content to meet word count requirements...</p>
                    <img src="image.jpg" alt="Descriptive alternative text">
                    <a href="https://example.com">External link</a>
                    <a href="/internal">Internal link</a>
                </article>
            </main>
            <footer>
                <p>Footer content</p>
            </footer>
            <script type="application/ld+json">
            {
                "@context": "https://schema.org",
                "@type": "Article"
            }
            </script>
        </body>
        </html>
        '''
        
        validator = SEOValidator()
        result = validator.validate(perfect_html)
        
        # Should score very high (90+)
        assert result['score'] >= 90
        assert result['grade'] in ['A', 'B']
```

### Running Unit Tests

```bash
# Run all unit tests
pytest tests/unit/

# Run specific test file
pytest tests/unit/test_converters.py

# Run specific test
pytest tests/unit/test_converters.py::TestDocxConverter::test_docx_to_markdown_conversion

# Run with coverage
pytest tests/unit/ --cov=converters --cov=utils

# Run tests matching pattern
pytest -k "docx"

# Verbose output
pytest tests/unit/ -v

# Stop on first failure
pytest tests/unit/ -x
```

---

## Integration Tests

### Purpose
Test how components work together.

### Example: Test Conversion Pipeline

Create `tests/integration/test_conversion_pipeline.py`:

```python
"""Integration tests for conversion pipeline."""
import pytest
from io import BytesIO
from converters.docx_converter import DocxConverter
from utils.html_generator import HtmlGenerator
from utils.seo_validator import SEOValidator
from utils.image_handler import ImageHandler


class TestConversionPipeline:
    """Test end-to-end conversion pipeline."""
    
    @pytest.fixture
    def image_handler(self):
        """Provide image handler instance."""
        return ImageHandler()
    
    def test_docx_to_html_with_seo(self, image_handler):
        """Test complete DOCX to SEO-optimized HTML."""
        # Step 1: Convert DOCX to Markdown
        with open('tests/fixtures/sample.docx', 'rb') as f:
            converter = DocxConverter(f)
            markdown = converter.convert()
        
        assert markdown is not None
        
        # Step 2: Generate HTML
        html_gen = HtmlGenerator(
            template='modern',
            color_scheme='blue',
            enable_seo=True
        )
        html = html_gen.generate(markdown, 'test.docx')
        
        assert html is not None
        assert '<html' in html
        
        # Step 3: Validate SEO
        validator = SEOValidator()
        report = validator.validate(html)
        
        assert report['score'] > 0
        assert 'grade' in report
    
    def test_csv_to_static_site(self):
        """Test CSV to static site generation."""
        # Convert CSV
        csv_data = BytesIO(b"Name,Value\nTest,123")
        from converters.csv_converter import CsvConverter
        
        converter = CsvConverter(csv_data)
        markdown = converter.convert()
        
        # Generate HTML
        html_gen = HtmlGenerator()
        html = html_gen.generate(markdown, 'data.csv')
        
        # Verify table in HTML
        assert '<table' in html or '|' in html
    
    def test_image_extraction_and_optimization(self):
        """Test image extraction and optimization flow."""
        handler = ImageHandler()
        
        # Simulate image data
        import base64
        from PIL import Image
        
        # Create test image
        img = Image.new('RGB', (2000, 2000), color='red')
        img_bytes = BytesIO()
        img.save(img_bytes, format='JPEG')
        img_data = img_bytes.getvalue()
        
        # Store and optimize
        path = handler.store_image(img_data, extension='jpg')
        
        # Verify optimization
        optimized = handler.images[path]
        assert len(optimized['data']) < len(img_data)  # Should be smaller


class TestStaticSiteGeneration:
    """Test static site generation."""
    
    def test_multiple_files_to_static_site(self):
        """Test generating static site from multiple files."""
        from utils.static_site_generator import StaticSiteGenerator
        
        # Prepare multiple converted files
        files = [
            {
                'original_name': 'doc1.docx',
                'markdown_content': '# Document 1\n\nContent here.',
                'html_content': '<h1>Document 1</h1><p>Content here.</p>',
                'file_type': '.docx'
            },
            {
                'original_name': 'doc2.txt',
                'markdown_content': '# Document 2\n\nMore content.',
                'html_content': '<h1>Document 2</h1><p>More content.</p>',
                'file_type': '.txt'
            }
        ]
        
        # Generate site
        generator = StaticSiteGenerator()
        site_zip = generator.generate_site(files, "Test Site", None)
        
        # Verify ZIP created
        assert site_zip is not None
        assert site_zip.tell() > 0  # Has content
```

### Running Integration Tests

```bash
# Run all integration tests
pytest tests/integration/

# Run with markers
pytest -m integration

# Slow tests (optional)
pytest -m "integration and not slow"
```

---

## End-to-End Tests

### Purpose
Test complete user workflows through the UI.

### Example: E2E Test with Playwright

Create `tests/e2e/test_user_workflows.py`:

```python
"""End-to-end tests using Playwright."""
import pytest
from playwright.sync_api import Page, expect


class TestFileConversionWorkflow:
    """Test complete file conversion workflows."""
    
    def test_upload_and_convert_docx(self, page: Page):
        """Test uploading and converting DOCX file."""
        # Navigate to app
        page.goto("http://localhost:5000")
        
        # Upload file
        page.set_input_files(
            'input[type="file"]',
            'tests/fixtures/sample.docx'
        )
        
        # Wait for upload confirmation
        expect(page.locator('text=sample.docx')).to_be_visible()
        
        # Select output format
        page.select_option('select[label*="Output"]', 'HTML')
        
        # Convert
        page.click('button:has-text("Convert All Files")')
        
        # Wait for conversion
        expect(page.locator('text=Conversion completed')).to_be_visible(
            timeout=30000
        )
        
        # Verify download available
        expect(page.locator('button:has-text("Download")')).to_be_visible()
    
    def test_seo_report_generation(self, page: Page):
        """Test SEO report workflow."""
        page.goto("http://localhost:5000")
        
        # Enable SEO
        seo_checkbox = page.locator('input[type="checkbox"]', has_text="SEO")
        if not seo_checkbox.is_checked():
            seo_checkbox.check()
        
        # Upload and convert
        page.set_input_files('input[type="file"]', 'tests/fixtures/sample.docx')
        page.select_option('select', 'HTML')
        page.click('button:has-text("Convert")')
        
        # Navigate to SEO Report tab
        page.click('text=SEO Report')
        
        # Verify report elements
        expect(page.locator('text=SEO Score')).to_be_visible()
        expect(page.locator('text=Grade')).to_be_visible()
        
        # Check for score display
        expect(page.locator('text=/\\d+\\/100/')).to_be_visible()
    
    def test_batch_conversion(self, page: Page):
        """Test converting multiple files."""
        page.goto("http://localhost:5000")
        
        # Upload multiple files
        page.set_input_files('input[type="file"]', [
            'tests/fixtures/sample.docx',
            'tests/fixtures/sample.csv',
            'tests/fixtures/sample.txt'
        ])
        
        # Verify all files listed
        expect(page.locator('text=sample.docx')).to_be_visible()
        expect(page.locator('text=sample.csv')).to_be_visible()
        expect(page.locator('text=sample.txt')).to_be_visible()
        
        # Convert all
        page.click('button:has-text("Convert All")')
        
        # Wait for completion
        expect(page.locator('text=3')).to_be_visible(timeout=60000)


@pytest.fixture(scope="session")
def browser_context_args(browser_context_args):
    """Configure browser context."""
    return {
        **browser_context_args,
        "viewport": {
            "width": 1920,
            "height": 1080,
        },
    }
```

### Running E2E Tests

```bash
# Start application first
streamlit run app.py --server.port 5000 &

# Run E2E tests
pytest tests/e2e/

# With headed browser (see what's happening)
pytest tests/e2e/ --headed

# With slowmo (slower for debugging)
pytest tests/e2e/ --slowmo 1000

# Specific browser
pytest tests/e2e/ --browser chromium
pytest tests/e2e/ --browser firefox
```

---

## Manual Testing

### Manual Test Checklist

#### File Upload
- [ ] Upload single DOCX file
- [ ] Upload multiple files (mixed types)
- [ ] Upload file >50MB (should show error)
- [ ] Upload unsupported format (should reject)
- [ ] Drag and drop file

#### Conversion
- [ ] Convert DOCX to Markdown
- [ ] Convert DOCX to HTML
- [ ] Convert CSV to Markdown table
- [ ] Convert TXT with special encoding
- [ ] Convert WXR (WordPress export)
- [ ] Batch convert 10+ files

#### HTML Generation
- [ ] Try each template (Modern, Minimal, Classic, Dark)
- [ ] Try each color scheme
- [ ] Try each font option
- [ ] Verify styling applies correctly

#### SEO Features
- [ ] Enable/disable SEO toggle
- [ ] Review SEO report for converted file
- [ ] Check score calculation
- [ ] Verify grade display
- [ ] Review issues, warnings, successes
- [ ] Read recommendations

#### Image Handling
- [ ] Convert DOCX with embedded images
- [ ] Verify images extracted
- [ ] Check image optimization
- [ ] Convert WXR, download remote images
- [ ] Verify images in output

#### Static Site
- [ ] Generate static site
- [ ] Download and extract
- [ ] Open index.html
- [ ] Navigate to pages
- [ ] Verify styling consistent

#### Download
- [ ] Download individual Markdown file
- [ ] Download individual HTML file
- [ ] Create ZIP archive
- [ ] Verify ZIP contains all files

#### Browser Compatibility
- [ ] Test in Chrome
- [ ] Test in Firefox
- [ ] Test in Safari
- [ ] Test in Edge
- [ ] Test on mobile device

---

## Performance Tests

### Benchmark Tests

Create `tests/performance/test_benchmarks.py`:

```python
"""Performance benchmark tests."""
import pytest
from io import BytesIO


class TestConversionPerformance:
    """Benchmark conversion performance."""
    
    def test_small_docx_conversion_speed(self, benchmark):
        """Benchmark small DOCX conversion."""
        from converters.docx_converter import DocxConverter
        
        with open('tests/fixtures/small.docx', 'rb') as f:
            data = f.read()
        
        def convert():
            converter = DocxConverter(BytesIO(data))
            return converter.convert()
        
        result = benchmark(convert)
        assert result is not None
        # Should complete in <1 second
    
    def test_large_docx_conversion_speed(self, benchmark):
        """Benchmark large DOCX conversion."""
        from converters.docx_converter import DocxConverter
        
        with open('tests/fixtures/large.docx', 'rb') as f:
            data = f.read()
        
        def convert():
            converter = DocxConverter(BytesIO(data))
            return converter.convert()
        
        result = benchmark(convert)
        # Should complete in <10 seconds
    
    def test_seo_validation_speed(self, benchmark):
        """Benchmark SEO validation."""
        from utils.seo_validator import SEOValidator
        
        html = '''<html><head><title>Test</title></head><body>
        <h1>Title</h1><p>Content</p></body></html>'''
        
        def validate():
            validator = SEOValidator()
            return validator.validate(html)
        
        result = benchmark(validate)
        assert result['score'] >= 0
        # Should complete in <100ms


# Run with: pytest tests/performance/ --benchmark-only
```

---

## Security Tests

### Security Audit

Create `tests/security/test_security.py`:

```python
"""Security tests."""
import pytest


class TestInputValidation:
    """Test input validation and sanitization."""
    
    def test_file_type_validation(self):
        """Test file type is validated."""
        from app import CONVERTERS
        
        # Valid extensions
        assert '.docx' in CONVERTERS
        assert '.csv' in CONVERTERS
        
        # Invalid should not be present
        assert '.exe' not in CONVERTERS
        assert '.sh' not in CONVERTERS
    
    def test_html_sanitization(self):
        """Test HTML output is sanitized."""
        from utils.html_generator import HtmlGenerator
        
        malicious_markdown = '''
        # Title
        <script>alert('XSS')</script>
        [Click](javascript:alert('XSS'))
        '''
        
        gen = HtmlGenerator()
        html = gen.generate(malicious_markdown, 'test.md')
        
        # Script tags should be escaped or removed
        assert '<script>' not in html.lower()
        assert 'javascript:' not in html.lower()
    
    def test_path_traversal_prevention(self):
        """Test path traversal is prevented."""
        # Simulate file upload with malicious name
        malicious_names = [
            '../../../etc/passwd',
            '..\\..\\..\\windows\\system32',
            'normal_file.docx'
        ]
        
        from pathlib import Path
        
        for name in malicious_names:
            # Should strip path components
            safe_name = Path(name).name
            assert '/' not in safe_name
            assert '\\' not in safe_name
```

### Run Security Scans

```bash
# Scan for common security issues
bandit -r . -f json -o security-report.json

# Check for known vulnerabilities
safety check

# Or with pip audit
pip audit
```

---

## CI/CD Integration

### GitHub Actions Workflow

Create `.github/workflows/test.yml`:

```yaml
name: Test Suite

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest
    
    strategy:
      matrix:
        python-version: ['3.11', '3.12']
    
    steps:
    - uses: actions/checkout@v4
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: ${{ matrix.python-version }}
    
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
        pip install -r requirements-dev.txt
    
    - name: Run unit tests
      run: |
        pytest tests/unit/ -v --cov=. --cov-report=xml
    
    - name: Run integration tests
      run: |
        pytest tests/integration/ -v
    
    - name: Upload coverage
      uses: codecov/codecov-action@v3
      with:
        file: ./coverage.xml
    
    - name: Security scan
      run: |
        bandit -r . -ll
        safety check
    
    - name: Lint check
      run: |
        pylint converters/ utils/ --fail-under=8.0
```

---

## Test Coverage

### Generate Coverage Report

```bash
# Run tests with coverage
pytest --cov=. --cov-report=html --cov-report=term

# Open HTML report
open htmlcov/index.html
```

### Coverage Goals

| Component | Target Coverage |
|-----------|----------------|
| Converters | 90%+ |
| Utils | 85%+ |
| Overall | 80%+ |

### View Coverage

```bash
# Terminal report
pytest --cov=. --cov-report=term-missing

# HTML report
pytest --cov=. --cov-report=html
```

---

## Test Execution Guide

### Quick Test

```bash
# Run fastest tests only
pytest -m "unit and not slow"
```

### Full Test Suite

```bash
# Run everything
pytest tests/
```

### Pre-Commit Tests

```bash
# Run before committing
pytest tests/unit/ tests/integration/ -x
```

### Pre-Release Tests

```bash
# Complete test suite
pytest tests/ --cov=. --cov-report=html
bandit -r .
safety check
```

---

## Writing Good Tests

### Test Naming Convention

```python
def test_[function]_[scenario]_[expected_result]():
    """Test that [function] [expected result] when [scenario]."""
    pass

# Examples:
def test_docx_converter_returns_markdown_when_valid_file():
    pass

def test_seo_validator_flags_error_when_title_missing():
    pass
```

### Test Structure (AAA Pattern)

```python
def test_example():
    # Arrange - Set up test data
    input_data = "test"
    expected = "expected result"
    
    # Act - Execute the code being tested
    result = function_under_test(input_data)
    
    # Assert - Verify the result
    assert result == expected
```

### Best Practices

1. **One assertion per test** (when possible)
2. **Test behavior, not implementation**
3. **Use descriptive names**
4. **Keep tests independent**
5. **Use fixtures for common setup**
6. **Mock external dependencies**
7. **Test edge cases and errors**

---

**Last Updated:** October 8, 2025  
**Version:** 1.0.0
