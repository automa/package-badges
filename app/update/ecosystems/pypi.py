import logging
import tomllib
from pathlib import Path
from typing import List, Optional

from .ecosystem import Badge, Ecosystem, Package


class PyPI(Ecosystem):
    """Package manager PyPI for Python."""

    def __init__(self):
        super().__init__("pypi", "pyproject.toml")

    def _parse(self, root: str, manifest_path: Path) -> Optional[Package]:
        try:
            with open(manifest_path, "rb") as f:
                pyproject_data = tomllib.load(f)

            if not pyproject_data:
                return None

            # Check for project section
            project_section = pyproject_data.get("project")

            if not project_section:
                return None

            name = project_section.get("name")
            version = project_section.get("version")

            # Check classifiers for 'Private ::' or private indicator
            private = any(
                classifier.startswith("Private ::")
                for classifier in project_section.get("classifiers", [])
            )

            if name and version and not private:
                return Package(
                    path=root,
                    name=name,
                    version=version,
                )
        except (tomllib.TOMLDecodeError, IOError) as e:
            logging.info(f"Error reading {manifest_path}: {e}")

        return None

    def badges(self, package: Package) -> List[Badge]:
        """Create PyPI badges for the package."""
        name = package.name

        return [
            Badge(
                title="PyPI version",
                image_url=f"https://img.shields.io/pypi/v/{name}",
                link_url=f"https://pypi.org/project/{name}/",
            ),
            Badge(
                title="PyPI license",
                image_url=f"https://img.shields.io/pypi/l/{name}",
                link_url=f"https://pypi.org/project/{name}/",
            ),
            Badge(
                title="PyPI downloads",
                image_url=f"https://img.shields.io/pypi/dm/{name}",
                link_url=f"https://pypi.org/project/{name}/",
            ),
        ]
