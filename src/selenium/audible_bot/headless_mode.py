# pylint: disable=wildcard-import
"""
Scraping list of audiobooks in headless mode.
"""

from src.imports.selenium_imports import *
from src.imports.typing import *
from src.imports.data import *
from .spider import AUDIBLE_SEARCH_ROOT, get_ebooks


def get_ebooks_headless(
    url: str = AUDIBLE_SEARCH_ROOT,
    driver_class: type[Driver] = webdriver.Chrome,
) -> pd.DataFrame:
    """Gets ebooks info from audible using Selenium in headless mode."""
    options: list[str] = ["headless"]

    return get_ebooks(
        driver_options=options,
        url=url,
        driver_class=driver_class,
    )
