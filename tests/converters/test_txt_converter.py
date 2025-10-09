"""Tests for TXT converter module."""

import io

import pytest

from converters.txt_converter import TxtConverter


class TestTxtConverter:
    """Test suite for TxtConverter class."""

    @pytest.fixture
    def converter(self):
        """Create a TxtConverter instance."""
        return TxtConverter()

    @pytest.mark.unit
    @pytest.mark.converter
    def test_convert_basic_txt(self, converter, sample_txt_file):
        """Test basic TXT conversion to markdown."""
        result = converter.convert(sample_txt_file)

        assert isinstance(result, str)
        assert len(result) > 0
        assert "Test Document" in result

    @pytest.mark.unit
    @pytest.mark.converter
    @pytest.mark.parametrize(
        "encoding",
        ["utf-8", "latin-1", "cp1252"],
    )
    def test_convert_different_encodings(self, converter, encoding):
        """Test TXT conversion with different encodings."""
        content = "Test content with special chars: é, ñ, ü"
        try:
            file_obj = io.BytesIO(content.encode(encoding))
        except UnicodeEncodeError:
            pytest.skip(f"Cannot encode test content in {encoding}")

        file_obj.name = "test.txt"
        file_obj.seek(0)

        result = converter.convert(file_obj)
        assert isinstance(result, str)
        assert len(result) > 0

    @pytest.mark.unit
    @pytest.mark.converter
    def test_convert_empty_txt(self, converter):
        """Test handling of empty TXT file."""
        content = ""
        file_obj = io.BytesIO(content.encode("utf-8"))
        file_obj.name = "empty.txt"
        file_obj.seek(0)

        result = converter.convert(file_obj)
        assert isinstance(result, str)

    @pytest.mark.unit
    @pytest.mark.converter
    def test_preserve_markdown_formatting(self, converter):
        """Test that existing markdown formatting is preserved."""
        content = "# Heading\n\n**Bold** and *italic* text\n\n- List item"
        file_obj = io.BytesIO(content.encode("utf-8"))
        file_obj.name = "markdown.txt"
        file_obj.seek(0)

        result = converter.convert(file_obj)
        assert "# Heading" in result
        assert "**Bold**" in result
        assert "*italic*" in result

    @pytest.mark.unit
    @pytest.mark.converter
    def test_multiline_text(self, converter):
        """Test handling of multi-line text."""
        content = "Line 1\nLine 2\nLine 3\n\nParagraph 2"
        file_obj = io.BytesIO(content.encode("utf-8"))
        file_obj.name = "multiline.txt"
        file_obj.seek(0)

        result = converter.convert(file_obj)
        assert "Line 1" in result
        assert "Line 2" in result
        assert "Paragraph 2" in result

    @pytest.mark.unit
    @pytest.mark.converter
    def test_special_characters(self, converter):
        """Test handling of special characters."""
        content = "Special: @#$%^&*()_+-=[]{}|;:',.<>?/~`"
        file_obj = io.BytesIO(content.encode("utf-8"))
        file_obj.name = "special.txt"
        file_obj.seek(0)

        result = converter.convert(file_obj)
        assert "Special:" in result
