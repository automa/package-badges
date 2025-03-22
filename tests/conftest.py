import sys
from os.path import abspath, dirname

# Add the project root to the Python path
sys.path.insert(0, abspath(dirname(dirname(__file__))))

import pytest
from fastapi.testclient import TestClient

from app.main import app


@pytest.fixture
def client():
    """Create a test client for the app."""
    with TestClient(app) as test_client:
        yield test_client
