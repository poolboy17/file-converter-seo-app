"""Tests for WXR converter module."""

import io

import pytest

from converters.wxr_converter import WxrConverter


class TestWxrConverter:
    """Test suite for WxrConverter class."""

    @pytest.fixture
    def converter(self):
        """Create a WxrConverter instance."""
        return WxrConverter()

    @pytest.mark.unit
    @pytest.mark.converter
    def test_convert_basic_wxr(self, converter, sample_wxr_file):
        """Test basic WXR conversion to markdown."""
        result = converter.convert(sample_wxr_file)

        assert isinstance(result, str)
        assert len(result) > 0
        assert "Test Post" in result

    @pytest.mark.unit
    @pytest.mark.converter
    def test_wxr_extract_posts(self, converter, sample_wxr_file):
        """Test extracting posts from WXR."""
        markdown = converter.convert(sample_wxr_file)

        assert isinstance(markdown, str)
        assert len(markdown) > 0
        # Check that post content is present
        assert "title" in markdown.lower()
        assert "test" in markdown.lower()

    @pytest.mark.unit
    @pytest.mark.converter
    def test_wxr_metadata_extraction(self, converter, sample_wxr_file):
        """Test metadata extraction from WXR posts."""
        markdown = converter.convert(sample_wxr_file)

        assert isinstance(markdown, str)
        assert "title" in markdown.lower() or "post" in markdown.lower()

    @pytest.mark.unit
    @pytest.mark.converter
    def test_wxr_html_to_markdown(self, converter):
        """Test HTML to markdown conversion in WXR content."""
        html = "<p>Test <strong>bold</strong> text</p>"
        result = converter._html_to_markdown(html)

        assert isinstance(result, str)
        assert "Test" in result

    @pytest.mark.unit
    @pytest.mark.converter
    def test_wxr_empty_file(self, converter):
        """Test handling of empty WXR file."""
        content = '<?xml version="1.0"?><rss><channel></channel></rss>'
        file_obj = io.BytesIO(content.encode("utf-8"))
        file_obj.name = "empty.wxr"
        file_obj.seek(0)

        result = converter.convert(file_obj)
        assert isinstance(result, str)

    @pytest.mark.unit
    @pytest.mark.converter
    def test_wxr_malformed_xml(self, converter):
        """Test handling of malformed XML."""
        content = "Not valid XML content"
        file_obj = io.BytesIO(content.encode("utf-8"))
        file_obj.name = "invalid.wxr"
        file_obj.seek(0)

        # WXR converter has fallback parsing, so it may not raise an exception
        result = converter.convert(file_obj)
        assert isinstance(result, str)
