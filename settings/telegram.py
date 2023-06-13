
__author__ = 'Khiem Doan'
__github__ = 'https://github.com/khiemdoan'
__email__ = 'doankhiem.crazy@gmail.com'

from functools import lru_cache

from pydantic import BaseSettings, Field
from pydantic.error_wrappers import ValidationError


class TelegramSettings(BaseSettings):

    bot_token: str = Field(env='TELEGRAM_BOT_TOKEN')


@lru_cache
def get_telegram_settings() -> TelegramSettings:
    try:
        return TelegramSettings()
    except ValidationError:
        pass

    return TelegramSettings(_env_file='.env')
