# Development Workflows

Complete workflows for developers contributing to or customizing the File Converter application.

## Table of Contents
1. [Initial Setup](#initial-setup)
2. [Adding New File Format Converter](#adding-new-file-format-converter)
3. [Creating New HTML Template](#creating-new-html-template)
4. [Adding SEO Validation Rule](#adding-seo-validation-rule)
5. [Bug Fix Workflow](#bug-fix-workflow)
6. [Feature Development Workflow](#feature-development-workflow)
7. [Code Review Process](#code-review-process)

---

## Initial Setup

### Workflow: Set Up Development Environment

**Prerequisites:**
- Python 3.11 or higher installed
- Git installed
- GitHub account
- Text editor or IDE

**Steps:**

1. **Fork Repository**
   ```bash
   # Go to GitHub
   https://github.com/poolboy17/file-converter-seo-app
   # Click "Fork" button
   ```

2. **Clone Your Fork**
   ```bash
   git clone https://github.com/YOUR_USERNAME/file-converter-seo-app.git
   cd file-converter-seo-app
   ```

3. **Add Upstream Remote**
   ```bash
   git remote add upstream https://github.com/poolboy17/file-converter-seo-app.git
   git remote -v  # Verify remotes
   ```

4. **Create Virtual Environment**
   ```bash
   python -m venv venv
   
   # Activate (Windows)
   venv\Scripts\activate
   
   # Activate (Mac/Linux)
   source venv/bin/activate
   ```

5. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   # Or if using uv
   uv sync
   ```

6. **Verify Installation**
   ```bash
   streamlit run app.py --server.port 5000
   # Open http://localhost:5000
   # Test basic conversion
   ```

7. **Set Up IDE**
   - Open project in your IDE
   - Configure Python interpreter to use venv
   - Install recommended extensions (Python, Pylint)
   - Review existing code structure

**Expected Outcome:** 
- Working development environment
- Application runs successfully
- Ready to make changes

**Time Estimate:** 10-15 minutes

---

## Adding New File Format Converter

### Workflow: Implement PDF Converter

**Use Case:** Add support for converting PDF files to Markdown.

**Prerequisites:**
- Development environment set up
- Understanding of Python classes
- PDF parsing library chosen (e.g., PyPDF2, pdfplumber)

**Steps:**

1. **Create Feature Branch**
   ```bash
   git checkout main
   git pull upstream main
   git checkout -b feature/pdf-converter
   ```

2. **Install Required Library**
   ```bash
   pip install pdfplumber
   # or add to pyproject.toml
   ```

3. **Create Converter Class**
   
   Create `converters/pdf_converter.py`:
   ```python
   """PDF to Markdown converter."""
   import pdfplumber
   from io import BytesIO
   
   class PdfConverter:
       """Converter for PDF files."""
       
       def __init__(self, file):
           """Initialize with uploaded file."""
           self.file = file
           self.content = ""
       
       def convert(self):
           """Convert PDF to Markdown.
           
           Returns:
               str: Markdown formatted content
           """
           try:
               # Read PDF
               pdf_bytes = BytesIO(self.file.read())
               
               with pdfplumber.open(pdf_bytes) as pdf:
                   for page_num, page in enumerate(pdf.pages, 1):
                       # Extract text
                       text = page.extract_text()
                       
                       if text:
                           # Add page marker
                           self.content += f"\n## Page {page_num}\n\n"
                           self.content += text + "\n\n"
                       
                       # Extract tables
                       tables = page.extract_tables()
                       for table in tables:
                           self.content += self._table_to_markdown(table)
                           self.content += "\n\n"
               
               return self.content
               
           except Exception as e:
               raise Exception(f"PDF conversion failed: {str(e)}")
       
       def _table_to_markdown(self, table):
           """Convert table to Markdown format."""
           if not table:
               return ""
           
           markdown = ""
           # Header row
           markdown += "| " + " | ".join(str(cell) for cell in table[0]) + " |\n"
           # Separator
           markdown += "| " + " | ".join(["---"] * len(table[0])) + " |\n"
           # Data rows
           for row in table[1:]:
               markdown += "| " + " | ".join(str(cell) for cell in row) + " |\n"
           
           return markdown
   ```

4. **Register Converter**
   
   Edit `app.py`:
   ```python
   from converters.pdf_converter import PdfConverter
   
   # Add to CONVERTERS dictionary
   CONVERTERS = {
       '.docx': DocxConverter,
       '.csv': CsvConverter,
       '.txt': TxtConverter,
       '.wxr': WxrConverter,
       '.pdf': PdfConverter,  # NEW
   }
   ```

5. **Update File Uploader**
   
   In `app.py`, update accepted file types:
   ```python
   uploaded_files = st.file_uploader(
       "Choose files to convert",
       type=['docx', 'csv', 'txt', 'wxr', 'pdf'],  # Added 'pdf'
       accept_multiple_files=True
   )
   ```

6. **Test Locally**
   ```bash
   streamlit run app.py --server.port 5000
   ```
   - Upload sample PDF
   - Verify conversion works
   - Check tables convert correctly
   - Test with different PDF types

7. **Add Documentation**
   
   Update `README.md`:
   ```markdown
   ### Supported Formats
   - DOCX (Microsoft Word)
   - CSV (Comma-separated values)
   - TXT (Plain text)
   - WXR (WordPress export)
   - PDF (Portable Document Format) ← NEW
   ```

8. **Update Config**
   
   Edit `config.yaml`:
   ```yaml
   formats:
     supported_extensions:
       - docx
       - csv
       - txt
       - wxr
       - pdf  # NEW
   ```

9. **Commit Changes**
   ```bash
   git add converters/pdf_converter.py
   git add app.py
   git add README.md
   git add config.yaml
   git commit -m "feat: add PDF converter support
   
   - Implement PdfConverter class
   - Extract text and tables from PDF
   - Register .pdf extension
   - Update documentation"
   ```

10. **Push and Create PR**
    ```bash
    git push origin feature/pdf-converter
    # Go to GitHub and create Pull Request
    ```

11. **Respond to Review**
    - Address reviewer comments
    - Make requested changes
    - Push updates to same branch
    - Request re-review

**Expected Outcome:**
- PDF files can be uploaded
- PDFs convert to Markdown
- Tables preserved
- Feature documented

**Testing Checklist:**
- [ ] Simple PDF converts correctly
- [ ] PDF with tables converts correctly
- [ ] Multi-page PDF handles all pages
- [ ] Image-heavy PDF handles gracefully
- [ ] Encrypted PDF shows error message
- [ ] Empty PDF handles without crashing

**Time Estimate:** 2-4 hours

---

## Creating New HTML Template

### Workflow: Add "Professional" Template Style

**Use Case:** Create a new template design for professional documents.

**Steps:**

1. **Create Feature Branch**
   ```bash
   git checkout -b feature/professional-template
   ```

2. **Design Template CSS**
   
   In `utils/template_manager.py`, add new style:
   ```python
   def _get_professional_style(self, primary_color):
       """Generate professional template CSS."""
       return f"""
       /* Professional Template */
       body {{
           font-family: 'Georgia', serif;
           line-height: 1.8;
           max-width: 800px;
           margin: 0 auto;
           padding: 60px 40px;
           background: #f9f9f9;
           color: #2c2c2c;
       }}
       
       header {{
           border-bottom: 3px solid {primary_color};
           padding-bottom: 30px;
           margin-bottom: 50px;
       }}
       
       h1 {{
           font-size: 2.5em;
           font-weight: bold;
           color: #1a1a1a;
           margin-bottom: 10px;
           letter-spacing: -0.5px;
       }}
       
       h2 {{
           font-size: 1.8em;
           color: {primary_color};
           margin-top: 40px;
           margin-bottom: 20px;
           font-weight: 600;
       }}
       
       article {{
           background: white;
           padding: 50px;
           box-shadow: 0 2px 8px rgba(0,0,0,0.1);
           border-radius: 4px;
       }}
       
       p {{
           margin-bottom: 20px;
           text-align: justify;
       }}
       
       blockquote {{
           border-left: 4px solid {primary_color};
           padding-left: 30px;
           margin: 30px 0;
           font-style: italic;
           color: #555;
       }}
       
       code {{
           background: #f4f4f4;
           padding: 2px 6px;
           border-radius: 3px;
           font-family: 'Courier New', monospace;
           font-size: 0.9em;
       }}
       
       pre {{
           background: #282c34;
           color: #abb2bf;
           padding: 20px;
           border-radius: 4px;
           overflow-x: auto;
       }}
       
       footer {{
           margin-top: 60px;
           padding-top: 30px;
           border-top: 2px solid #e0e0e0;
           text-align: center;
           color: #666;
           font-size: 0.9em;
       }}
       """
   ```

3. **Register Template**
   
   Update `generate_css()` method:
   ```python
   def generate_css(self):
       """Generate CSS based on selected template."""
       templates = {
           'modern': self._get_modern_style,
           'minimal': self._get_minimal_style,
           'classic': self._get_classic_style,
           'dark': self._get_dark_style,
           'professional': self._get_professional_style,  # NEW
       }
       # ... rest of method
   ```

4. **Add to UI Options**
   
   In `app.py`:
   ```python
   html_template = st.sidebar.selectbox(
       "HTML Template",
       ["Modern", "Minimal", "Classic", "Dark", "Professional"],  # Added
       help="Choose HTML template style"
   )
   ```

5. **Update Config**
   
   Edit `config.yaml`:
   ```yaml
   templates:
     styles:
       - name: "modern"
         description: "Clean, contemporary design"
       - name: "minimal"
         description: "Simple, distraction-free"
       - name: "classic"
         description: "Traditional document style"
       - name: "dark"
         description: "Dark mode optimized"
       - name: "professional"  # NEW
         description: "Formal business documents"
   ```

6. **Test Template**
   - Run application
   - Convert a document
   - Select "Professional" template
   - Verify styling looks correct
   - Test with different color schemes
   - Check responsive design

7. **Add Screenshot**
   - Create sample output
   - Take screenshot
   - Save to `docs/images/template-professional.png`

8. **Update Documentation**
   
   In `README.md`:
   ```markdown
   ### HTML Generation
   - **5 Template Styles**: Modern, Minimal, Classic, Dark, Professional
   ```

9. **Commit and Push**
   ```bash
   git add utils/template_manager.py app.py config.yaml README.md
   git commit -m "feat: add Professional HTML template
   
   - Add formal business document styling
   - Georgia serif font, justified text
   - Clean white article background
   - Professional color scheme
   - Update documentation"
   
   git push origin feature/professional-template
   ```

**Expected Outcome:**
- New template available in UI
- Professional styling applied correctly
- Works with all color schemes

**Time Estimate:** 1-2 hours

---

## Adding SEO Validation Rule

### Workflow: Add Meta Robots Tag Validation

**Use Case:** Validate that pages have proper robots meta tag for SEO.

**Steps:**

1. **Create Branch**
   ```bash
   git checkout -b feature/seo-robots-validation
   ```

2. **Add Validation Method**
   
   In `utils/seo_validator.py`:
   ```python
   def validate_robots_tag(self, soup):
       """Validate meta robots tag presence and configuration.
       
       Args:
           soup: BeautifulSoup HTML object
           
       Returns:
           int: Score points (0-10)
       """
       robots_meta = soup.find('meta', attrs={'name': 'robots'})
       
       if not robots_meta:
           self.warnings.append(
               "Missing meta robots tag - add to control indexing"
           )
           return 5  # Half points for missing but not critical
       
       content = robots_meta.get('content', '').lower()
       
       # Check for problematic directives
       if 'noindex' in content:
           self.issues.append(
               "Meta robots set to 'noindex' - page won't be indexed"
           )
           return 0
       
       if 'nofollow' in content:
           self.warnings.append(
               "Meta robots includes 'nofollow' - links won't be followed"
           )
           return 7
       
       # Ideal configuration
       if 'index' in content or 'follow' in content:
           self.successes.append(
               "✓ Meta robots configured for indexing"
           )
           return 10
       
       return 8  # Present but not explicit
   ```

3. **Integrate into Validation**
   
   Update `validate()` method:
   ```python
   def validate(self, html_content, filename="document.html"):
       """Run all SEO validations."""
       # ... existing validations ...
       
       # Add new validation
       score += self.validate_robots_tag(soup)
       max_score += 10
       
       # ... rest of method ...
   ```

4. **Add Enhancement Support**
   
   In `utils/seo_enhancer.py`:
   ```python
   def enhance_html(self, html_content, filename="document.html"):
       """Enhance HTML with SEO improvements."""
       # ... existing enhancements ...
       
       # Add robots meta tag if missing
       if not soup.find('meta', attrs={'name': 'robots'}):
           robots_tag = soup.new_tag('meta')
           robots_tag['name'] = 'robots'
           robots_tag['content'] = 'index, follow'
           head.append(robots_tag)
       
       # ... rest of method ...
   ```

5. **Update Scoring Weight**
   
   In `config.yaml`:
   ```yaml
   seo:
     scoring:
       # ... existing rules ...
       robots_tag:
         weight: 10
   ```

6. **Test Validation**
   ```python
   # Create test file: test_seo_robots.py
   from utils.seo_validator import SEOValidator
   
   def test_robots_validation():
       validator = SEOValidator()
       
       # Test: Missing robots tag
       html = "<html><head></head><body>Content</body></html>"
       result = validator.validate(html)
       assert "robots" in str(validator.warnings)
       
       # Test: Noindex robots tag
       html = '<html><head><meta name="robots" content="noindex"></head></html>'
       result = validator.validate(html)
       assert "noindex" in str(validator.issues)
       
       # Test: Proper robots tag
       html = '<html><head><meta name="robots" content="index, follow"></head></html>'
       result = validator.validate(html)
       # Should have success message
       
       print("All tests passed!")
   
   if __name__ == "__main__":
       test_robots_validation()
   ```

7. **Run Tests**
   ```bash
   python test_seo_robots.py
   ```

8. **Update Documentation**
   
   In `README.md` and `ARCHITECTURE.md`:
   ```markdown
   **SEO Checks:**
   - Title tags (30-60 characters)
   - Meta descriptions (120-160 characters)
   - Heading hierarchy (H1-H6)
   - Image alt text coverage
   - Internal/external links
   - Content length (300+ words)
   - Open Graph tags
   - Structured data (JSON-LD)
   - Meta robots tag ← NEW
   ```

9. **Commit Changes**
   ```bash
   git add utils/seo_validator.py utils/seo_enhancer.py config.yaml
   git add README.md ARCHITECTURE.md test_seo_robots.py
   git commit -m "feat: add meta robots tag SEO validation
   
   - Validate robots meta tag presence
   - Check for noindex/nofollow directives
   - Auto-inject optimal robots tag
   - Add test coverage
   - Update documentation"
   
   git push origin feature/seo-robots-validation
   ```

**Expected Outcome:**
- Robots tag validated in SEO report
- Proper robots tag auto-injected
- Warnings for problematic configurations

**Time Estimate:** 1-2 hours

---

## Bug Fix Workflow

### Workflow: Fix Image Extraction Bug

**Scenario:** Images from DOCX files not extracting correctly.

**Steps:**

1. **Reproduce Bug**
   - Upload DOCX with images
   - Convert to HTML
   - Observe images missing
   - Note error messages

2. **Create Issue**
   ```markdown
   Title: DOCX images not extracting
   
   **Description:**
   Images embedded in DOCX files are not appearing in converted HTML.
   
   **Steps to Reproduce:**
   1. Upload DOCX file with images
   2. Convert to HTML
   3. Check output
   
   **Expected:** Images appear in HTML
   **Actual:** Images missing
   
   **Environment:**
   - OS: Windows 10
   - Browser: Chrome 118
   - Python: 3.11
   ```

3. **Create Bug Fix Branch**
   ```bash
   git checkout main
   git pull upstream main
   git checkout -b fix/docx-image-extraction
   ```

4. **Debug Issue**
   - Add logging to `converters/docx_converter.py`
   - Print image relationships
   - Check image handler calls
   - Identify root cause

5. **Implement Fix**
   ```python
   # In converters/docx_converter.py
   def extract_images(self, image_handler):
       """Extract images from DOCX file."""
       for rel in self.doc.part.rels.values():
           if "image" in rel.target_ref:
               # FIX: Handle different image path formats
               image_data = rel.target_part.blob
               image_ext = rel.target_part.content_type.split('/')[-1]
               
               # Store image
               image_path = image_handler.store_image(
                   image_data,
                   extension=image_ext
               )
               
               self.images[rel.target_ref] = image_path
   ```

6. **Test Fix**
   - Upload problematic DOCX
   - Verify images now extract
   - Test with multiple image formats
   - Test with large images
   - Ensure no regression

7. **Add Test Case**
   ```python
   # test_docx_images.py
   def test_image_extraction():
       from converters.docx_converter import DocxConverter
       from utils.image_handler import ImageHandler
       
       # Load test DOCX with images
       with open('test_files/document_with_images.docx', 'rb') as f:
           converter = DocxConverter(f)
           image_handler = ImageHandler()
           
           markdown = converter.convert()
           
           # Verify images extracted
           assert len(image_handler.images) > 0
           assert '![' in markdown  # Markdown image syntax
   ```

8. **Update CHANGELOG**
   ```markdown
   ## [1.0.1] - 2025-10-XX
   
   ### Fixed
   - DOCX image extraction now handles all image path formats
   - Images with special characters in filenames now extract correctly
   ```

9. **Commit Fix**
   ```bash
   git add converters/docx_converter.py test_docx_images.py CHANGELOG.md
   git commit -m "fix: DOCX image extraction handling
   
   - Handle different image path formats in DOCX relationships
   - Support images with special characters
   - Add test coverage for image extraction
   
   Fixes #123"
   
   git push origin fix/docx-image-extraction
   ```

10. **Create Pull Request**
    - Reference issue number
    - Describe fix clearly
    - Include test results
    - Request review

**Expected Outcome:**
- Bug fixed
- Test added to prevent regression
- Documentation updated

**Time Estimate:** 1-3 hours depending on complexity

---

## Feature Development Workflow

### Workflow: Complete Feature Development Cycle

**Example:** Add bulk image download optimization

**Steps:**

1. **Plan Feature**
   - Write feature specification
   - Design implementation approach
   - Identify affected components
   - Estimate complexity

2. **Create Epic/Issue**
   ```markdown
   Title: Optimize bulk image downloads
   
   **Goal:** Improve performance when downloading many images from WXR
   
   **Approach:**
   - Implement concurrent downloads
   - Add progress indicator
   - Cache downloaded images
   - Handle failures gracefully
   
   **Acceptance Criteria:**
   - [ ] Downloads 100 images in <30 seconds
   - [ ] Progress bar shows accurate progress
   - [ ] Failed downloads don't stop process
   - [ ] Downloaded images cached per session
   ```

3. **Create Feature Branch**
   ```bash
   git checkout -b feature/bulk-image-optimization
   ```

4. **Implement incrementally**
   - Commit small, logical changes
   - Test after each change
   - Keep commits focused

5. **Write Tests**
   - Unit tests for new functions
   - Integration tests for workflow
   - Performance benchmarks

6. **Update Documentation**
   - README features list
   - Architecture diagrams
   - User workflow docs
   - Config file

7. **Self-Review**
   - Check code quality
   - Verify no debug code left
   - Ensure consistent style
   - Test edge cases

8. **Create Pull Request**
   - Clear title and description
   - Link related issues
   - Include screenshots/demos
   - Request specific reviewers

9. **Address Review Feedback**
   - Respond to all comments
   - Make requested changes
   - Explain design decisions
   - Re-request review

10. **Merge and Deploy**
    - Squash commits if needed
    - Update version number
    - Tag release
    - Deploy to production

**Time Estimate:** Varies by feature size (hours to days)

---

## Code Review Process

### Workflow: Reviewing Pull Requests

**As a Reviewer:**

1. **Initial Review**
   - Read PR description
   - Check linked issues
   - Review changed files list
   - Assess scope and impact

2. **Code Review**
   - Check code quality
   - Verify logic correctness
   - Look for potential bugs
   - Assess performance impact
   - Check error handling

3. **Testing**
   - Pull branch locally
   - Run application
   - Test feature manually
   - Run automated tests
   - Check edge cases

4. **Documentation Review**
   - Verify README updated
   - Check code comments
   - Review config changes
   - Ensure examples provided

5. **Provide Feedback**
   ```markdown
   **General:** Good implementation overall!
   
   **Required Changes:**
   - [ ] Add error handling in `convert()` method
   - [ ] Fix typo in comment (line 45)
   
   **Suggestions:**
   - Consider extracting this to a helper function
   - Could simplify this logic
   
   **Questions:**
   - Why did you choose this approach over X?
   - Have you tested with large files?
   ```

6. **Approve or Request Changes**
   - Approve if ready to merge
   - Request changes if issues found
   - Be constructive and helpful

**As an Author:**

1. **Respond to Feedback**
   - Address each comment
   - Explain decisions
   - Make requested changes
   - Ask for clarification if needed

2. **Update PR**
   - Push additional commits
   - Mark conversations resolved
   - Re-request review
   - Thank reviewers

**Best Practices:**
- Review within 24-48 hours
- Be respectful and constructive
- Focus on code, not person
- Suggest alternatives
- Approve when ready

---

**Last Updated:** October 8, 2025  
**Version:** 1.0.0
