"""
Building the spider.
"""

from src.imports.selenium_imports import (
    webdriver,
    Driver,
    By,
    WebElement,
    EC,
    WebDriverWait as wait,
)
import pandas as pd
from typing import Union, Type

AUDIBLE_ROOT: str = "https://www.audible.com"


def get_ebooks(
    url: str = AUDIBLE_ROOT,
    driver_class: Type[Driver] = webdriver.Chrome,
) -> pd.DataFrame:
    """Gets eboks info from audible using Selenium."""
    # Input validation.
    wrong_type_url: bool = not isinstance(url, str)
    driver_is_not_a_class: bool = not isinstance(driver_class, type)
    wrong_type_driver: bool = (
        type(driver_class) != Type[Driver]  # pylint: disable=unidiomatic-typecheck
    )
    empty_url: bool = not url or url == ""

    if any([wrong_type_url, driver_is_not_a_class, wrong_type_driver, empty_url]):
        raise ValueError("Invalid arguments.")

    # Initialisation.
    result: pd.DataFrame = pd.DataFrame({})
    data: dict[str, list[str]] = {
        "title": [],
        "sub_title": [],
        "author": [],
        "narrator": [],
        "series": [],
        "length": [],
        "release_date": [],
        "language": [],
    }

    # Calling the constructor.
    driver: Driver = driver_class()
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

    # Getting all list items in the container.
    # We screen for irrelevant elementc.
    products: list[WebElement] = [
        product
        for product in container.find_elements(
            by=By.XPATH,
            value="./li",
        )
        if isinstance(product, WebElement)
        and len(product.find_elements(by=By.XPATH, value="./li")) > 5
    ]
    if not products:
        raise ValueError("List of books not found.")

    # Extracting data from each book.

    driver.close()
    return result
