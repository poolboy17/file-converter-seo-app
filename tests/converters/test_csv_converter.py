"""Tests for CSV converter module."""

import io

import pandas as pd
import pytest

from converters.csv_converter import CsvConverter


class TestCsvConverter:
    """Test suite for CsvConverter class."""

    @pytest.fixture
    def converter(self):
        """Create a CsvConverter instance."""
        return CsvConverter()

    @pytest.mark.unit
    @pytest.mark.converter
    def test_convert_basic_csv(self, converter, sample_csv_file):
        """Test basic CSV conversion to markdown."""
        result = converter.convert(sample_csv_file, include_metadata=False)

        assert isinstance(result, str)
        assert "Name" in result
        assert "John Doe" in result
        assert "|" in result  # Markdown table format

    @pytest.mark.unit
    @pytest.mark.converter
    def test_convert_with_metadata(self, converter, sample_csv_file):
        """Test CSV conversion with metadata included."""
        result = converter.convert(sample_csv_file, include_metadata=True)

        assert isinstance(result, str)
        assert "rows" in result.lower() or "columns" in result.lower()

    @pytest.mark.unit
    @pytest.mark.converter
    @pytest.mark.parametrize(
        "encoding,content",
        [
            ("utf-8", "Name,Value\nTest,123"),
            ("latin-1", "Name,Value\nTest,456"),
        ],
    )
    def test_convert_different_encodings(self, converter, encoding, content):
        """Test CSV conversion with different encodings."""
        file_obj = io.BytesIO(content.encode(encoding))
        file_obj.name = "test.csv"
        file_obj.seek(0)

        result = converter.convert(file_obj, include_metadata=False)
        assert "Name" in result
        assert "Value" in result

    @pytest.mark.unit
    @pytest.mark.converter
    def test_convert_empty_csv(self, converter):
        """Test handling of empty CSV file."""
        content = ""
        file_obj = io.BytesIO(content.encode("utf-8"))
        file_obj.name = "empty.csv"
        file_obj.seek(0)

        with pytest.raises(Exception):
            converter.convert(file_obj)

    @pytest.mark.unit
    @pytest.mark.converter
    def test_dataframe_to_markdown(self, converter, sample_dataframe):
        """Test DataFrame to markdown table conversion."""
        result = converter._dataframe_to_markdown(sample_dataframe)

        assert isinstance(result, list)
        assert len(result) > 0
        assert any("Name" in line for line in result)
        assert any("|" in line for line in result)

    @pytest.mark.unit
    @pytest.mark.converter
    def test_extract_metadata(self, converter, sample_dataframe):
        """Test metadata extraction from DataFrame."""
        result = converter._extract_metadata(sample_dataframe, "test.csv")

        assert isinstance(result, list)
        assert len(result) > 0

    @pytest.mark.unit
    @pytest.mark.converter
    def test_csv_with_special_characters(self, converter):
        """Test CSV with special characters."""
        content = 'Name,Description\n"Test","Text with ""quotes"" and, commas"'
        file_obj = io.BytesIO(content.encode("utf-8"))
        file_obj.name = "special.csv"
        file_obj.seek(0)

        result = converter.convert(file_obj, include_metadata=False)
        assert "Test" in result

    @pytest.mark.unit
    @pytest.mark.converter
    def test_csv_with_numeric_data(self, converter):
        """Test CSV with numeric data for statistics."""
        content = "Number,Value\n1,100\n2,200\n3,300"
        file_obj = io.BytesIO(content.encode("utf-8"))
        file_obj.name = "numeric.csv"
        file_obj.seek(0)

        result = converter.convert(file_obj, include_metadata=True)
        assert isinstance(result, str)
        assert "Number" in result

    @pytest.mark.unit
    @pytest.mark.converter
    def test_csv_with_missing_values(self, converter):
        """Test CSV with missing/null values."""
        content = "Name,Age,City\nJohn,30,NYC\nJane,,London\nBob,25,"
        file_obj = io.BytesIO(content.encode("utf-8"))
        file_obj.name = "missing.csv"
        file_obj.seek(0)

        result = converter.convert(file_obj, include_metadata=False)
        assert "John" in result
        assert "Jane" in result
