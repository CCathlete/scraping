"""
A spider repository contract (interface).
"""

from abc import ABC, abstractmethod
from src.imports.data import *
from src.imports.selenium_imports import Driver as SeleniumDriver
from src.imports.typing import *

Driver: TypeAlias = Union[SeleniumDriver]


class Skeleton(ABC):
    """An abstract class that defines the structure of a
    spider.
    """

    __data: Data

    @abstractmethod
    def init_driver(
        self,
        driver_type: type[Driver],
    ) -> Self:
        """Initialises the driver."""
        pass

    @abstractmethod
    def scrape(
        self,
    ) -> Self:
        """Scrapes data from URL given to an internal driver.

        - If `callback` is provided, calls it with the scraped
        data (for Scrapy).

        - Otherwise, returns data directly (for Selenium).
        """
        pass

    @abstractmethod
    def process(
        self,
    ) -> Self:
        """Processes the scraped data and returns the output."""
        pass

    @abstractmethod
    def save_data(
        self,
        path: str,
        extension: SupportedOutput = SupportedOutput.CSV,
    ) -> Self:
        """Gets data, a path to a parent folder and an
        extension and saves the data to a file.

        Raises an error is the writing had failed.
        """
        pass

    @abstractmethod
    def get_data(
        self,
    ) -> Data:
        """
        Returns the scraped data.
        """
        return self.__data
