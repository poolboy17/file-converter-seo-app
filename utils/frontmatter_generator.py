import re
from datetime import datetime
from typing import Any

import yaml


class FrontmatterGenerator:
    """Generate frontmatter for various static site generators."""

    def __init__(self):
        self.generators = {
            "jekyll": self._generate_jekyll_frontmatter,
            "hugo": self._generate_hugo_frontmatter,
            "astro": self._generate_astro_frontmatter,
        }

    def generate(
        self, ssg_type: str, metadata: dict[str, Any], filename: str = None
    ) -> str:
        """
        Generate frontmatter for specified SSG.

        Args:
            ssg_type: Type of static site generator (jekyll, hugo, astro)
            metadata: Metadata dictionary to convert to frontmatter
            filename: Original filename for fallback title

        Returns:
            str: Formatted frontmatter string
        """
        # Ensure we have at least a title
        if "title" not in metadata or not metadata["title"]:
            if filename:
                metadata["title"] = filename.rsplit(".", 1)[0]
            else:
                metadata["title"] = "Untitled"

        if ssg_type.lower() in self.generators:
            return self.generators[ssg_type.lower()](metadata)
        else:
            return self._generate_jekyll_frontmatter(metadata)  # Default to Jekyll

    def _generate_jekyll_frontmatter(self, metadata: dict[str, Any]) -> str:
        """Generate Jekyll-compatible YAML frontmatter."""
        lines = ["---"]

        # Title (required)
        if "title" in metadata:
            lines.append(f"title: \"{self._escape_yaml(metadata['title'])}\"")

        # Date
        if "date" in metadata:
            lines.append(f"date: {self._format_date(metadata['date'])}")
        elif "created" in metadata:
            lines.append(f"date: {self._format_date(metadata['created'])}")
        else:
            lines.append(f"date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S %z')}")

        # Author
        if "author" in metadata:
            lines.append(f"author: \"{self._escape_yaml(metadata['author'])}\"")

        # Categories
        if "categories" in metadata and metadata["categories"]:
            if isinstance(metadata["categories"], list):
                lines.append("categories:")
                for cat in metadata["categories"]:
                    lines.append(f"  - {self._escape_yaml(str(cat))}")
            else:
                lines.append(
                    f"categories: [{self._escape_yaml(str(metadata['categories']))}]"
                )

        # Tags
        if "tags" in metadata and metadata["tags"]:
            if isinstance(metadata["tags"], list):
                lines.append("tags:")
                for tag in metadata["tags"]:
                    lines.append(f"  - {self._escape_yaml(str(tag))}")
            else:
                lines.append(f"tags: [{self._escape_yaml(str(metadata['tags']))}]")

        # Layout
        if "layout" in metadata:
            lines.append(f"layout: {metadata['layout']}")
        else:
            lines.append("layout: post")

        # Permalink
        if "permalink" in metadata:
            lines.append(f"permalink: {metadata['permalink']}")

        # Excerpt
        if "excerpt" in metadata:
            lines.append(f"excerpt: \"{self._escape_yaml(metadata['excerpt'])}\"")

        # Custom fields
        for key, value in metadata.items():
            if key not in [
                "title",
                "date",
                "created",
                "author",
                "categories",
                "tags",
                "layout",
                "permalink",
                "excerpt",
            ]:
                if isinstance(value, (list, dict)):
                    continue  # Skip complex types for now
                lines.append(f'{key}: "{self._escape_yaml(str(value))}"')

        lines.append("---")
        return "\n".join(lines)

    def _generate_hugo_frontmatter(self, metadata: dict[str, Any]) -> str:
        """Generate Hugo-compatible YAML/TOML frontmatter."""
        lines = ["---"]

        # Title (required)
        if "title" in metadata:
            lines.append(f"title: \"{self._escape_yaml(metadata['title'])}\"")

        # Date
        if "date" in metadata:
            lines.append(f"date: {self._format_date(metadata['date'])}")
        elif "created" in metadata:
            lines.append(f"date: {self._format_date(metadata['created'])}")
        else:
            lines.append(f"date: {datetime.now().isoformat()}")

        # Draft status
        if "status" in metadata:
            draft = metadata["status"] != "publish"
            lines.append(f"draft: {str(draft).lower()}")
        else:
            lines.append("draft: false")

        # Author/Authors
        if "author" in metadata:
            lines.append(f"author: \"{self._escape_yaml(metadata['author'])}\"")

        # Description/Summary
        if "excerpt" in metadata:
            lines.append(f"description: \"{self._escape_yaml(metadata['excerpt'])}\"")
        elif "subject" in metadata:
            lines.append(f"description: \"{self._escape_yaml(metadata['subject'])}\"")

        # Tags
        if "tags" in metadata and metadata["tags"]:
            if isinstance(metadata["tags"], list):
                lines.append("tags:")
                for tag in metadata["tags"]:
                    lines.append(f'  - "{self._escape_yaml(str(tag))}"')
            else:
                lines.append(f"tags: [\"{self._escape_yaml(str(metadata['tags']))}\"]")

        # Categories
        if "categories" in metadata and metadata["categories"]:
            if isinstance(metadata["categories"], list):
                lines.append("categories:")
                for cat in metadata["categories"]:
                    lines.append(f'  - "{self._escape_yaml(str(cat))}"')
            else:
                lines.append(
                    f"categories: [\"{self._escape_yaml(str(metadata['categories']))}\"]"
                )

        # Slug
        if "title" in metadata:
            slug = self._generate_slug(metadata["title"])
            lines.append(f'slug: "{slug}"')

        # Weight (for ordering)
        lines.append("weight: 10")

        # Custom taxonomies
        if "post_type" in metadata and metadata["post_type"]:
            lines.append(f"type: \"{metadata['post_type']}\"")

        lines.append("---")
        return "\n".join(lines)

    def _generate_astro_frontmatter(self, metadata: dict[str, Any]) -> str:
        """Generate Astro-compatible frontmatter."""
        lines = ["---"]

        # Title (required)
        if "title" in metadata:
            lines.append(f"title: \"{self._escape_yaml(metadata['title'])}\"")

        # Description
        if "excerpt" in metadata:
            lines.append(f"description: \"{self._escape_yaml(metadata['excerpt'])}\"")
        elif "subject" in metadata:
            lines.append(f"description: \"{self._escape_yaml(metadata['subject'])}\"")

        # Publish Date
        if "date" in metadata:
            lines.append(f"pubDate: \"{self._format_date(metadata['date'])}\"")
        elif "created" in metadata:
            lines.append(f"pubDate: \"{self._format_date(metadata['created'])}\"")
        else:
            lines.append(f"pubDate: \"{datetime.now().strftime('%Y-%m-%d')}\"")

        # Updated Date
        if "modified" in metadata:
            lines.append(f"updatedDate: \"{self._format_date(metadata['modified'])}\"")

        # Author
        if "author" in metadata:
            lines.append(f"author: \"{self._escape_yaml(metadata['author'])}\"")

        # Hero Image (if available)
        if "image" in metadata:
            lines.append(f"heroImage: \"{metadata['image']}\"")

        # Tags
        if "tags" in metadata and metadata["tags"]:
            if isinstance(metadata["tags"], list):
                tags_str = ", ".join(
                    [f'"{self._escape_yaml(str(t))}"' for t in metadata["tags"]]
                )
                lines.append(f"tags: [{tags_str}]")
            else:
                lines.append(f"tags: [\"{self._escape_yaml(str(metadata['tags']))}\"]")

        # Categories (as additional tags or custom field)
        if "categories" in metadata and metadata["categories"]:
            if isinstance(metadata["categories"], list):
                cats_str = ", ".join(
                    [f'"{self._escape_yaml(str(c))}"' for c in metadata["categories"]]
                )
                lines.append(f"categories: [{cats_str}]")
            else:
                lines.append(
                    f"categories: [\"{self._escape_yaml(str(metadata['categories']))}\"]"
                )

        # Draft status
        if "status" in metadata:
            draft = metadata["status"] != "publish"
            lines.append(f"draft: {str(draft).lower()}")
        else:
            lines.append("draft: false")

        lines.append("---")
        return "\n".join(lines)

    def _escape_yaml(self, text: str) -> str:
        """Escape special characters for YAML."""
        if not isinstance(text, str):
            text = str(text)
        # Escape quotes
        text = text.replace('"', '\\"')
        # Remove control characters
        text = re.sub(r"[\x00-\x1f\x7f]", "", text)
        return text

    def _format_date(self, date_value: Any) -> str:
        """Format date value to ISO format."""
        if isinstance(date_value, str):
            # Check if it's already ISO format
            if "T" in date_value or re.match(r"^\d{4}-\d{2}-\d{2}", date_value):
                return date_value
            # Return as-is if we can't parse it
            return date_value
        elif isinstance(date_value, datetime):
            return date_value.isoformat()
        else:
            return str(date_value)

    def _generate_slug(self, title: str) -> str:
        """Generate URL-friendly slug from title."""
        slug = title.lower()
        slug = re.sub(r"[^\w\s-]", "", slug)
        slug = re.sub(r"[\s_]+", "-", slug)
        slug = slug.strip("-")
        return slug

    def extract_metadata_from_markdown(self, markdown_content: str) -> dict[str, Any]:
        """Extract existing frontmatter metadata from markdown content."""
        metadata = {}

        # Check if content has frontmatter
        if markdown_content.startswith("---"):
            parts = markdown_content.split("---", 2)
            if len(parts) >= 3:
                frontmatter_text = parts[1].strip()
                try:
                    # Use proper YAML parsing to handle complex structures
                    metadata = yaml.safe_load(frontmatter_text)
                    if not isinstance(metadata, dict):
                        metadata = {}
                except yaml.YAMLError:
                    # Fallback to simple parsing if YAML parsing fails
                    for line in frontmatter_text.split("\n"):
                        if ":" in line and not line.strip().startswith("-"):
                            key, value = line.split(":", 1)
                            key = key.strip()
                            value = value.strip().strip('"').strip("'")
                            metadata[key] = value

        return metadata
