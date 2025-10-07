from slack_bolt.adapter.starlette.async_handler import AsyncSlackRequestHandler
from starlette.applications import Starlette
from starlette.requests import Request
from starlette.responses import JSONResponse
from starlette.routing import Route

from app.__main__ import main
from app.utils.env import env
from app.utils.slack import app as slack_app

req_handler = AsyncSlackRequestHandler(slack_app)


async def endpoint(req: Request):
    return await req_handler.handle(req)


async def health(req: Request):
    try:
        await env.slack_client.api_test()
        slack_healthy = True
    except Exception:
        slack_healthy = False

    return JSONResponse(
        {
            "healthy": slack_healthy,
            "slack": slack_healthy,
        }
    )


app = Starlette(
    debug=True if env.environment != "production" else False,
    routes=[
        Route(path="/slack/events", endpoint=endpoint, methods=["POST"]),
        Route(path="/health", endpoint=health, methods=["GET"]),
    ],
    lifespan=main,
)
