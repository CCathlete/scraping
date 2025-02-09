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
    for product in products:
        # The dict keys are tuples, iterating over dict is iterating over the keys.
        for field_name, xpath in data:
            data[field_name, xpath].append(
                product.find_element(
                    by=By.XPATH,
                    value=xpath,
                    # Converting to text when storing.
                ).text,
            )

    # Creating a DataFrame from field_name and the inner value.
    result = pd.DataFrame(
        {field_name: data[field_name, xpath] for field_name, xpath in data}
    )

    # Dumping the DF into a csv.
    result.to_csv("audoble_books.csv", index=False)

    driver.quit()
    return result
