from pathlib import Path
from unittest.mock import patch

import pytest
from automa.bot import CodeFolder
from automa.bot.webhook import generate_webhook_signature

from app.env import env

fixtures = Path(__file__).parent / "fixtures"
fixture_code = CodeFolder(fixtures / "code")


def call_with_fixture(client, filename):
    fixture = open(fixtures / filename, "r").read()

    signature = generate_webhook_signature(env().automa_webhook_secret, fixture)

    return client.post(
        "/hooks/automa",
        content=fixture.encode(),
        headers={
            "webhook-signature": signature,
            "x-automa-server-host": "https://api.automa.app",
        },
    )


@pytest.mark.parametrize(
    "signature",
    [
        ("invalid"),
        (None),
    ],
)
def test_invalid_signature(client, signature):
    """Test the Automa webhook endpoint with different invalid signature scenarios."""

    headers = {}

    if signature:
        headers["webhook-signature"] = signature

    response = client.post(
        "/hooks/automa",
        content=b'{ "id": "whmsg_1", "timestamp": "2025-05-30T09:30:06.261Z" }',
        headers=headers,
    )

    assert response.status_code == 401


@patch("automa.bot.AsyncCodeResource.cleanup")
@patch("automa.bot.AsyncCodeResource.propose")
@patch("automa.bot.AsyncCodeResource.download", return_value=fixture_code)
def test_valid_signature(download_mock, propose_mock, cleanup_mock, client):
    """Test the Automa webhook endpoint with a valid signature."""

    response = call_with_fixture(client, "task.json")

    # Returns 200 OK
    assert response.status_code == 200

    # Has empty body
    assert response.content == b""

    # Downloads the code
    download_mock.assert_called_once_with(
        {
            "task": {
                "id": 1,
                "token": "abcdef",
                "title": "Running package-badges on monorepo",
            }
        }
    )

    # Proposes the code
    propose_mock.assert_called_once_with(
        {
            "task": {
                "id": 1,
                "token": "abcdef",
                "title": "Running package-badges on monorepo",
            },
            "proposal": {"title": "Added package badges"},
        }
    )

    # Cleans up the code
    cleanup_mock.assert_called_once_with(
        {
            "task": {
                "id": 1,
                "token": "abcdef",
                "title": "Running package-badges on monorepo",
            }
        }
    )


@patch("automa.bot.AsyncCodeResource.cleanup")
@patch("automa.bot.AsyncCodeResource.propose")
@patch("automa.bot.AsyncCodeResource.download", side_effect=Exception("Download error"))
def test_download_error(download_mock, propose_mock, cleanup_mock, client):
    """Test the Automa webhook endpoint with a download error."""

    with pytest.raises(Exception):
        response = call_with_fixture(client, "task.json")

        # Returns 500 Internal Server Error
        assert response.status_code == 500

    # Downsloads the code
    download_mock.assert_called_once_with(
        {
            "task": {
                "id": 1,
                "token": "abcdef",
                "title": "Running package-badges on monorepo",
            }
        }
    )

    # Does not propose the code
    propose_mock.assert_not_called()

    # Does not clean up the code
    cleanup_mock.assert_not_called()


@patch("automa.bot.AsyncCodeResource.cleanup")
@patch("automa.bot.AsyncCodeResource.propose", side_effect=Exception("Propose error"))
@patch("automa.bot.AsyncCodeResource.download", return_value=fixture_code)
def test_propose_error(download_mock, propose_mock, cleanup_mock, client):
    """Test the Automa webhook endpoint with a propose error."""

    with pytest.raises(Exception):
        response = call_with_fixture(client, "task.json")

        # Returns 500 Internal Server Error
        assert response.status_code == 500

    # Downloads the code
    download_mock.assert_called_once_with(
        {
            "task": {
                "id": 1,
                "token": "abcdef",
                "title": "Running package-badges on monorepo",
            }
        }
    )

    # Proposes the code
    propose_mock.assert_called_once_with(
        {
            "task": {
                "id": 1,
                "token": "abcdef",
                "title": "Running package-badges on monorepo",
            },
            "proposal": {"title": "Added package badges"},
        }
    )

    # Cleans up the code
    cleanup_mock.assert_called_once_with(
        {
            "task": {
                "id": 1,
                "token": "abcdef",
                "title": "Running package-badges on monorepo",
            }
        }
    )
