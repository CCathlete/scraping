"""
Entry point to the program.
"""

import src.domain.selenium as my_selenium
from src.imports.selenium_imports import TimeoutException, webdriver

AUDIBLE_SEARCH_ROOT: str = "https://www.audible.com/search"


def country_matches() -> None:
    """Main funciton for a country's football matches data
    extraction."""
    country: str = "Spain"
    print()  # \n
    print(f"Country: {country}")
    print(f"Games Data: {my_selenium.get_all_matches(country)}")


def spider() -> None:
    """Entry point for spider creation."""
    print()  # \n
    try:
        print(f"List of ebooks from Audible: {my_selenium.get_ebooks()}")
    except (ValueError, TimeoutException) as err:
        print(err)


def spider_headless() -> None:
    """Entry point for spider creation in headless mode."""
    print()  # \n
    try:
        print(
            f"List of ebooks from Audible (headless mode): {my_selenium.get_ebooks_headless()}"
        )
    except (ValueError, TimeoutException) as err:
        print(err)


def ebooks_ddd() -> None:
    """Entry point for scraping using DDD architecture."""
    print()  # \n
    try:
        print(
            f"List of ebooks from Audible: {my_selenium.get_audiobooks(
                url=AUDIBLE_SEARCH_ROOT,
                driver_type=webdriver.Chrome,
                options_to_set=["headless"],
                )}"
        )
    except (ValueError, TimeoutException) as err:
        print(err)


if __name__ == "__main__":
    # country_matches()
    # spider()
    # spider_headless()
    ebooks_ddd()
