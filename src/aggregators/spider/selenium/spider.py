"""
Selenium based implementation of the spider.Skeleton 
interface.
"""

import time
from ..interface import Skeleton
from src.imports.selenium_imports import *
from src.imports.data import *
from src.imports.typing import *
from src.entities.container import Container
from src.entities.locator import Locator


class Spider(Skeleton):
    """A spider that uses Selenium to scrape data."""

    @dataclass
    class PaginationOptions:
        """Configuration options for pagination.
        Fields:
        - next_button_locator (Locator): Locator for the "Next" button.
        - next_page_url_fn (Callable[[int], str], optional): Function to generate the next page URL.
        - scroll (bool, optional): Whether to scroll down for infinite scrolling.
        - max_pages (int, optional): Maximum number of pages to scrape.
        """

        next_button_locator: Optional[Locator]
        next_page_url_fn: Optional[Callable[[int], str]] = None
        scroll: bool = False
        max_pages: int = 100
        curr_page: int = 1

    def __init__(
        self,
        root_url: str = "https://www.google.com",
        options_to_set: list[str] = ["headless"],
        pagination_opts: Optional[PaginationOptions] = None,
    ) -> None:
        self.root_url = root_url
        self.options_to_set = options_to_set
        if pagination_opts:
            self.pagination_opts = pagination_opts

    def set_default_pagination_options(self, opts: PaginationOptions):
        """
        Registers new default pagination options to the spider.
        """
        self.pagination_opts = opts

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
        override_pag_opts: Optional[PaginationOptions] = None,
    ) -> Optional[Data]:
        """Scrapes data from a given URL and returns the data
        directly.
        """
        if not self.tree_root:
            print("No container tree sets.")
            return None

        data: dict[str, list[str]] = {}

        while self.paginate(override_pag_opts):
            self.tree_rot.extract(data)

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

    def __scroll_to_bottom(self):
        """
        Scrolls to the bottom of the page, triggering
        a javascript function.
        """
        self.driver.execute_script(
            "window.scrollTo(0, document.body.scrollHeight);",
        )
        time.sleep(2)

    def paginate(
        self,
        override_pag_opts: Optional[PaginationOptions] = None,
    ) -> bool:
        """
        Handles pagination depending on the strategy:
        - Clicks a 'Next' button if `next_button_locator` is provided.
        - Navigates using URL pattern if `next_page_url_fn` is provided.
        - Scrolls down for infinite scrolling if `scroll` is True.

        Args:
            next_button_locator (Locator, optional): Locator for the "Next" button.
            next_page_url_fn (Callable[[int], str], optional): Function to generate paginated URLs.
            scroll (bool, optional): Enables infinite scrolling.
            max_pages (int): Maximum number of pages to prevent infinite loops.
        """
        # Overriding pagination options if provided.
        pag_opts: Spider.PaginationOptions = override_pag_opts or self.pagination_opts

        if pag_opts.curr_page > pag_opts.max_pages:
            return False

        # Pagination logic - flipping to the next page.
        # There are cases you need to scroll to the bottom
        # of each page for elements to appear.
        if pag_opts.scroll:
            self.__scroll_to_bottom()
            time.sleep(2)  # Waiting for the page to load.

        # If we have more pages to scrape, we'll return True.
        if pag_opts.next_page_url_fn:
            next_url: str = pag_opts.next_page_url_fn(
                pag_opts.curr_page,
            )
            if next_url:
                self.driver.get(next_url)
                pag_opts.curr_page += 1
                return True

        if pag_opts.next_button_locator:
            try:
                next_button: WebElement = self.driver.find_element(
                    pag_opts.next_button_locator.type,
                    pag_opts.next_button_locator.value,
                )
                if next_button.is_displayed():
                    next_button.click()
                    time.sleep(2)  # Loading time.
                    pag_opts.curr_page += 1
                    return True
            except (NoSuchElementException, TimeoutException):
                return False  # No more pages to load.

        return False
