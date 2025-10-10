"""Tests for file utilities module."""

import io
import zipfile

import pytest

from utils.file_utils import create_download_zip, create_file_metadata, get_file_extension


class TestFileUtils:
    """Test suite for file utility functions."""

    @pytest.mark.unit
    @pytest.mark.utils
    @pytest.mark.parametrize(
        "filename,expected",
        [
            ("test.csv", "csv"),
            ("document.docx", "docx"),
            ("file.TXT", "txt"),
            ("archive.ZIP", "zip"),
            ("no_extension", ""),
        ],
    )
    def test_get_file_extension(self, filename, expected):
        """Test file extension extraction."""
        result = get_file_extension(filename)
        assert result == expected

    @pytest.mark.unit
    @pytest.mark.utils
    def test_create_file_metadata_basic(self):
        """Test creating file metadata."""
        file_data = {
            "original_name": "test.csv",
            "file_type": "csv",
            "markdown_content": "# Test\n\nContent here",
            "html_content": "<h1>Test</h1><p>Content here</p>",
        }

        result = create_file_metadata(file_data)

        assert isinstance(result, str)
        assert "test.csv" in result
        assert "CSV" in result
        assert "Markdown length:" in result

    @pytest.mark.unit
    @pytest.mark.utils
    def test_create_download_zip_markdown(self):
        """Test creating download ZIP with markdown files."""
        converted_files = [
            {
                "original_name": "test1.csv",
                "file_type": "csv",
                "markdown_content": "# Test 1",
                "html_content": None,
            },
            {
                "original_name": "test2.txt",
                "file_type": "txt",
                "markdown_content": "# Test 2",
                "html_content": None,
            },
        ]

        result = create_download_zip(converted_files, "Markdown")

        assert isinstance(result, io.BytesIO)

        # Verify ZIP contents - each article in its own folder
        with zipfile.ZipFile(result, "r") as zip_file:
            names = zip_file.namelist()
            assert any("test1/index.md" in name for name in names)
            assert any("test2/index.md" in name for name in names)

    @pytest.mark.unit
    @pytest.mark.utils
    def test_create_download_zip_html(self):
        """Test creating download ZIP with HTML files."""
        converted_files = [
            {
                "original_name": "test.csv",
                "file_type": "csv",
                "markdown_content": "# Test",
                "html_content": "<h1>Test</h1>",
            }
        ]

        result = create_download_zip(converted_files, "HTML")

        assert isinstance(result, io.BytesIO)

        # Verify ZIP contents - HTML in article folder
        with zipfile.ZipFile(result, "r") as zip_file:
            names = zip_file.namelist()
            assert any("test/index.html" in name for name in names)

    @pytest.mark.unit
    @pytest.mark.utils
    def test_create_download_zip_both_formats(self):
        """Test creating ZIP with both markdown and HTML."""
        converted_files = [
            {
                "original_name": "test.csv",
                "file_type": "csv",
                "markdown_content": "# Test",
                "html_content": "<h1>Test</h1>",
            }
        ]

        result = create_download_zip(converted_files, "Both")

        # Verify both formats in article folder
        with zipfile.ZipFile(result, "r") as zip_file:
            names = zip_file.namelist()
            assert any("test/index.md" in name for name in names)
            assert any("test/index.html" in name for name in names)

    @pytest.mark.unit
    @pytest.mark.utils
    def test_create_download_zip_includes_metadata(self):
        """Test that ZIP includes metadata files."""
        converted_files = [
            {
                "original_name": "test.csv",
                "file_type": "csv",
                "markdown_content": "# Test",
                "html_content": None,
            }
        ]

        result = create_download_zip(converted_files, "Markdown")

        with zipfile.ZipFile(result, "r") as zip_file:
            names = zip_file.namelist()
            assert any("metadata" in name for name in names)

    @pytest.mark.unit
    @pytest.mark.utils
    def test_create_download_zip_empty_list(self):
        """Test creating ZIP with empty file list."""
        converted_files = []
        result = create_download_zip(converted_files, "Markdown")

        assert isinstance(result, io.BytesIO)

        with zipfile.ZipFile(result, "r") as zip_file:
            assert len(zip_file.namelist()) == 0
