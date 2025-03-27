from pathlib import Path
from typing import List, Optional


class Package:
    """Package information."""

    def __init__(self, path: str, name: str, version: str):
        self.path = path
        self.name = name
        self.version = version


class Badge:
    """Badge information."""

    def __init__(self, title: str, image_url: str, link_url: str):
        self.title = title
        self.image_url = image_url
        self.link_url = link_url


class Ecosystem:
    """Base class for package managers."""

    def __init__(self, name: str, manifest_file: str):
        self.name = name
        self.manifest_file = manifest_file

    def detect(self, files: List[str]) -> bool:
        """Check if the package manager is present in the files."""
        return self.manifest_file in files

    def parse(self, root: str, manifest_path: Path) -> Optional[Package]:
        """Parse the manifest file and return package info."""
        raise NotImplementedError("Subclasses must implement parse method")

    def badges(self, package: Package) -> List[Badge]:
        """
        Create a list of badges for the package.

        Args:
            package: The package to create badges for

        Returns:
            A list of badges
        """
        raise NotImplementedError("Subclasses must implement badges method")
