import logging
import tomllib
from pathlib import Path
from typing import List, Optional

from .ecosystem import Badge, Ecosystem, Package


class Cargo(Ecosystem):
    """Package manager for Rust/Cargo."""

    def __init__(self):
        super().__init__("cargo", "Cargo.toml")

    def parse(self, root: str, manifest_path: Path) -> Optional[Package]:
        try:
            with open(manifest_path, "rb") as f:
                cargo_data = tomllib.load(f)

            if not cargo_data:
                return None

            package_section = cargo_data.get("package", {})

            # TODO: Having no version means private
            # TODO: Having non-standard publish means private
            # TODO: Having publish = false means private

            # Only process if it's a package, not just a workspace
            if package_section:
                return Package(
                    path=root,
                    name=package_section.get("name", ""),
                    version=package_section.get("version", ""),
                )
        except (tomllib.TOMLDecodeError, IOError) as e:
            logging.info(f"Error reading {manifest_path}: {e}")

        return None

    def badges(self, package: Package) -> List[Badge]:
        """Create cargo badges for the package."""
        name = package.name

        return [
            Badge(
                title="Crates.io version",
                image_url=f"https://img.shields.io/crates/v/{name}",
                link_url=f"https://crates.io/crates/{name}",
            ),
            Badge(
                title="Docs.rs documentation",
                image_url="https://img.shields.io/badge/docs.rs-latest-blue",
                link_url=f"https://docs.rs/{name}",
            ),
            Badge(
                title="Crates.io license",
                image_url=f"https://img.shields.io/crates/l/{name}",
                link_url=f"https://crates.io/crates/{name}",
            ),
        ]
