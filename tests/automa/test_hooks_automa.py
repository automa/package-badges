from pathlib import Path

import pytest
from automa.bot.webhook import generate_webhook_signature

from app.env import env


def call_with_fixture(client, filename):
    fixture = open(Path(__file__).parent / "fixtures" / filename, "r").read()

    signature = generate_webhook_signature(env().automa_webhook_secret, fixture)

    return client.post(
        "/hooks/automa",
        content=fixture.encode(),
        headers={
            "x-automa-server-host": "https://api.automa.app",
            "x-automa-signature": signature,
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
        headers["x-automa-signature"] = signature

    response = client.post("/hooks/automa", content=b"{}", headers=headers)

    assert response.status_code == 401


def test_valid_signature(client):
    """Test the Automa webhook endpoint with a valid signature."""

    response = call_with_fixture(client, "task.json")

    assert response.status_code == 200

    assert response.content == b""
