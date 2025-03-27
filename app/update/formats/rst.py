from typing import List

from ..ecosystems.ecosystem import Badge
from .format import Format


class RSTFormat(Format):
    """reStructuredText format implementation."""

    def __init__(self):
        super().__init__("reStructuredText", ".rst")

    def render_badge(self, badge: Badge) -> str:
        """Render the badge in reStructuredText format."""
        return f".. image:: {badge.image_url}\n   :target: {badge.link_url}\n   :alt: {badge.title}"

    def join_badges(self, badge_strings: List[str]) -> str:
        """Join badges with double newlines for proper separation."""
        return "\n\n".join(badge_strings)

    def find_insertion_point(self, content_lines: List[str]) -> int:
        """Find where to insert badges - after the title underline."""
        # Default after potential title underline
        insert_index = 2

        # Look for title underline pattern in first few lines
        for i in range(1, min(5, len(content_lines))):
            if all(c == "=" for c in content_lines[i]) or all(
                c == "-" for c in content_lines[i]
            ):
                insert_index = i + 1
                break

        return insert_index
