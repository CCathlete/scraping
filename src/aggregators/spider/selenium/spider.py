"""
Selenium based implementation of the spider.Skeleton 
interface.
"""

from ..interface import Skeleton
from src.imports.selenium_imports import *
from src.imports.data import *
from src.imports.typing import *
from src.entities.container import Container


class Spider(Skeleton):
    """A spider that uses Selenium to scrape data."""

    def __init__(
        self,
        root_url: str = "https://www.google.com",
        options_to_set: list[str] = ["headless"],
    ) -> None:
        self.root_url = root_url
        self.options_to_set = options_to_set

    def set_container_tree(
        self,
        containers: list[Container] = [],
    ) -> None:
        """Sets the container tree."""
        self.containers = containers

    def init_driver(
        self,
        driver_type: type[Driver],
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

        self.driver.get(url)

        data: dict[str, list[str]] = {}

        for container in self.containers:
            container.extract(data)

        return pd.DataFrame(data)

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
