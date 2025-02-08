"""
A module for scraping information about a country's team's
matches from https://www.adamchoi.co.uk/overs/detailed
"""

from typing import Union
import os
import time
import pandas as pd
from src.imports.selenium_imports import (
    webdriver,
    WebElement,
    Select,
    WebDriverWait,
    EC,
    By,
    TimeoutException,
)


def get_all_matches(country: str) -> pd.DataFrame:
    """Scraping info about all matches that held place in the
    input country, and returning a dataframe with the results.
    """
    results: pd.DataFrame = pd.DataFrame({})
    if country == "":
        raise ValueError("Country name is empty.")

    url_details: str = "https://www.adamchoi.co.uk/overs/detailed"

    # Path to the chromedriver executable.
    driver_path: Union[str, None] = os.getenv("CHROMEDRIVER_EXE_PATH")
    if driver_path is None:
        raise ValueError("Environment variable CHROMEDRIVER_EXE_PATH is not set.")

    # Defining a driver object.
    driver: webdriver.Chrome = webdriver.Chrome()

    # Opening the website with Chrome (GET request).
    driver.get(url_details)

    # Waiting for the cookie popup and clicking Consent.
    try:
        cookie_button = WebDriverWait(driver, 500).until(
            EC.element_to_be_clickable((By.XPATH, "//button/p[text()='Consent']"))
        )
        cookie_button.click()
    except TimeoutException:
        print("No cookie popup found.")
        # Closing the browser.
        driver.quit()
        return results

    # Defining a button object for the "All matches" button
    # css class.
    all_matches_button: WebElement = driver.find_element(
        by=By.XPATH,
        value=r"//label[@analytics-event='All matches']",
    )
    all_matches_button.click()

    # Defining an object for the select tag with id="country".
    country_dropdown: Select = Select(
        driver.find_element(
            by=By.ID,
            value="country",
        ),
    )
    # Selecting the option with the input country name.
    country_dropdown.select_by_visible_text(country)
    # Dropdown menu involves a JavaScript, so we need to wait
    # for the page to load.
    time.sleep(3)

    # After selecting the country, the HTML will contain
    # a table with the matches, where each table row is a
    # match.
    table_rows: list[WebElement] = driver.find_elements(
        by=By.TAG_NAME,
        value="tr",
    )
    # TODO: Add a constraint for selecting only rows with more
    # than 1 column (some rows are irrelevant and need to be
    # screened out).

    column_names: list[str] = [
        "date",
        "home_team",
        "score",
        "away_team",
    ]
    data: dict[str, list[str]] = {n: [] for n in column_names}

    # Entering the data from each table row into the
    # corresponding lists.
    # Each row has 4 child tags of table data = <td>.
    for row in table_rows:
        data["date"].append(
            # This returns a WebElement object so we need to
            # apply the text method at the end.
            row.find_element(
                by=By.XPATH,
                value="./td[1]",
            ).text,
        )
        # td[2] is just an icon so we skip it.
        data["home_team"].append(
            row.find_element(
                by=By.XPATH,
                value="./td[3]",
            ).text,
        )
        data["score"].append(
            row.find_element(
                by=By.XPATH,
                value="./td[4]",
            ).text,
        )
        data["away_team"].append(
            row.find_element(
                by=By.XPATH,
                value="./td[5]",
            ).text,
        )

    # Closing the browser.
    driver.quit()
    # Creating a DataFrame from the data.
    results = pd.DataFrame(data)

    return results
