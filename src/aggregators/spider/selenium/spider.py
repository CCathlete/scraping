"""
Selenium based implementation of the spider.Skeleton 
interface.
"""

from ..interface import Skeleton
from ..imports.selenium_imports import *
from src.entities.locator import Locator

DEFAULT_LOCATORS: list[Locator] = [Locator()]


class Spider(Skeleton):
    """A spider that uses Selenium to scrape data."""

    locators: list[Locator]
    root_url: str
    driver: Driver
    driver_options: DriverOptions

    def __init__(
        self,
        locators: list[Locator] = DEFAULT_LOCATORS,
        root_url: str = "https://www.google.com",
        driver: Driver = webdriver.Chrome(),
        driver_options: DriverOptions = webdriver.ChromeOptions(),
    ) -> None:
        self.locators = locators
        self.root_url = root_url
        self.driver = driver
        self.driver_options = driver_options
