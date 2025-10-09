# Testing Blueprint for File Converter SEO App

## Overview

This testing suite provides comprehensive coverage for the file converter application using pytest with best practices including fixtures, parametrization, and markers.

## Structure

```
tests/
├── __init__.py
├── conftest.py                    # Shared fixtures and configuration
├── README.md                      # This file
├── converters/                    # Converter module tests
│   ├── __init__.py
│   ├── test_csv_converter.py
│   ├── test_docx_converter.py
│   ├── test_txt_converter.py
│   └── test_wxr_converter.py
├── utils/                         # Utility module tests
│   ├── __init__.py
│   ├── test_frontmatter_generator.py
│   ├── test_seo_enhancer.py
│   ├── test_file_utils.py
│   └── test_image_handler.py
└── integration/                   # Integration tests
    ├── __init__.py
    └── test_conversion_pipeline.py
```

## Running Tests

### Run all tests
```bash
pytest
```

### Run with coverage report
```bash
pytest --cov=converters --cov=utils --cov-report=html
```

### Run specific test categories
```bash
# Unit tests only
pytest -m unit

# Integration tests only
pytest -m integration

# Converter tests only
pytest -m converter

# Utils tests only
pytest -m utils

# Exclude slow tests
pytest -m "not slow"
```

### Run specific test file
```bash
pytest tests/converters/test_csv_converter.py
```

### Run with verbose output
```bash
pytest -v
```

### Run and stop on first failure
```bash
pytest -x
```

## Test Markers

Tests are organized using pytest markers:

- `@pytest.mark.unit` - Unit tests for individual functions/methods
- `@pytest.mark.integration` - Integration tests for multiple components
- `@pytest.mark.converter` - Tests for converter modules
- `@pytest.mark.utils` - Tests for utility modules
- `@pytest.mark.slow` - Tests that take longer to run
- `@pytest.mark.parametrize` - Parametrized tests with multiple inputs

## Fixtures

### Common Fixtures (in conftest.py)

#### File Fixtures
- `temp_test_dir` - Temporary directory for test files
- `sample_csv_file` - Mock CSV file object
- `sample_txt_file` - Mock TXT file object
- `sample_docx_file` - Mock DOCX file object
- `sample_wxr_file` - Mock WordPress WXR file object

#### Content Fixtures
- `sample_csv_content` - Sample CSV content string
- `sample_txt_content` - Sample text content
- `sample_dataframe` - Sample pandas DataFrame
- `sample_html_content` - Sample HTML content
- `sample_wxr_content` - Sample WXR/XML content

#### Metadata Fixtures
- `sample_metadata` - Sample metadata dictionary
- `sample_markdown_with_frontmatter` - Markdown with frontmatter
- `sample_seo_metadata` - SEO metadata dictionary

#### Utility Fixtures
- `temp_output_dir` - Temporary output directory
- `mock_streamlit_file` - Mock Streamlit uploaded file class
- `sample_image_data` - Base64 encoded sample image

## Writing New Tests

### Template for Unit Test

```python
import pytest
from module_name import ClassName

class TestClassName:
    """Test suite for ClassName."""

    @pytest.fixture
    def instance(self):
        """Create a ClassName instance."""
        return ClassName()

    @pytest.mark.unit
    @pytest.mark.utils  # or @pytest.mark.converter
    def test_method_name(self, instance):
        """Test description."""
        result = instance.method_name(input_data)

        assert result is not None
        assert expected_value in result
```

### Template for Parametrized Test

```python
@pytest.mark.unit
@pytest.mark.parametrize(
    "input_value,expected_output",
    [
        ("input1", "output1"),
        ("input2", "output2"),
        ("input3", "output3"),
    ],
)
def test_with_multiple_inputs(self, instance, input_value, expected_output):
    """Test with multiple input scenarios."""
    result = instance.method(input_value)
    assert result == expected_output
```

### Template for Integration Test

```python
@pytest.mark.integration
def test_complete_workflow(self, sample_file, temp_output_dir):
    """Test complete workflow from input to output."""
    # Step 1: Convert
    converter = Converter()
    result1 = converter.convert(sample_file)

    # Step 2: Process
    processor = Processor()
    result2 = processor.process(result1)

    # Step 3: Verify
    assert result2 is not None
    assert len(result2) > 0
```

## Coverage Goals

- **Target**: 80%+ overall coverage (configured in pytest.ini)
- **Priority Areas**:
  - Converters: 85%+
  - Utils: 80%+
  - Integration: 70%+

## Best Practices

1. **Use descriptive test names**: Test names should clearly describe what is being tested
2. **One assertion per concept**: Keep tests focused on a single behavior
3. **Use fixtures**: Reuse common setup code via fixtures
4. **Parametrize when possible**: Test multiple scenarios with parametrization
5. **Mark tests appropriately**: Use markers for categorization
6. **Test edge cases**: Include tests for empty inputs, invalid data, etc.
7. **Mock external dependencies**: Use mocks for network calls, file I/O, etc.
8. **Clean up resources**: Use fixtures with yield or tmp_path for cleanup

## Continuous Integration

### Pre-commit Checks
```bash
# Run tests before committing
pytest -x --cov=converters --cov=utils --cov-fail-under=80
```

### Coverage Report
After running tests with coverage, view the HTML report:
```bash
# Open coverage report
open htmlcov/index.html  # macOS
start htmlcov/index.html  # Windows
xdg-open htmlcov/index.html  # Linux
```

## Dependencies

Required testing packages (add to pyproject.toml):
```toml
[project.optional-dependencies]
dev = [
    "pytest>=7.4.0",
    "pytest-cov>=4.1.0",
    "pytest-mock>=3.11.0",
]
```

Install with:
```bash
pip install pytest pytest-cov pytest-mock
```

## Troubleshooting

### Tests not found
- Ensure files are named `test_*.py` or `*_test.py`
- Ensure classes are named `Test*`
- Ensure methods are named `test_*`

### Import errors
- Ensure modules are in PYTHONPATH
- Run tests from project root directory
- Check that `__init__.py` files exist

### Coverage too low
- Review coverage report: `pytest --cov-report=term-missing`
- Add tests for uncovered lines
- Consider excluding generated/boilerplate code

## Future Enhancements

- [ ] Add property-based testing with Hypothesis
- [ ] Add mutation testing with mutmut
- [ ] Add performance benchmarks with pytest-benchmark
- [ ] Add API tests for Streamlit components
- [ ] Add visual regression tests for HTML output
- [ ] Add security tests with bandit integration
