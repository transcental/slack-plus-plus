from slack_bolt.async_app import AsyncApp

from slackpp.config import config

app = AsyncApp(token=config.slack.bot_token, signing_secret=config.slack.signing_secret)
