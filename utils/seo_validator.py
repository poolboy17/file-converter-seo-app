from bs4 import BeautifulSoup


class SEOValidator:
    """Validate and score HTML content for SEO best practices."""

    def __init__(self):
        self.issues = []
        self.warnings = []
        self.successes = []
        self.score = 100

    def validate(self, html_content: str, title: str | None = None) -> dict:
        """
        Validate HTML content for SEO best practices.

        Args:
            html_content: HTML string to validate
            title: Optional title for context

        Returns:
            Dict with score, issues, warnings, and recommendations
        """
        self.issues = []
        self.warnings = []
        self.successes = []
        self.score = 100

        soup = BeautifulSoup(html_content, "html.parser")

        # Run all validation checks
        self._check_title_tag(soup)
        self._check_meta_description(soup)
        self._check_heading_structure(soup)
        self._check_images(soup)
        self._check_links(soup)
        self._check_content_length(soup)
        self._check_open_graph(soup)
        self._check_structured_data(soup)
        self._check_semantic_html(soup)

        return {
            "score": max(0, self.score),
            "issues": self.issues,
            "warnings": self.warnings,
            "successes": self.successes,
            "recommendations": self._generate_recommendations(),
        }

    def _check_title_tag(self, soup):
        """Check title tag presence and quality."""
        title = soup.find("title")

        if not title:
            self.issues.append("Missing <title> tag")
            self.score -= 15
        elif not title.string or not title.string.strip():
            self.issues.append("Empty <title> tag")
            self.score -= 15
        else:
            title_text = title.string.strip()
            title_length = len(title_text)

            if title_length < 30:
                self.warnings.append(
                    f"Title too short ({title_length} chars, recommend 30-60)"
                )
                self.score -= 5
            elif title_length > 60:
                self.warnings.append(
                    f"Title too long ({title_length} chars, recommend 30-60)"
                )
                self.score -= 3
            else:
                self.successes.append(f"Title length is optimal ({title_length} chars)")

    def _check_meta_description(self, soup):
        """Check meta description presence and quality."""
        meta_desc = soup.find("meta", {"name": "description"})

        if not meta_desc or not meta_desc.get("content"):
            self.issues.append("Missing meta description")
            self.score -= 10
        else:
            desc_text = meta_desc.get("content", "").strip()
            desc_length = len(desc_text)

            if desc_length < 50:
                self.warnings.append(
                    f"Meta description too short ({desc_length} chars, recommend 120-160)"  # noqa: E501
                )
                self.score -= 5
            elif desc_length > 160:
                self.warnings.append(
                    f"Meta description too long ({desc_length} chars, recommend 120-160)"  # noqa: E501
                )
                self.score -= 3
            else:
                self.successes.append(
                    f"Meta description length is optimal ({desc_length} chars)"
                )

    def _check_heading_structure(self, soup):
        """Check heading hierarchy and structure."""
        h1_tags = soup.find_all("h1")

        if len(h1_tags) == 0:
            self.issues.append("No H1 heading found")
            self.score -= 10
        elif len(h1_tags) > 1:
            self.warnings.append(
                f"Multiple H1 tags found ({len(h1_tags)}), should have only one"
            )
            self.score -= 5
        else:
            h1_text = h1_tags[0].get_text().strip()
            if len(h1_text) < 20:
                self.warnings.append(f"H1 is short ({len(h1_text)} chars)")
                self.score -= 2
            else:
                self.successes.append("H1 heading is properly structured")

        # Check heading hierarchy
        headings = []
        for level in range(1, 7):
            tags = soup.find_all(f"h{level}")
            for tag in tags:
                headings.append((level, tag.get_text().strip()))

        # Verify no heading levels are skipped
        if headings:
            prev_level = 0
            for level, _ in headings:  # text not used, just checking hierarchy
                if level > prev_level + 1 and prev_level > 0:
                    self.warnings.append(
                        f"Heading hierarchy skips level (H{prev_level} to H{level})"
                    )
                    self.score -= 2
                    break
                prev_level = level

    def _check_images(self, soup):
        """Check images for alt text and optimization."""
        images = soup.find_all("img")

        if not images:
            return

        missing_alt = 0
        empty_alt = 0
        good_alt = 0

        for img in images:
            alt = img.get("alt")
            if alt is None:
                missing_alt += 1
            elif not alt.strip() or len(alt.strip()) < 5:
                empty_alt += 1
            else:
                good_alt += 1

        if missing_alt > 0:
            self.issues.append(f"{missing_alt} image(s) missing alt text")
            self.score -= min(10, missing_alt * 2)

        if empty_alt > 0:
            self.warnings.append(
                f"{empty_alt} image(s) with empty or very short alt text"
            )
            self.score -= min(5, empty_alt)

        if good_alt > 0:
            self.successes.append(f"{good_alt} image(s) have proper alt text")

    def _check_links(self, soup):
        """Check internal and external links."""
        links = soup.find_all("a", href=True)

        if not links:
            self.warnings.append("No links found in content")
            self.score -= 3
            return

        internal_links = 0
        external_links = 0

        for link in links:
            href = link.get("href", "")

            if not href or href.startswith("#"):
                continue
            elif href.startswith("http"):
                external_links += 1
                # Check if external links have rel="noopener" for security
                if not link.get("rel"):
                    self.warnings.append(
                        "External links should have rel='noopener' or rel='nofollow'"
                    )
                    self.score -= 1
            else:
                internal_links += 1

        if external_links > 0:
            self.successes.append(f"Found {external_links} external link(s)")
        if internal_links > 0:
            self.successes.append(f"Found {internal_links} internal link(s)")

    def _check_content_length(self, soup):
        """Check content length for SEO."""
        # Extract text content
        text = soup.get_text()
        words = len(text.split())

        if words < 300:
            self.warnings.append(f"Content is short ({words} words, recommend 300+)")
            self.score -= 5
        elif words > 2000:
            self.successes.append(f"Good content length ({words} words)")
        else:
            self.successes.append(f"Adequate content length ({words} words)")

    def _check_open_graph(self, soup):
        """Check Open Graph tags for social sharing."""
        og_tags = {
            "og:title": soup.find("meta", property="og:title"),
            "og:description": soup.find("meta", property="og:description"),
            "og:image": soup.find("meta", property="og:image"),
            "og:url": soup.find("meta", property="og:url"),
            "og:type": soup.find("meta", property="og:type"),
        }

        missing_og = [tag for tag, element in og_tags.items() if not element]

        if len(missing_og) == 5:
            self.warnings.append(
                "No Open Graph tags found (important for social sharing)"
            )
            self.score -= 5
        elif missing_og:
            self.warnings.append(f"Missing Open Graph tags: {', '.join(missing_og)}")
            self.score -= 2
        else:
            self.successes.append("All essential Open Graph tags present")

    def _check_structured_data(self, soup):
        """Check for structured data (Schema.org)."""
        json_ld = soup.find_all("script", type="application/ld+json")
        microdata = soup.find_all(attrs={"itemscope": True})

        if not json_ld and not microdata:
            self.warnings.append("No structured data (Schema.org) found")
            self.score -= 3
        else:
            self.successes.append("Structured data present")

    def _check_semantic_html(self, soup):
        """Check for semantic HTML5 elements."""
        semantic_tags = [
            "article",
            "section",
            "nav",
            "aside",
            "header",
            "footer",
            "main",
        ]
        found_tags = [tag for tag in semantic_tags if soup.find(tag)]

        if len(found_tags) == 0:
            self.warnings.append(
                "No semantic HTML5 tags found (article, section, etc.)"
            )
            self.score -= 3
        else:
            self.successes.append(f"Using semantic HTML5 tags: {', '.join(found_tags)}")

    def _generate_recommendations(self) -> list[str]:
        """Generate actionable recommendations based on issues."""
        recommendations = []

        if any("title" in issue.lower() for issue in self.issues):
            recommendations.append("Add a descriptive title tag (30-60 characters)")

        if any("meta description" in issue.lower() for issue in self.issues):
            recommendations.append("Add a meta description (120-160 characters)")

        if any("H1" in str(self.issues) for _ in self.issues):
            recommendations.append("Add a single H1 heading to the page")

        if any("alt text" in issue.lower() for issue in self.issues):
            recommendations.append("Add descriptive alt text to all images")

        if any("Open Graph" in str(self.warnings) for _ in self.warnings):
            recommendations.append(
                "Add Open Graph tags for better social media sharing"
            )

        if any("structured data" in warning.lower() for warning in self.warnings):
            recommendations.append("Add Schema.org structured data for rich snippets")

        if any("semantic" in warning.lower() for warning in self.warnings):
            recommendations.append(
                "Use semantic HTML5 tags (article, section, header, etc.)"
            )

        return recommendations


def get_seo_grade(score: int) -> str:
    """Convert SEO score to letter grade."""
    if score >= 90:
        return "A"
    elif score >= 80:
        return "B"
    elif score >= 70:
        return "C"
    elif score >= 60:
        return "D"
    else:
        return "F"
