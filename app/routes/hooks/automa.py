import json
import logging

from automa.bot import AsyncAutoma
from automa.bot.webhook import verify_webhook
from fastapi import APIRouter, Request, Response
from opentelemetry.semconv.attributes.http_attributes import (
    HTTP_REQUEST_HEADER_TEMPLATE,
)

from ...env import env
from ...update import update

router = APIRouter(tags=["automa"])


@router.post("")
async def automa_hook(request: Request):
    signature = request.headers.get("x-automa-signature")
    payload = (await request.body()).decode("utf-8")

    # Verify request
    if not verify_webhook(env().automa_webhook_secret, signature, payload):
        logging.warning(
            "Invalid signature",
            extra={
                "http.request.id": request.state.request_id,
                f"{HTTP_REQUEST_HEADER_TEMPLATE}.x-automa-signature": signature,
            },
        )

        return Response(status_code=401)

    base_url = request.headers.get("x-automa-server-host")
    body = json.loads(payload)

    # Create client with base URL
    automa = AsyncAutoma(base_url=base_url)

    # Download code
    folder = await automa.code.download(body)

    try:
        update(folder)

        # Propose code
        await automa.code.propose(
            {
                **body,
                "proposal": {
                    "message": "Added package badges",
                },
            }
        )
    finally:
        # Clean up
        await automa.code.cleanup(body)

    return Response(status_code=200)
