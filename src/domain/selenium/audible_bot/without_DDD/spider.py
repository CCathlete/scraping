"""
Building the spider.
"""

from src.imports.selenium_imports import *
from src.imports.typing import *
from src.imports.data import *

AUDIBLE_SEARCH_ROOT: str = "https://www.audible.com/search"


def get_ebooks(
    driver_options: Optional[list[str]] = None,
    url: str = AUDIBLE_SEARCH_ROOT,
    driver_class: type[Driver] = webdriver.Chrome,
) -> pd.DataFrame:
    """Gets eboks info from audible using Selenium."""
    # Input validation.
    wrong_type_url: bool = not isinstance(url, str)
    driver_is_not_a_class: bool = not isinstance(driver_class, type)
    wrong_type_driver: bool = (
        driver_class is Driver  # pylint: disable=unidiomatic-typecheck
    )
    empty_url: bool = not url or url == ""

    if any([wrong_type_url, driver_is_not_a_class, wrong_type_driver, empty_url]):
        raise ValueError("Invalid arguments.")

    # Initialisation.
    result: pd.DataFrame = pd.DataFrame({})
    data: dict[tuple[str, str], list[str]] = {
        ("title", ".//h3[contains(@class, 'bc-heading')]"): [],
        ("sub_title", ".//li[contains(@class, 'subtitle')]"): [],
        ("author", ".//li[contains(@class, 'authorLabel')]"): [],
        ("narrator", ".//li[contains(@class, 'narratorLabel')]"): [],
        ("series", ".//li[contains(@class, 'seriesLabel')]"): [],
        ("length", ".//li[contains(@class, 'runtimeLabel')]"): [],
        ("release_date", ".//li[contains(@class, 'releaseDateLabel')]"): [],
        ("language", ".//li[contains(@class, 'languageLabel')]"): [],
    }
    options: DriverOptions = init_driver_options(driver_class=driver_class)
    # TODO: Check if in place is possible.
    options = set_options(driver_options, options)

    ################################################
    # TODO: Might need refactoring.
    # Calling the constructor.
    driver: Driver  # Declaration.
    if driver_class is webdriver.Chrome:
        driver = webdriver.Chrome(options=options)
    elif driver_class is webdriver.Firefox:
        driver = webdriver.Firefox(options=options)
    elif driver_class is webdriver.Edge():
        # Looks like options are not supported.
        driver = webdriver.Edge()
    elif driver_class is webdriver.Ie:
        driver = webdriver.Ie(options=options)
    ################################################

    driver.get(url)
    driver.maximize_window()

    # Locating the container that has the list of books.
    container: WebElement = wait(driver, 10).until(
        EC.presence_of_element_located(
            (By.CLASS_NAME, "adbl-impression-container"),
        ),
    )
    if not container:
        raise ValueError("Container not found.")

    book_rel_xpath: str = r".//li[contains(@class, 'bc-list-item')]"
    # Getting all list items in the container.
    # We screen for irrelevant elementc.
    products: list[WebElement] = [
        product
        for product in container.find_elements(
            by=By.XPATH,
            value=book_rel_xpath,
        )
        if isinstance(product, WebElement)
        and len(product.find_elements(by=By.XPATH, value=book_rel_xpath)) > 5
    ]
    if not products:
        raise ValueError("List of books not found.")

    # Extracting data from each book.
    for product in products:
        # The dict keys are tuples, iterating over dict is iterating over the keys.
        for field_name, xpath in data:
            try:
                data[field_name, xpath].append(
                    product.find_element(
                        by=By.XPATH,
                        value=xpath,
                        # Converting to text when storing.
                    ).text,
                )
            except (NoSuchAttributeException, NoSuchElementException):
                data[field_name, xpath].append("")

    # Creating a DataFrame from field_name and the inner value.
    result = pd.DataFrame(
        {field_name: data[field_name, xpath] for field_name, xpath in data}
    )

    # Dumping the DF into a csv.
    result.to_csv("audible_books.csv", index=False)

    driver.quit()
    return result
