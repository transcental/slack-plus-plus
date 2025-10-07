import contextlib
import logging
from time import time

from aiohttp import ClientSession
from slack_bolt.async_app import AsyncApp
from slack_sdk.web.async_client import AsyncWebClient
from starlette.applications import Starlette

from slackpp.config import config
from slackpp.utils.logging import send_heartbeat

logger = logging.getLogger(__name__)


class Environment:
    slack_client: AsyncWebClient
    http: ClientSession
    app = AsyncApp(
        token=config.slack.bot_token, signing_secret=config.slack.signing_secret
    )

    @contextlib.asynccontextmanager
    async def enter(self, _app: Starlette):
        st = time()
        logger.debug("Entering environment context")
        self.http = ClientSession()
        self.slack_client = AsyncWebClient(token=config.slack.bot_token)

        handler = None
        if config.slack.app_token:
            if config.environment == "production":
                logging.warning(
                    "You are currently running Socket mode in production. This is NOT RECOMMENDED - you should set up a proper HTTP server with a request URL."
                )
            from slack_bolt.adapter.socket_mode.async_handler import (
                AsyncSocketModeHandler,
            )

            handler = AsyncSocketModeHandler(self.app, config.slack.app_token)
            logger.debug("Starting Socket Mode handler")
            await handler.connect_async()

        logger.debug(f"Environment setup in {time() - st:.02}s")
        await send_heartbeat(
            ":neodog_nom_stick: beep boop! online!",
            client=self.slack_client,
        )

        yield

        logger.debug("Exiting environment context")

        if handler:
            logger.debug("Stopping Socket Mode handler")
            await handler.close_async()

        await self.http.close()


env = Environment()
