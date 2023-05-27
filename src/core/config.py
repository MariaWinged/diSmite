from pathlib import Path

from pydantic import BaseSettings


class BaseConfig(BaseSettings):
    class Config:
        env_file = Path(__file__).parent.parent.parent / '.env'
        env_file_encoding = 'utf-8'


class HiRezConfig(BaseConfig):
    devId: int
    authKey: str

    class Config:
        env_prefix = 'HIREZ_'


class DiscordConfig(BaseConfig):
    token: str
    bot: str = 'diSmite'
    appId: int
    prefix: list[str] = ['~']
    intents: int = 395137644544

    class Config:
        env_prefix = 'DISCORD_'


class Settings(BaseSettings):
    hirez_config: HiRezConfig = HiRezConfig()
    discord_config: DiscordConfig = DiscordConfig()


settings = Settings()
