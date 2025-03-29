import re
from typing import List

from ..ecosystems.ecosystem import Badge
from .format import Format


class MDFormat(Format):
    """Markdown format implementation."""

    def __init__(self):
        super().__init__("Markdown", ".md")

    def render_badge(self, badge: Badge) -> str:
        """Render the badge in Markdown format."""
        return f"[![{badge.title}]({badge.image_url})]({badge.link_url})"

    def join_badges(self, badge_strings: List[str]) -> str:
        """Join badges with a newline for better readability."""
        return "\n".join(badge_strings)

    def find_insertion_point(self, content_lines: List[str]) -> int:
        """
        Find where to insert badges - after the first heading of any level,
        or at the beginning if no heading is found.
        """
        # Regex pattern for Markdown headings: 1-6 # characters followed by a space and then text
        heading_pattern = re.compile(r"^(#{1,6})\s+(.+)$")

        for i, line in enumerate(content_lines):
            if heading_pattern.match(line.strip()):
                return i + 1

        return 0  # If no heading found, insert at the beginning
