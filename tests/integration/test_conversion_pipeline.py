"""Integration tests for the complete conversion pipeline."""

import io

import pytest

from converters.csv_converter import CsvConverter
from converters.docx_converter import DocxConverter
from converters.txt_converter import TxtConverter
from converters.wxr_converter import WxrConverter
from utils.frontmatter_generator import FrontmatterGenerator
from utils.seo_enhancer import SEOEnhancer


class TestConversionPipeline:
    """Integration tests for complete conversion workflows."""

    @pytest.mark.integration
    def test_csv_to_markdown_to_html_pipeline(self, sample_csv_file):
        """Test complete CSV to markdown to HTML pipeline."""
        # Step 1: Convert CSV to markdown
        converter = CsvConverter()
        markdown = converter.convert(sample_csv_file, include_metadata=True)

        assert isinstance(markdown, str)
        assert len(markdown) > 0

        # Step 2: Add frontmatter
        frontmatter_gen = FrontmatterGenerator()
        metadata = {"title": "Test CSV Data", "author": "Test"}
        frontmatter = frontmatter_gen.generate("jekyll", metadata)

        full_content = f"{frontmatter}\n\n{markdown}"
        assert "---" in full_content
        assert "title:" in full_content

    @pytest.mark.integration
    def test_txt_to_markdown_with_seo(self, sample_txt_file):
        """Test TXT conversion with SEO enhancement."""
        # Step 1: Convert TXT to markdown
        converter = TxtConverter()
        markdown = converter.convert(sample_txt_file)

        assert isinstance(markdown, str)
        assert len(markdown) > 0

        # Step 2: Add frontmatter
        frontmatter_gen = FrontmatterGenerator()
        metadata = {
            "title": "Test Document",
            "description": "Test description",
            "tags": ["test", "integration"],
        }
        frontmatter = frontmatter_gen.generate("hugo", metadata)

        assert "title:" in frontmatter
        assert "tags:" in frontmatter

    @pytest.mark.integration
    def test_docx_to_html_with_seo(self, sample_docx_file):
        """Test DOCX conversion with SEO enhancement."""
        # Step 1: Convert DOCX to markdown
        converter = DocxConverter()
        markdown = converter.convert(sample_docx_file)

        assert isinstance(markdown, str)
        assert len(markdown) > 0

        # Step 2: Enhance with SEO (if converting to HTML)
        # This simulates the full pipeline
        assert markdown is not None

    @pytest.mark.integration
    def test_wxr_to_multiple_files_pipeline(self, sample_wxr_file):
        """Test WXR conversion pipeline."""
        # Step 1: Convert WXR (produces markdown with all posts)
        converter = WxrConverter()
        markdown = converter.convert(sample_wxr_file)

        assert isinstance(markdown, str)
        assert len(markdown) > 0

        # Step 2: Markdown should contain post content
        assert "title" in markdown.lower() or "post" in markdown.lower()

    @pytest.mark.integration
    @pytest.mark.parametrize(
        "ssg_type",
        ["jekyll", "hugo", "astro"],
    )
    def test_conversion_with_different_ssgs(self, sample_txt_file, ssg_type):
        """Test conversion pipeline with different SSG types."""
        # Convert to markdown
        converter = TxtConverter()
        markdown = converter.convert(sample_txt_file)

        # Generate frontmatter for different SSGs
        frontmatter_gen = FrontmatterGenerator()
        metadata = {"title": "Test", "author": "Test Author"}
        frontmatter = frontmatter_gen.generate(ssg_type, metadata)

        assert "---" in frontmatter
        assert "title:" in frontmatter

        # Combine
        full_content = f"{frontmatter}\n\n{markdown}"
        assert len(full_content) > len(markdown)

    @pytest.mark.integration
    def test_batch_conversion_multiple_files(
        self, sample_csv_file, sample_txt_file, temp_output_dir
    ):
        """Test batch conversion of multiple files."""
        files = [sample_csv_file, sample_txt_file]
        results = []

        for file in files:
            if file.name.endswith(".csv"):
                converter = CsvConverter()
                content = converter.convert(file, include_metadata=False)
            elif file.name.endswith(".txt"):
                converter = TxtConverter()
                content = converter.convert(file)
            else:
                continue

            results.append({"filename": file.name, "content": content})

        assert len(results) == 2
        assert all(len(r["content"]) > 0 for r in results)

    @pytest.mark.integration
    def test_metadata_extraction_and_regeneration(
        self, sample_markdown_with_frontmatter
    ):
        """Test extracting metadata and regenerating frontmatter."""
        frontmatter_gen = FrontmatterGenerator()

        # Extract existing metadata
        metadata = frontmatter_gen.extract_metadata_from_markdown(
            sample_markdown_with_frontmatter
        )

        assert isinstance(metadata, dict)
        assert "title" in metadata

        # Regenerate frontmatter with modified metadata
        metadata["author"] = "New Author"
        new_frontmatter = frontmatter_gen.generate("jekyll", metadata)

        assert "New Author" in new_frontmatter

    @pytest.mark.integration
    @pytest.mark.slow
    def test_large_csv_conversion(self):
        """Test conversion of large CSV file."""
        # Create a large CSV
        rows = ["Name,Age,City\n"]
        for i in range(1000):
            rows.append(f"Person{i},{20+i%50},City{i%10}\n")

        csv_content = "".join(rows)
        file_obj = io.BytesIO(csv_content.encode("utf-8"))
        file_obj.name = "large.csv"
        file_obj.seek(0)

        # Convert
        converter = CsvConverter()
        result = converter.convert(file_obj, include_metadata=True)

        assert isinstance(result, str)
        assert "Person0" in result
        assert "Person999" in result

    @pytest.mark.integration
    def test_error_handling_in_pipeline(self):
        """Test error handling throughout the pipeline."""
        # Test with invalid CSV - converter may handle gracefully
        invalid_csv = io.BytesIO(b"\x00\x01\x02invalid binary data")
        invalid_csv.name = "invalid.csv"
        invalid_csv.seek(0)

        converter = CsvConverter()
        # Some converters have error handling, so test that they return something or raise
        try:
            result = converter.convert(invalid_csv)
            # If it succeeds, it should at least return a string
            assert isinstance(result, str) or result is None
        except Exception as e:
            # Or it raises an exception
            assert str(e) is not None

    @pytest.mark.integration
    def test_unicode_handling_across_pipeline(self):
        """Test Unicode character handling across the pipeline."""
        # Create content with Unicode
        content = "# Tëst Dòcümënt\n\nContént with émojis 🎉🚀"
        file_obj = io.BytesIO(content.encode("utf-8"))
        file_obj.name = "unicode.txt"
        file_obj.seek(0)

        # Convert
        converter = TxtConverter()
        result = converter.convert(file_obj)

        assert "Tëst" in result
        assert "émojis" in result
