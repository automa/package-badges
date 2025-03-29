import os
import shutil
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Dict

import pytest
from syrupy.assertion import SnapshotAssertion

from app.update.update import update


@pytest.fixture
def temp_dir():
    """Create a temporary directory for testing."""
    with TemporaryDirectory() as dir_path:
        yield dir_path


def run_fixture(
    temp_dir: TemporaryDirectory[str], fixture_name: str, snapshot: SnapshotAssertion
) -> None:
    """Run test on a specific fixture."""
    # Setup the fixture
    source = Path(__file__).parent / "fixtures" / fixture_name
    fixture_dir = Path(temp_dir) / fixture_name

    if os.path.isdir(source):
        shutil.copytree(source, fixture_dir)

    # Run the update function
    update(fixture_dir)

    result: Dict[str, str] = {}

    for root, _, files in os.walk(fixture_dir):
        for file in files:
            file_path = Path(root) / file

            with open(file_path, "r") as f:
                content = f.read()
                rel_path = file_path.relative_to(fixture_dir)
                result[str(rel_path)] = content

    assert result == snapshot


def test_empty(temp_dir: TemporaryDirectory[str], snapshot: SnapshotAssertion):
    run_fixture(temp_dir, "empty", snapshot)


def test_no_readme(temp_dir: TemporaryDirectory[str], snapshot: SnapshotAssertion):
    run_fixture(temp_dir, "no_readme", snapshot)


def test_npm(temp_dir: TemporaryDirectory[str], snapshot: SnapshotAssertion):
    run_fixture(temp_dir, "npm", snapshot)


def test_npm_private(temp_dir: TemporaryDirectory[str], snapshot: SnapshotAssertion):
    run_fixture(temp_dir, "npm_private", snapshot)


def test_monorepo(temp_dir: TemporaryDirectory[str], snapshot: SnapshotAssertion):
    run_fixture(temp_dir, "monorepo", snapshot)
