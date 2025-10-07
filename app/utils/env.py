import os

from aiohttp import ClientSession
from dotenv import load_dotenv
from slack_sdk.web.async_client import AsyncWebClient


load_dotenv(override=True)


class Environment:
    def __init__(self):
        self.slack_bot_token = os.environ.get("SLACK_BOT_TOKEN", "unset")
        self.slack_signing_secret = os.environ.get("SLACK_SIGNING_SECRET", "unset")
        self.slack_app_token = os.environ.get("SLACK_APP_TOKEN")

        self.environment = os.environ.get("ENVIRONMENT", "development")

        self.port = int(os.environ.get("PORT", 3000))

        self.slack_heartbeat_channel = os.environ.get("SLACK_HEARTBEAT_CHANNEL")

        unset = [key for key, value in self.__dict__.items() if value == "unset"]

        if unset:
            raise ValueError(f"Missing environment variables: {', '.join(unset)}")

        self.session: ClientSession

        self.slack_client = AsyncWebClient(token=self.slack_bot_token)


env = Environment()
