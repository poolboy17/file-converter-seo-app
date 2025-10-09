"""Tests for frontmatter generator module."""

from datetime import datetime

import pytest

from utils.frontmatter_generator import FrontmatterGenerator


class TestFrontmatterGenerator:
    """Test suite for FrontmatterGenerator class."""

    @pytest.fixture
    def generator(self):
        """Create a FrontmatterGenerator instance."""
        return FrontmatterGenerator()

    @pytest.mark.unit
    @pytest.mark.utils
    def test_generate_jekyll_frontmatter(self, generator, sample_metadata):
        """Test Jekyll frontmatter generation."""
        result = generator.generate("jekyll", sample_metadata)

        assert "---" in result
        assert "title:" in result
        assert "Test Document" in result
        assert "layout:" in result

    @pytest.mark.unit
    @pytest.mark.utils
    def test_generate_hugo_frontmatter(self, generator, sample_metadata):
        """Test Hugo frontmatter generation."""
        result = generator.generate("hugo", sample_metadata)

        assert "---" in result
        assert "title:" in result
        assert "draft:" in result
        assert "Test Document" in result

    @pytest.mark.unit
    @pytest.mark.utils
    def test_generate_astro_frontmatter(self, generator, sample_metadata):
        """Test Astro frontmatter generation."""
        result = generator.generate("astro", sample_metadata)

        assert "---" in result
        assert "title:" in result
        assert "pubDate:" in result
        assert "Test Document" in result

    @pytest.mark.unit
    @pytest.mark.utils
    @pytest.mark.parametrize(
        "ssg_type",
        ["jekyll", "hugo", "astro", "JEKYLL", "Hugo", "Astro"],
    )
    def test_generate_case_insensitive(self, generator, sample_metadata, ssg_type):
        """Test that SSG type is case-insensitive."""
        result = generator.generate(ssg_type, sample_metadata)

        assert "---" in result
        assert "title:" in result

    @pytest.mark.unit
    @pytest.mark.utils
    def test_generate_with_missing_title(self, generator):
        """Test frontmatter generation with missing title."""
        metadata = {"author": "Test"}
        result = generator.generate("jekyll", metadata, filename="test.md")

        assert "title:" in result
        assert "test" in result.lower()

    @pytest.mark.unit
    @pytest.mark.utils
    def test_generate_with_list_tags(self, generator):
        """Test frontmatter with list of tags."""
        metadata = {"title": "Test", "tags": ["tag1", "tag2", "tag3"]}
        result = generator.generate("jekyll", metadata)

        assert "tags:" in result
        assert "tag1" in result
        assert "tag2" in result

    @pytest.mark.unit
    @pytest.mark.utils
    def test_generate_with_list_categories(self, generator):
        """Test frontmatter with list of categories."""
        metadata = {"title": "Test", "categories": ["cat1", "cat2"]}
        result = generator.generate("jekyll", metadata)

        assert "categories:" in result
        assert "cat1" in result

    @pytest.mark.unit
    @pytest.mark.utils
    def test_escape_yaml_special_chars(self, generator):
        """Test YAML escaping of special characters."""
        text = 'Test "quoted" text'
        result = generator._escape_yaml(text)

        assert "\\" in result  # Escaped quotes

    @pytest.mark.unit
    @pytest.mark.utils
    def test_format_date_iso(self, generator):
        """Test date formatting with ISO format."""
        date_str = "2024-01-01T12:00:00"
        result = generator._format_date(date_str)

        assert "2024-01-01" in result

    @pytest.mark.unit
    @pytest.mark.utils
    def test_format_date_datetime_object(self, generator):
        """Test date formatting with datetime object."""
        date_obj = datetime(2024, 1, 1, 12, 0, 0)
        result = generator._format_date(date_obj)

        assert "2024-01-01" in result

    @pytest.mark.unit
    @pytest.mark.utils
    def test_generate_slug(self, generator):
        """Test slug generation from title."""
        title = "This is a Test Title!"
        result = generator._generate_slug(title)

        assert result == "this-is-a-test-title"
        assert " " not in result
        assert "!" not in result

    @pytest.mark.unit
    @pytest.mark.utils
    def test_extract_metadata_from_markdown(
        self, generator, sample_markdown_with_frontmatter
    ):
        """Test extracting metadata from markdown with frontmatter."""
        result = generator.extract_metadata_from_markdown(
            sample_markdown_with_frontmatter
        )

        assert isinstance(result, dict)
        assert "title" in result
        assert result["title"] == "Test Document"

    @pytest.mark.unit
    @pytest.mark.utils
    def test_extract_metadata_no_frontmatter(self, generator):
        """Test extracting metadata from markdown without frontmatter."""
        markdown = "# Just a heading\n\nSome content"
        result = generator.extract_metadata_from_markdown(markdown)

        assert isinstance(result, dict)
        assert len(result) == 0

    @pytest.mark.unit
    @pytest.mark.utils
    def test_generate_default_to_jekyll(self, generator, sample_metadata):
        """Test that unknown SSG types default to Jekyll."""
        result = generator.generate("unknown_ssg", sample_metadata)

        # Should generate Jekyll-style frontmatter
        assert "---" in result
        assert "layout:" in result  # Jekyll-specific field

    @pytest.mark.unit
    @pytest.mark.utils
    def test_hugo_draft_status(self, generator):
        """Test Hugo draft status based on publish status."""
        # Published post
        metadata_published = {"title": "Test", "status": "publish"}
        result = generator.generate("hugo", metadata_published)
        assert "draft: false" in result

        # Draft post
        metadata_draft = {"title": "Test", "status": "draft"}
        result = generator.generate("hugo", metadata_draft)
        assert "draft: true" in result

    @pytest.mark.unit
    @pytest.mark.utils
    def test_custom_fields_preservation(self, generator):
        """Test that custom fields are preserved in frontmatter."""
        metadata = {"title": "Test", "custom_field": "custom_value"}
        result = generator.generate("jekyll", metadata)

        assert "custom_field:" in result
        assert "custom_value" in result
