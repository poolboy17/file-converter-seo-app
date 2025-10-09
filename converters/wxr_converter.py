import re
import xml.etree.ElementTree as ET
from datetime import datetime
from typing import Dict, List

from bs4 import BeautifulSoup


class WxrConverter:
    """Converter for WordPress WXR (export) files to markdown format."""

    def __init__(self):
        self.image_handler = None
        self.downloaded_images = {}  # Map: original_url -> local_filename

    def convert(self, file, include_metadata=True, image_handler=None):
        """
        Convert WXR file to markdown.

        Args:
            file: Streamlit uploaded file object
            include_metadata: Whether to include post metadata
            image_handler: Optional ImageHandler instance for downloading images

        Returns:
            str: Markdown content
        """
        try:
            self.image_handler = image_handler
            self.downloaded_images = {}

            # Read and parse XML content
            content = file.read().decode("utf-8", errors="replace")

            # Parse the WXR content
            posts = self._parse_wxr_content(content)

            markdown_lines = []

            # Add overall metadata if requested
            if include_metadata:
                markdown_lines.extend(self._extract_site_metadata(content, file.name))
                markdown_lines.append("")

            # Process each post/page
            for i, post in enumerate(posts):
                if i > 0:
                    markdown_lines.append("\n---\n")  # Separator between posts

                post_markdown = self._convert_post_to_markdown(post, include_metadata)
                markdown_lines.extend(post_markdown)

            return "\n".join(markdown_lines)

        except Exception as e:
            raise Exception(f"Error converting WXR file: {str(e)}")

    def _parse_wxr_content(self, content):
        """Parse WXR XML content and extract posts."""
        posts = []

        try:
            # Clean up the XML content
            content = self._clean_xml_content(content)

            # Parse XML
            root = ET.fromstring(content)

            # Define namespaces
            namespaces = {
                "wp": "http://wordpress.org/export/1.2/",
                "content": "http://purl.org/rss/1.0/modules/content/",
                "excerpt": "http://wordpress.org/export/1.2/excerpt/",
                "dc": "http://purl.org/dc/elements/1.1/",
            }

            # Find all items (posts/pages)
            items = root.findall(".//item")

            for item in items:
                post_data = self._extract_post_data(item, namespaces)
                if post_data and post_data.get("content"):
                    posts.append(post_data)

        except ET.ParseError as e:
            # If XML parsing fails, try to extract content using regex
            posts = self._parse_wxr_with_regex(content)

        return posts

    def _clean_xml_content(self, content):
        """Clean XML content to handle common issues."""
        # Remove or replace problematic characters
        content = re.sub(r"[\x00-\x08\x0B\x0C\x0E-\x1F\x7F]", "", content)

        # Fix common encoding issues
        content = content.replace("&", "&amp;")
        content = re.sub(r"&amp;(amp|lt|gt|quot|apos);", r"&\1;", content)

        return content

    def _extract_post_data(self, item, namespaces):
        """Extract post data from XML item."""
        post_data = {}

        # Basic fields
        title_elem = item.find("title")
        post_data["title"] = title_elem.text if title_elem is not None else "Untitled"

        link_elem = item.find("link")
        post_data["link"] = link_elem.text if link_elem is not None else ""

        # WordPress specific fields
        post_type_elem = item.find("wp:post_type", namespaces)
        post_data["post_type"] = (
            post_type_elem.text if post_type_elem is not None else "post"
        )

        post_status_elem = item.find("wp:status", namespaces)
        post_data["status"] = (
            post_status_elem.text if post_status_elem is not None else "publish"
        )

        post_date_elem = item.find("wp:post_date", namespaces)
        post_data["date"] = post_date_elem.text if post_date_elem is not None else ""

        # Content
        content_elem = item.find("content:encoded", namespaces)
        post_data["content"] = content_elem.text if content_elem is not None else ""

        # Excerpt
        excerpt_elem = item.find("excerpt:encoded", namespaces)
        post_data["excerpt"] = excerpt_elem.text if excerpt_elem is not None else ""

        # Author
        author_elem = item.find("dc:creator", namespaces)
        post_data["author"] = author_elem.text if author_elem is not None else ""

        # Categories and tags
        post_data["categories"] = []
        post_data["tags"] = []

        categories = item.findall("category")
        for cat in categories:
            domain = cat.get("domain", "")
            if domain == "category":
                post_data["categories"].append(cat.text)
            elif domain == "post_tag":
                post_data["tags"].append(cat.text)

        return post_data

    def _parse_wxr_with_regex(self, content):
        """Fallback method to parse WXR using regex when XML parsing fails."""
        posts = []

        # Find all items using regex
        item_pattern = r"<item>(.*?)</item>"
        items = re.findall(item_pattern, content, re.DOTALL)

        for item_content in items:
            post_data = {}

            # Extract title
            title_match = re.search(r"<title>(.*?)</title>", item_content, re.DOTALL)
            post_data["title"] = title_match.group(1) if title_match else "Untitled"

            # Extract content
            content_match = re.search(
                r"<content:encoded><!\[CDATA\[(.*?)\]\]></content:encoded>",
                item_content,
                re.DOTALL,
            )
            post_data["content"] = content_match.group(1) if content_match else ""

            # Extract other fields
            date_match = re.search(r"<wp:post_date>(.*?)</wp:post_date>", item_content)
            post_data["date"] = date_match.group(1) if date_match else ""

            author_match = re.search(
                r"<dc:creator><!\[CDATA\[(.*?)\]\]></dc:creator>", item_content
            )
            post_data["author"] = author_match.group(1) if author_match else ""

            if post_data.get("content"):
                posts.append(post_data)

        return posts

    def _extract_site_metadata(self, content, filename):
        """Extract site-level metadata from WXR."""
        metadata = [
            "---",
            f'title: "WordPress Export - {filename}"',
            f'source_format: "WXR"',
            f'export_date: "{datetime.now().isoformat()}"',
        ]

        # Try to extract site info
        site_title_match = re.search(r"<title>(.*?)</title>", content)
        if site_title_match:
            metadata.append(f'site_title: "{site_title_match.group(1)}"')

        site_url_match = re.search(r"<link>(.*?)</link>", content)
        if site_url_match:
            metadata.append(f'site_url: "{site_url_match.group(1)}"')

        # Count posts
        post_count = len(re.findall(r"<wp:post_type>post</wp:post_type>", content))
        page_count = len(re.findall(r"<wp:post_type>page</wp:post_type>", content))

        metadata.append(f"posts: {post_count}")
        metadata.append(f"pages: {page_count}")
        metadata.append("---")

        return metadata

    def _convert_post_to_markdown(self, post, include_metadata=True):
        """Convert a single post to markdown."""
        markdown_lines = []

        # Add post metadata
        if include_metadata:
            markdown_lines.append("---")
            markdown_lines.append(f"title: \"{post.get('title', 'Untitled')}\"")

            if post.get("date"):
                markdown_lines.append(f"date: \"{post['date']}\"")

            if post.get("author"):
                markdown_lines.append(f"author: \"{post['author']}\"")

            if post.get("post_type"):
                markdown_lines.append(f"type: \"{post['post_type']}\"")

            if post.get("status"):
                markdown_lines.append(f"status: \"{post['status']}\"")

            if post.get("categories"):
                markdown_lines.append(f"categories: {post['categories']}")

            if post.get("tags"):
                markdown_lines.append(f"tags: {post['tags']}")

            if post.get("link"):
                markdown_lines.append(f"original_url: \"{post['link']}\"")

            markdown_lines.append("---")
            markdown_lines.append("")

        # Add title as heading
        markdown_lines.append(f"# {post.get('title', 'Untitled')}")
        markdown_lines.append("")

        # Add excerpt if available
        if post.get("excerpt") and post["excerpt"].strip():
            excerpt_text = self._html_to_markdown(post["excerpt"])
            markdown_lines.append("*" + excerpt_text.strip() + "*")
            markdown_lines.append("")

        # Convert content from HTML to markdown
        if post.get("content"):
            content_markdown = self._html_to_markdown(post["content"])
            markdown_lines.append(content_markdown)

        return markdown_lines

    def _html_to_markdown(self, html_content):
        """Convert HTML content to markdown."""
        if not html_content:
            return ""

        # Use BeautifulSoup to parse HTML
        soup = BeautifulSoup(html_content, "html.parser")

        # Convert common HTML elements to markdown
        markdown_content = self._convert_html_elements(soup)

        # Clean up the markdown
        markdown_content = self._clean_markdown(markdown_content)

        return markdown_content

    def _convert_html_elements(self, soup):
        """Convert HTML elements to markdown equivalents."""
        # Convert headers
        for i in range(1, 7):
            for heading in soup.find_all(f"h{i}"):
                heading.replace_with(f"{'#' * i} {heading.get_text().strip()}\n\n")

        # Convert paragraphs
        for p in soup.find_all("p"):
            p.replace_with(f"{p.get_text().strip()}\n\n")

        # Convert links
        for link in soup.find_all("a"):
            href = link.get("href", "")
            text = link.get_text().strip()
            if href and text:
                link.replace_with(f"[{text}]({href})")
            else:
                link.replace_with(text)

        # Convert images
        for img in soup.find_all("img"):
            src = img.get("src", "")
            alt = img.get("alt", "Image")
            if src:
                # Download image if handler is available
                local_src = self._download_image_if_needed(src)
                img.replace_with(f"![{alt}]({local_src})\n\n")

        # Convert lists
        for ul in soup.find_all("ul"):
            list_items = []
            for li in ul.find_all("li"):
                list_items.append(f"- {li.get_text().strip()}")
            ul.replace_with("\n".join(list_items) + "\n\n")

        for ol in soup.find_all("ol"):
            list_items = []
            for i, li in enumerate(ol.find_all("li"), 1):
                list_items.append(f"{i}. {li.get_text().strip()}")
            ol.replace_with("\n".join(list_items) + "\n\n")

        # Convert code blocks
        for pre in soup.find_all("pre"):
            code_content = pre.get_text()
            pre.replace_with(f"```\n{code_content}\n```\n\n")

        # Convert inline code
        for code in soup.find_all("code"):
            code.replace_with(f"`{code.get_text()}`")

        # Convert bold and italic
        for strong in soup.find_all(["strong", "b"]):
            strong.replace_with(f"**{strong.get_text()}**")

        for em in soup.find_all(["em", "i"]):
            em.replace_with(f"*{em.get_text()}*")

        # Convert blockquotes
        for blockquote in soup.find_all("blockquote"):
            quote_lines = blockquote.get_text().strip().split("\n")
            quote_markdown = "\n".join(f"> {line}" for line in quote_lines)
            blockquote.replace_with(f"{quote_markdown}\n\n")

        return soup.get_text()

    def _clean_markdown(self, content):
        """Clean up markdown content."""
        # Remove excessive whitespace
        content = re.sub(r"\n{3,}", "\n\n", content)

        # Remove leading/trailing whitespace
        content = content.strip()

        # Fix spacing around headers
        content = re.sub(r"\n(#{1,6}\s+.*?)\n", r"\n\n\1\n\n", content)

        return content

    def _download_image_if_needed(self, url):
        """Download an image if handler is available, otherwise return original URL."""
        if not self.image_handler:
            return url

        # Check if already downloaded
        if url in self.downloaded_images:
            return f"assets/{self.downloaded_images[url]}"

        # Try to download the image
        result = self.image_handler.download_image(url)
        if result:
            image_data, ext = result
            # Optimize and save
            optimized_data, ext = self.image_handler.optimize_image(image_data)
            filename = self.image_handler.save_image(
                optimized_data, ext, prefix="wxr_img"
            )

            # Store mapping
            self.downloaded_images[url] = filename
            return f"assets/{filename}"

        # If download failed, return original URL
        return url
