import json
from datetime import datetime
from typing import Dict, List, Optional

from bs4 import BeautifulSoup


class SEOEnhancer:
    """Enhance HTML content with SEO optimizations."""

    def __init__(self):
        self.base_url = ""

    def enhance(
        self,
        html_content: str,
        title: str,
        description: str = None,
        keywords: List[str] = None,
        author: str = None,
        canonical_url: str = None,
    ) -> str:
        """
        Enhance HTML content with SEO optimizations.

        Args:
            html_content: Original HTML content
            title: Page title
            description: Meta description
            keywords: List of keywords
            author: Author name
            canonical_url: Canonical URL

        Returns:
            Enhanced HTML content
        """
        soup = BeautifulSoup(html_content, "html.parser")

        # Enhance head section
        self._enhance_meta_tags(
            soup, title, description, keywords, author, canonical_url
        )
        self._add_open_graph_tags(soup, title, description, canonical_url)
        self._add_twitter_cards(soup, title, description)
        self._add_structured_data(soup, title, description, author)

        # Enhance body content
        self._ensure_semantic_html(soup)
        self._enhance_images(soup)
        self._enhance_links(soup)

        return str(soup)

    def _enhance_meta_tags(
        self, soup, title, description, keywords, author, canonical_url
    ):
        """Add or enhance meta tags."""
        head = soup.find("head")
        if not head:
            head = soup.new_tag("head")
            if soup.html:
                soup.html.insert(0, head)

        # Title
        if not soup.find("title"):
            title_tag = soup.new_tag("title")
            title_tag.string = title
            head.append(title_tag)

        # Meta description
        if description and not soup.find("meta", {"name": "description"}):
            meta_desc = soup.new_tag(
                "meta", attrs={"name": "description", "content": description}
            )
            head.append(meta_desc)

        # Keywords
        if keywords and not soup.find("meta", {"name": "keywords"}):
            meta_keywords = soup.new_tag(
                "meta", attrs={"name": "keywords", "content": ", ".join(keywords)}
            )
            head.append(meta_keywords)

        # Author
        if author and not soup.find("meta", {"name": "author"}):
            meta_author = soup.new_tag(
                "meta", attrs={"name": "author", "content": author}
            )
            head.append(meta_author)

        # Viewport
        if not soup.find("meta", {"name": "viewport"}):
            meta_viewport = soup.new_tag(
                "meta",
                attrs={
                    "name": "viewport",
                    "content": "width=device-width, initial-scale=1.0",
                },
            )
            head.append(meta_viewport)

        # Charset
        if not soup.find("meta", charset=True):
            meta_charset = soup.new_tag("meta", charset="UTF-8")
            head.insert(0, meta_charset)

        # Canonical URL
        if canonical_url and not soup.find("link", {"rel": "canonical"}):
            canonical = soup.new_tag(
                "link", attrs={"rel": "canonical", "href": canonical_url}
            )
            head.append(canonical)

        # Robots meta
        if not soup.find("meta", {"name": "robots"}):
            meta_robots = soup.new_tag(
                "meta", attrs={"name": "robots", "content": "index, follow"}
            )
            head.append(meta_robots)

    def _add_open_graph_tags(self, soup, title, description, url):
        """Add Open Graph tags for social sharing."""
        head = soup.find("head")
        if not head:
            return

        og_tags = {
            "og:type": "article",
            "og:title": title,
            "og:description": description or title,
            "og:url": url or "",
            "og:site_name": title,
        }

        for property, content in og_tags.items():
            if content and not soup.find("meta", property=property):
                og_tag = soup.new_tag(
                    "meta", attrs={"property": property, "content": content}
                )
                head.append(og_tag)

    def _add_twitter_cards(self, soup, title, description):
        """Add Twitter Card tags."""
        head = soup.find("head")
        if not head:
            return

        twitter_tags = {
            "twitter:card": "summary_large_image",
            "twitter:title": title,
            "twitter:description": description or title,
        }

        for name, content in twitter_tags.items():
            if content and not soup.find("meta", {"name": name}):
                twitter_tag = soup.new_tag(
                    "meta", attrs={"name": name, "content": content}
                )
                head.append(twitter_tag)

    def _add_structured_data(self, soup, title, description, author):
        """Add Schema.org structured data as JSON-LD."""
        head = soup.find("head")
        if not head:
            return

        # Check if structured data already exists
        if soup.find("script", type="application/ld+json"):
            return

        structured_data = {
            "@context": "https://schema.org",
            "@type": "Article",
            "headline": title,
            "description": description or title,
            "author": {"@type": "Person", "name": author or "Unknown"},
            "datePublished": datetime.now().isoformat(),
            "dateModified": datetime.now().isoformat(),
        }

        script = soup.new_tag("script", type="application/ld+json")
        script.string = json.dumps(structured_data, indent=2)
        head.append(script)

    def _ensure_semantic_html(self, soup):
        """Wrap content in semantic HTML5 tags if not present."""
        body = soup.find("body")
        if not body:
            return

        # If there's no article tag, wrap main content in one
        if not soup.find("article"):
            # Find the main content div or create article wrapper
            main_content = body.find(["div", "main"])
            if main_content and not main_content.find_parent("article"):
                article = soup.new_tag("article")
                main_content.wrap(article)

    def _enhance_images(self, soup):
        """Enhance images with proper attributes."""
        images = soup.find_all("img")

        for img in images:
            # Add loading="lazy" for performance
            if not img.get("loading"):
                img["loading"] = "lazy"

            # Ensure alt text exists (add placeholder if missing)
            if not img.get("alt"):
                img["alt"] = "Image"

            # Add width and height if missing (helps with CLS)
            if not img.get("width"):
                img["width"] = "100%"

    def _enhance_links(self, soup):
        """Enhance links with proper attributes."""
        links = soup.find_all("a", href=True)

        for link in links:
            href = link.get("href", "")

            # Add rel="noopener" to external links
            if href.startswith("http"):
                rel = link.get("rel", [])
                if isinstance(rel, str):
                    rel = rel.split()
                if "noopener" not in rel:
                    rel.append("noopener")
                link["rel"] = " ".join(rel)

            # Ensure link text is descriptive (not "click here")
            link_text = link.get_text().strip().lower()
            if link_text in [
                "click here",
                "here",
                "link",
                "read more",
            ] and not link.get("aria-label"):
                link["aria-label"] = f"Link to {href}"
