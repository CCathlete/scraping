"""
Selenium based implementation of the spider.Skeleton 
interface.
"""

from ..interface import Skeleton
from src.imports.selenium_imports import *
from src.imports.data import *
from src.imports.typing import *
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
    ) -> None:
        self.locators = locators
        self.root_url = root_url

    def init_driver(
        self,
        driver_type: type[Driver] = webdriver.Chrome,
    ) -> Driver:
        """Initialises the driver."""
        self.driver = driver_type(options=self.driver_options)
        return self.driver

    def scrape(
        self,
        url: str,
        callback: Optional[Callable[[Data], None]] = None,
    ) -> Data:
        """Scrapes data from a given URL.

        - If `callback` is provided, calls it with the scraped
        data (for Scrapy).

        - Otherwise, returns data directly (for Selenium).
        """
        return pd.DataFrame()

    def process(
        self,
        data: Data,
    ) -> Output:
        """Processes the scraped data and returns the output."""
        pass

    def save_data(
        self,
        data: Union[Output, Data],
        path: str,
        extension: SupportedOutput = SupportedOutput.CSV,
    ) -> None:
        """Gets data, a path to a parent folder and an
        extension and saves the data to a file.

        Raises an error is the writing had failed.
        """
        pass
