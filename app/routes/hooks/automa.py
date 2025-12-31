import json
import logging
from typing import List, cast

from automa.bot import AsyncAutoma, CodeProposeParams
from automa.bot.webhook import verify_webhook
from fastapi import APIRouter, Request, Response
from opentelemetry.semconv.attributes.http_attributes import (
    HTTP_REQUEST_HEADER_TEMPLATE,
)

from app.update.ecosystems.ecosystem import Package

from ...env import env
from ...update import update

router = APIRouter(tags=["automa"])


@router.post("")
async def automa_hook(request: Request):
    id = request.headers.get("webhook-id")
    signature = request.headers.get("webhook-signature")

    payload = (await request.body()).decode("utf-8")
    body = json.loads(payload)

    # Skip if not `task.created` event
    if "type" not in body or body["type"] != "task.created":
        return Response(status_code=204)

    # Verify request
    if signature is None or not verify_webhook(
        env().automa_webhook_secret, signature, payload
    ):
        logging.warning(
            "Invalid signature",
            extra={
                "http.request.id": request.state.request_id,
                f"{HTTP_REQUEST_HEADER_TEMPLATE}.webhook-id": id,
                f"{HTTP_REQUEST_HEADER_TEMPLATE}.webhook-signature": signature,
            },
        )

        return Response(status_code=401)

    base_url = request.headers.get("x-automa-server-host")

    # Create client with base URL
    automa = AsyncAutoma(base_url=base_url)

    # Download code
    folder = await automa.code.download(body["data"])

    try:
        changed_packages = update(folder.path)

        # Propose code
        await automa.code.propose(
            cast(
                CodeProposeParams,
                {
                    **body["data"],
                    "proposal": generate_pr_fields(changed_packages),
                },
            )
        )
    finally:
        # Clean up
        await automa.code.cleanup(body["data"])

    return Response(status_code=200)


def generate_pr_fields(changed_packages: List[Package]) -> dict:
    """Generate PR fields from changed packages."""
    title = "Added package badges"

    if len(changed_packages) == 1:
        title = f"Added package badges for `{changed_packages[0].name}`"

    result = {"title": title}

    if len(changed_packages):
        list = "\n".join(
            f"- `{pkg.name}` ({pkg.ecosystem})" for pkg in changed_packages
        )
        result["body"] = f"Added package badges for the following packages:\n\n{list}"

    return result
