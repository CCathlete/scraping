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
    options_to_set: list[str]

    def __init__(
        self,
        locators: list[Locator] = DEFAULT_LOCATORS,
        root_url: str = "https://www.google.com",
        options_to_set: list[str] = ["headless"],
    ) -> None:
        self.locators = locators
        self.root_url = root_url
        self.options_to_set = options_to_set

    def init_driver(
        self,
        driver_type: type[Driver] = webdriver.Chrome,
    ) -> Self:
        """Initialises the driver."""
        options: DriverOptions = set_options(
            self.options_to_set,
            init_driver_options(driver_type),
        )
        ################################################
        # TODO: Might need refactoring.
        # Calling the constructor.
        driver: Driver  # Declaration.
        if driver_type is webdriver.Chrome:
            self.driver = webdriver.Chrome(options=options)
        elif driver_type is webdriver.Firefox:
            self.driver = webdriver.Firefox(options=options)
        elif driver_type is webdriver.Edge():
            # Looks like options are not supported.
            self.driver = webdriver.Edge()
        elif driver_type is webdriver.Ie:
            self.driver = webdriver.Ie(options=options)
        ################################################

        return self

    def scrape(
        self,
        url: str,
        callback: Optional[Callable[[Data], None]] = None,
    ) -> Data:
        """Scrapes data from a given URL and returns the data
        directly.
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
