"""Tests for DOCX converter module."""

import pytest

from converters.docx_converter import DocxConverter


class TestDocxConverter:
    """Test suite for DocxConverter class."""

    @pytest.fixture
    def converter(self):
        """Create a DocxConverter instance."""
        return DocxConverter()

    @pytest.mark.unit
    @pytest.mark.converter
    def test_convert_basic_docx(self, converter, sample_docx_file):
        """Test basic DOCX conversion to markdown."""
        result = converter.convert(sample_docx_file)

        assert isinstance(result, str)
        assert len(result) > 0
        assert "Test Document" in result

    @pytest.mark.unit
    @pytest.mark.converter
    def test_docx_headings_conversion(self, converter, sample_docx_file):
        """Test that DOCX headings are converted to markdown."""
        result = converter.convert(sample_docx_file)

        # Check for markdown heading formats
        assert "#" in result or "Section" in result

    @pytest.mark.unit
    @pytest.mark.converter
    def test_docx_paragraphs_conversion(self, converter, sample_docx_file):
        """Test that DOCX paragraphs are converted."""
        result = converter.convert(sample_docx_file)

        assert "paragraph" in result.lower() or "section" in result.lower()

    @pytest.mark.unit
    @pytest.mark.converter
    def test_docx_preserves_content_structure(self, converter, sample_docx_file):
        """Test that content structure is preserved."""
        result = converter.convert(sample_docx_file)

        # Should have multiple lines/sections
        lines = result.split("\n")
        assert len(lines) > 1
