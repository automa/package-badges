import os
from pathlib import Path
from shutil import copytree
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


def run_fixture(temp_dir: str, fixture_name: str, snapshot: SnapshotAssertion) -> None:
    """Run test on a specific fixture."""
    # Setup the fixture
    source = Path(__file__).parent / "fixtures" / fixture_name
    fixture_dir = Path(temp_dir) / fixture_name

    if os.path.isdir(source):
        copytree(source, fixture_dir)

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


def test_empty(temp_dir: str, snapshot: SnapshotAssertion):
    run_fixture(temp_dir, "empty", snapshot)


def test_no_readme(temp_dir: str, snapshot: SnapshotAssertion):
    run_fixture(temp_dir, "no_readme", snapshot)


def test_npm(temp_dir: str, snapshot: SnapshotAssertion):
    run_fixture(temp_dir, "npm", snapshot)


def test_npm_private(temp_dir: str, snapshot: SnapshotAssertion):
    run_fixture(temp_dir, "npm_private", snapshot)


def test_cargo(temp_dir: str, snapshot: SnapshotAssertion):
    run_fixture(temp_dir, "cargo", snapshot)


def test_cargo_private(temp_dir: str, snapshot: SnapshotAssertion):
    run_fixture(temp_dir, "cargo_private", snapshot)


def test_cargo_publish_empty(temp_dir: str, snapshot: SnapshotAssertion):
    run_fixture(temp_dir, "cargo_publish_empty", snapshot)


def test_cargo_publish_crates_io(temp_dir: str, snapshot: SnapshotAssertion):
    run_fixture(temp_dir, "cargo_publish_crates_io", snapshot)


def test_cargo_publish_registry(temp_dir: str, snapshot: SnapshotAssertion):
    run_fixture(temp_dir, "cargo_publish_registry", snapshot)


def test_cargo_publish_both_registries(temp_dir: str, snapshot: SnapshotAssertion):
    run_fixture(temp_dir, "cargo_publish_both_registries", snapshot)


def test_pypi(temp_dir: str, snapshot: SnapshotAssertion):
    run_fixture(temp_dir, "pypi", snapshot)


def test_pypi_private(temp_dir: str, snapshot: SnapshotAssertion):
    run_fixture(temp_dir, "pypi_private", snapshot)


def test_monorepo(temp_dir: str, snapshot: SnapshotAssertion):
    run_fixture(temp_dir, "monorepo", snapshot)


def test_md_empty(temp_dir: str, snapshot: SnapshotAssertion):
    run_fixture(temp_dir, "md_empty", snapshot)


def test_md_no_heading(temp_dir: str, snapshot: SnapshotAssertion):
    run_fixture(temp_dir, "md_no_heading", snapshot)


def test_md_h3_heading(temp_dir: str, snapshot: SnapshotAssertion):
    run_fixture(temp_dir, "md_h3_heading", snapshot)


def test_rst(temp_dir: str, snapshot: SnapshotAssertion):
    run_fixture(temp_dir, "rst", snapshot)


def test_rst_empty(temp_dir: str, snapshot: SnapshotAssertion):
    run_fixture(temp_dir, "rst_empty", snapshot)


def test_rst_no_heading(temp_dir: str, snapshot: SnapshotAssertion):
    run_fixture(temp_dir, "rst_no_heading", snapshot)


def test_rst_h1_heading(temp_dir: str, snapshot: SnapshotAssertion):
    run_fixture(temp_dir, "rst_h1_heading", snapshot)


def test_rst_h3_heading(temp_dir: str, snapshot: SnapshotAssertion):
    run_fixture(temp_dir, "rst_h3_heading", snapshot)


def test_existing_badge(temp_dir: str, snapshot: SnapshotAssertion):
    run_fixture(temp_dir, "existing_badge", snapshot)
