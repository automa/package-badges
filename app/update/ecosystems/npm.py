import json
import logging
from pathlib import Path
from typing import List, Optional

from .ecosystem import Badge, Ecosystem, Package


class NPM(Ecosystem):
    """Package manager for Node.js."""

    def __init__(self):
        super().__init__("npm", "package.json")

    def parse(self, root: str, manifest_path: Path) -> Optional[Package]:
        try:
            with open(manifest_path, "r") as f:
                package_data = json.load(f)

            if not package_data:
                return None

            name = package_data.get("name")
            version = package_data.get("version")
            private = package_data.get("private")

            if name and version and not private:
                return Package(
                    path=root,
                    name=name,
                    version=version,
                )
        except (json.JSONDecodeError, IOError) as e:
            logging.info(f"Error reading {manifest_path}: {e}")

        return None

    def badges(self, package: Package) -> List[Badge]:
        """Create npm badges for the package."""
        name = package.name

        return [
            Badge(
                title="NPM version",
                image_url=f"https://img.shields.io/npm/v/{name}",
                link_url=f"https://www.npmjs.com/package/{name}",
            ),
            Badge(
                title="NPM downloads",
                image_url=f"https://img.shields.io/npm/dm/{name}",
                link_url=f"https://www.npmjs.com/package/{name}",
            ),
            Badge(
                title="NPM license",
                image_url=f"https://img.shields.io/npm/l/{name}",
                link_url=f"https://www.npmjs.com/package/{name}",
            ),
        ]
