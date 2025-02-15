"""
A module with book extraction methods using 
the Spider class.
"""

from src.aggregators.spider.selenium import Spider
from src.entities import Container, Locator
from src.imports.data import Output
from src.imports.typing import *
from src.imports.selenium_imports import By


def get_audiobooks(
    url: str,
) -> Output:
    """_summary_

    Args:
        url (str): _description_

    Returns:
        Output: _description_
    """
    if not isinstance(url, str):
        return None

    # Setting up the containers and locators for book
    # extraction.

    loc_tree: list[Container] = [
        Container(
            name="top level container",
            # Container locator is not stored in the output.
            locator=Locator(
                l_type=By.CLASS_NAME,
                value="abdl-impression-container",
                name="locator for top level container",
            ),
            sub_containers=[],
        ),
    ]

    return None
