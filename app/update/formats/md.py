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
        """Find where to insert badges - after the title."""
        for i, line in enumerate(content_lines):
            if line.startswith("# "):
                return i + 1
        return 0  # If no heading found, insert at the beginning
