import logging
import os
from pathlib import Path
from typing import List, Optional

from .ecosystems.cargo import Cargo
from .ecosystems.ecosystem import Ecosystem, Package
from .ecosystems.npm import NPM
from .ecosystems.pypi import PyPI
from .formats.md import MDFormat
from .formats.rst import RSTFormat

ecosystems = [
    NPM(),
    Cargo(),
    PyPI(),
]

formats = [
    MDFormat(),
    RSTFormat(),
]


def update(folder: str) -> List[Package]:
    """
    Find all packages inside the given folder for all supported package managers
    and edit their READMEs to add badges related to package manager.

    Args:
        folder: The root folder to search in
    """
    changed_packages = []

    # Walk through the directory structure
    for root, _, files in os.walk(folder):
        # Check each ecosystem
        for eco in ecosystems:
            if not eco.detect(files):
                continue

            manifest_path = Path(root) / eco.manifest_file
            package_info = eco.parse(root, manifest_path)

            if not package_info:
                continue

            readme_path = find_readme(root, files)

            if readme_path and modify_readme(eco, package_info, readme_path):
                changed_packages.append(package_info)

    return changed_packages


def find_readme(directory: str, files: List[str]) -> Optional[Path]:
    """Find a README file in the given directory."""
    readme_candidates = ["readme.md", "readme.rst"]

    # Use next with generator expression to find the first matching file
    matching_file = next(
        (file for file in files if file.lower() in readme_candidates), None
    )

    return Path(directory) / matching_file if matching_file else None


def modify_readme(ecosystem: Ecosystem, package: Package, readme_path: Path) -> bool:
    is_changed = False

    try:
        with open(readme_path, "r") as f:
            content = f.read()

        # Get badges from the ecosystem
        badges = ecosystem.badges(package)

        # Get the format handler based on file extension
        file_ext = readme_path.suffix.lower()
        format_handler = next(
            (fmt for fmt in formats if fmt.extension == file_ext), None
        )

        if not format_handler:
            raise ValueError(f"Unsupported README format {file_ext}")

        # Use the format handler to modify the content with badges
        new_content = format_handler.modify_content(content, badges)

        # Update the is_changed flag if content has changed
        is_changed = new_content != content

        # Write the updated content back to the file
        with open(readme_path, "w") as f:
            f.write(new_content)

    except Exception as e:
        logging.error(
            f"Error updating README: {e}",
            extra={
                "package": package.name,
                "ecosystem": ecosystem.name,
                "readme": readme_path,
            },
        )

    return is_changed
