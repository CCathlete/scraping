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
        url: str,
        callback: Optional[Callable[[Data], None]] = None,
    ) -> Optional[Data]:
        """Scrapes data from a given URL.

        - If `callback` is provided, calls it with the scraped
        data (for Scrapy).

        - Otherwise, returns data directly (for Selenium).
        """
        pass

    @abstractmethod
    def process(
        self,
        data: Data,
    ) -> Output:
        """Processes the scraped data and returns the output."""
        pass

    @abstractmethod
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
