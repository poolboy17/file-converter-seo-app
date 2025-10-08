# Contributing to File Converter with SEO Optimization

Thank you for considering contributing to this project! We welcome contributions from everyone.

## Code of Conduct

- Be respectful and inclusive
- Focus on constructive feedback
- Help others learn and grow
- Maintain professional communication

## How to Contribute

### Reporting Bugs

Before creating a bug report:
1. Check existing issues to avoid duplicates
2. Collect relevant information (OS, Python version, error messages)
3. Create a minimal reproducible example

**Bug Report Template:**
```markdown
**Description**: Brief description of the issue

**Steps to Reproduce**:
1. Step one
2. Step two
3. Step three

**Expected Behavior**: What should happen

**Actual Behavior**: What actually happens

**Environment**:
- OS: [e.g., Windows 10, macOS 14, Ubuntu 22.04]
- Python Version: [e.g., 3.11.5]
- Streamlit Version: [e.g., 1.28.0]

**Additional Context**: Screenshots, logs, or other relevant information
```

### Suggesting Enhancements

Enhancement suggestions are tracked as GitHub issues. When creating an enhancement suggestion:

1. Use a clear, descriptive title
2. Provide detailed explanation of the proposed feature
3. Explain why this enhancement would be useful
4. Include examples or mockups if applicable

### Pull Requests

1. **Fork the Repository**
   ```bash
   git clone https://github.com/poolboy17/file-converter-seo-app.git
   cd file-converter-seo-app
   ```

2. **Create a Branch**
   ```bash
   git checkout -b feature/your-feature-name
   # or
   git checkout -b fix/your-bug-fix
   ```

3. **Make Your Changes**
   - Write clean, readable code
   - Follow existing code style
   - Add comments for complex logic
   - Update documentation as needed

4. **Test Your Changes**
   - Test with various file formats
   - Verify UI changes across browsers
   - Check SEO validation results
   - Ensure no regression in existing features

5. **Commit Your Changes**
   ```bash
   git add .
   git commit -m "feat: add new converter for XYZ format"
   ```

   **Commit Message Guidelines:**
   - `feat:` - New feature
   - `fix:` - Bug fix
   - `docs:` - Documentation changes
   - `style:` - Code style changes (formatting, etc.)
   - `refactor:` - Code refactoring
   - `test:` - Adding or updating tests
   - `chore:` - Maintenance tasks

6. **Push to Your Fork**
   ```bash
   git push origin feature/your-feature-name
   ```

7. **Create Pull Request**
   - Go to the original repository
   - Click "New Pull Request"
   - Select your branch
   - Fill in the PR template
   - Link related issues

### Pull Request Template

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Enhancement
- [ ] Documentation update
- [ ] Refactoring

## Related Issues
Fixes #(issue number)

## Testing
- [ ] Tested with DOCX files
- [ ] Tested with CSV files
- [ ] Tested with TXT files
- [ ] Tested with WXR files
- [ ] SEO validation tested
- [ ] Static site generation tested
- [ ] UI tested in multiple browsers

## Checklist
- [ ] Code follows project style guidelines
- [ ] Self-review completed
- [ ] Comments added for complex code
- [ ] Documentation updated
- [ ] No new warnings generated
- [ ] All tests pass

## Screenshots (if applicable)
Add screenshots for UI changes
```

## Development Setup

### Prerequisites
- Python 3.11 or higher
- Git
- Text editor or IDE

### Local Development

1. **Clone and Setup**
   ```bash
   git clone https://github.com/poolboy17/file-converter-seo-app.git
   cd file-converter-seo-app
   pip install -r requirements.txt
   ```

2. **Run Development Server**
   ```bash
   streamlit run app.py --server.port 5000
   ```

3. **Make Changes**
   - Edit files in your preferred editor
   - Streamlit auto-reloads on file changes
   - Test thoroughly before committing

### Code Style Guidelines

**Python Code:**
- Follow PEP 8 style guide
- Use 4 spaces for indentation
- Maximum line length: 100 characters
- Use descriptive variable names
- Add docstrings to functions and classes

**Example:**
```python
def convert_document(file_path: str, output_format: str) -> str:
    """
    Convert a document to the specified output format.
    
    Args:
        file_path: Path to the input file
        output_format: Desired output format (markdown, html)
    
    Returns:
        Converted content as string
    
    Raises:
        ValueError: If output_format is not supported
    """
    # Implementation
    pass
```

**HTML/CSS:**
- Use semantic HTML5 elements
- Keep CSS modular and reusable
- Add comments for complex styling
- Ensure responsive design

**Documentation:**
- Use clear, concise language
- Include code examples
- Keep README up to date
- Document all public APIs

## Adding New Features

### New File Format Converter

1. Create converter class in `converters/`:
```python
class NewFormatConverter:
    """Converter for NEW_FORMAT files."""
    
    def __init__(self, file):
        self.file = file
    
    def convert(self):
        """Convert NEW_FORMAT to Markdown."""
        # Implementation
        return markdown_content
```

2. Register in `app.py`:
```python
CONVERTERS = {
    '.new': NewFormatConverter,
}
```

3. Add tests and documentation

### New SEO Validation Rule

1. Add method to `SEOValidator` class:
```python
def validate_new_rule(self, soup):
    """Validate new SEO rule."""
    # Check condition
    if not meets_requirement:
        self.issues.append("Issue description")
        return 0
    return 10  # Score for passing
```

2. Call in `validate()` method
3. Update documentation with new rule

### New HTML Template

1. Create template in `templates/`
2. Register in `TemplateManager` class
3. Add CSS styling
4. Test across browsers
5. Update documentation

## Testing

### Manual Testing Checklist

**File Conversion:**
- [ ] DOCX files convert correctly
- [ ] CSV tables render properly
- [ ] TXT files preserve formatting
- [ ] WXR extracts posts/pages

**Image Handling:**
- [ ] Embedded images extracted
- [ ] Remote images downloaded
- [ ] Image optimization works
- [ ] Deduplication functions

**SEO Features:**
- [ ] Validation detects issues
- [ ] Enhancements add correctly
- [ ] Reports display accurately
- [ ] Toggle enables/disables properly

**UI/UX:**
- [ ] File upload works
- [ ] Options update correctly
- [ ] Downloads function
- [ ] Error messages clear

### Browser Testing
Test in:
- Chrome/Edge (latest)
- Firefox (latest)
- Safari (latest if on macOS)

## Documentation

### What to Document

- Public APIs and functions
- Complex algorithms or logic
- Configuration options
- Usage examples
- Architecture decisions

### Documentation Style

- Use Markdown for text files
- Include code examples
- Add diagrams for complex flows
- Keep language clear and concise
- Update README for user-facing changes

## Review Process

1. **Automated Checks**: PRs trigger automated checks
2. **Code Review**: Maintainer reviews code quality
3. **Testing**: Verify all tests pass
4. **Discussion**: Address reviewer feedback
5. **Merge**: Approved PRs are merged

## Release Process

Releases follow semantic versioning (MAJOR.MINOR.PATCH):
- MAJOR: Breaking changes
- MINOR: New features (backward compatible)
- PATCH: Bug fixes

## Questions?

- Open an issue for questions
- Check existing documentation
- Review closed issues and PRs

## Recognition

Contributors are recognized in:
- GitHub contributors list
- CHANGELOG.md entries
- README.md acknowledgments

Thank you for contributing! 🎉
