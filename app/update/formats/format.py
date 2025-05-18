from typing import List

from ..ecosystems.ecosystem import Badge


class Format:
    """Base format class for README files."""

    def __init__(self, name: str, extension: str):
        self.name = name
        self.extension = extension

    def render_badge(self, badge: Badge) -> str:
        """Render a badge in this format."""
        raise NotImplementedError("Subclasses must implement render_badge")

    def join_badges(self, badge_strings: List[str]) -> str:
        """Join multiple badge strings together."""
        raise NotImplementedError("Subclasses must implement join_badges")

    def find_insertion_point(self, content_lines: List[str]) -> int:
        """Find the appropriate insertion point in the content."""
        raise NotImplementedError("Subclasses must implement find_insertion_point")

    def modify_content(self, content: str, badges: List[Badge]) -> str:
        """Modify the content to include the badges."""
        # Filter out badges that already exist in the content
        new_badges = [badge for badge in badges if badge.image_url not in content]

        if len(new_badges) == 0:
            return content

        rendered_badges = [self.render_badge(badge) for badge in new_badges]
        badge_line = self.join_badges(rendered_badges)

        lines = content.split("\n")
        insert_index = self.find_insertion_point(lines)

        lines.insert(insert_index, badge_line)

        # Ensure there's a newline after the inserted badges
        if lines[insert_index + 1] != "":
            lines.insert(insert_index + 1, "")

        # Ensure there's a newline before the badges
        if insert_index and lines[insert_index - 1] != "":
            lines.insert(insert_index, "")

        return "\n".join(lines)
