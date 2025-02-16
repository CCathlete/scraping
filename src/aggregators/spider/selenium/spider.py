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
        root: Optional[Container] = None,
    ) -> Self:
        """Sets the container tree."""
        self.tree_root = root

        return self

    def init_driver(
        self,
        driver_type: type[Driver],
    ) -> Self:
        """Initialises the driver."""
        options: DriverOptions = set_options(
            to_set=self.options_to_set,
            initialised_opts=init_driver_options(driver_type),
        )
        ################################################
        # TODO: Might need refactoring.
        # Calling the constructor.
        self.driver: Driver  # Declaration.
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

        self.driver.get(self.root_url)

        return self

    def scrape(
        self,
        url: str,
        callback: Optional[Callable[[Data], None]] = None,
    ) -> Optional[Data]:
        """Scrapes data from a given URL and returns the data
        directly.
        """
        if not self.tree_root:
            print("No container tree set.")
            return None

        data: dict[str, list[str]] = {}

        self.tree_root.extract(data)

        self.driver.quit()
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
