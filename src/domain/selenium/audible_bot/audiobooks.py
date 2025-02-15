"""
A module with book extraction methods using 
the Spider class.
"""

from src.aggregators.spider.selenium import Spider
from src.entities import Container, Locator
from src.imports.data import Output
from src.imports.typing import *
from src.imports.selenium_imports import *


def get_audiobooks(
    url: str,
    driver_type: type[Driver],
) -> Output:
    """_summary_

    Args:
        url (str): _description_

    Returns:
        Output: _description_
    """
    if not isinstance(url, str):
        return None

    # Initialising the spider.
    spider: Spider = Spider(
        root_url=url,
        # options_to_set=["headless"],
        options_to_set=[],
    ).init_driver(
        driver_type,
    )

    # Setting up the containers and locators for book
    # extraction.
    spider.set_container_tree(
        containers=[
            Container(
                name="top level container",
                # Container locator is not stored in the output.
                locator=Locator(
                    l_type=By.CLASS_NAME,
                    value="abdl-impression-container",
                    name="locator for top level container",
                ),
                parent_element=spider.driver,
                sub_containers=[],
            ),
        ],
    )

    return None
