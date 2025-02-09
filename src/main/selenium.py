"""
Entry point to the program.
"""

import src.selenium as my_selenium
from src.imports.selenium_imports import TimeoutException


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


if __name__ == "__main__":
    # country_matches()
    spider()
