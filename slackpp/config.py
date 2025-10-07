from pydantic_settings import BaseSettings
from pydantic_settings import SettingsConfigDict


class SlackConfig(BaseSettings):
    bot_token: str
    signing_secret: str
    app_token: str | None
    heartbeat_channel: str | None = None


class Config(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_nested_delimiter="__")
    slack: SlackConfig
    environment: str = "development"
    port: int = 3000


config = Config()  # type: ignore
