"""
A module with book extraction methods using 
the Spider class.
"""

import os
from src.aggregators.spider.selenium import Spider
from src.entities import Container, Locator
from src.imports.data import Output
from src.imports.typing import *
from src.imports.selenium_imports import *
from src.imports.data import SupportedOutput


def get_audiobooks(
    url: str,
    driver_type: type[Driver],
    options_to_set: list[str] = [],
    output_path: str = f"{os.getcwd()}/output/audiobooks",
) -> Output:
    """
    Gets base url, driver type and options to set and returns
    a pandas object with all the audiobooks.
    """
    if not isinstance(url, str):
        return None

    # Initialising the spider.
    spider: Spider = Spider(
        root_url=url,
        options_to_set=options_to_set,
        pagination_opts=Spider.PaginationOptions(
            next_button_locator=Locator(
                By.XPATH,
                './/span[contains(@class , "nextButton")]',
                "next button",
            ),
            max_pages=100,
        ),
    ).init_driver(
        driver_type,
    )

    book_rel_path: str = r".//li[contains(@class, 'bc-list-item')]"

    # Setting up the containers and locators for book
    # extraction.
    return (
        spider.set_container_tree(
            root=Container(
                name="top level container",
                # Container locator is not stored in the output.
                locator=Locator(
                    l_type=By.CLASS_NAME,
                    value="adbl-impression-container",
                    name="locator for top level container",
                ),
                # Already initialised.
                parent_element=spider.driver,
                # After inisialising the tree root, we're setting
                # its sub containers (in place).
            ).sub_containers_from_common_locator(
                common_locator=Locator(
                    l_type=By.XPATH,
                    value=book_rel_path,
                ),
                # Every sub container will have these sub locators
                # to extract book data.
                sub_locators=[
                    Locator(
                        l_type=By.XPATH,
                        value=rf"{val}",
                        name=name,
                    )
                    for name, val in [
                        ("title", ".//h3[contains(@class, 'bc-heading')]"),
                        ("sub_title", ".//li[contains(@class, 'subtitle')]"),
                        ("author", ".//li[contains(@class, 'authorLabel')]"),
                        ("narrator", ".//li[contains(@class, 'narratorLabel')]"),
                        ("series", ".//li[contains(@class, 'seriesLabel')]"),
                        ("length", ".//li[contains(@class, 'runtimeLabel')]"),
                        ("release_date", ".//li[contains(@class, 'releaseDateLabel')]"),
                        ("language", ".//li[contains(@class, 'languageLabel')]"),
                    ]
                ],
                # All books have more than 5 fields and we want to
                # filter out irrelevant elements.
                condition=lambda elem: isinstance(elem, WebElement)
                and len(
                    elem.find_elements(
                        by=By.XPATH,
                        value=book_rel_path,
                    )
                )
                > 4,
            ),
        )
        .scrape()
        .save_data(output_path, SupportedOutput.CSV)
        .get_data()
    )
