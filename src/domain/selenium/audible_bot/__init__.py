"""Init module for the audible bot package."""

from src.domain.selenium.audible_bot.without_DDD.spider import get_ebooks
from src.domain.selenium.audible_bot.without_DDD.headless_mode import (
    get_ebooks_headless,
)
