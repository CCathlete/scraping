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
    ) -> Driver:
        """Initialises the driver."""
        pass

    @abstractmethod
    def scrape(
        self,
    ) -> Data:
        """_summary_"""
        pass
