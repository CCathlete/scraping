"""
Definition of the Container class.
A container is an HTML element that contains other elements.
"""

from .locator import Locator
from src.imports.selenium_imports import WebElement, Driver
from src.imports.typing import Union


class Container:
    """
    A web element that contains other elements.
    """

    def __init__(
        self,
        name: str,
        locator: Locator,
        sub_containers: list["Container"] = [],
        sub_locators: list[Locator] = [],
    ) -> None:
        self.name = name
        self.locator = locator
        self.sub_containers = sub_containers
        self.sub_locators = sub_locators

    def extract(
        self,
        container: "Container",
        parent_element: Union[WebElement, Driver],
        data: dict[str, list[str]] = {},
    ) -> dict[str, list[str]]:
        """
        Recursively extracts data from all elements and sub
        elements. Gets a dictionary of data and inserts data
        into it.
        """

        # The element of the container itself.
        element: WebElement = parent_element.find_element(
            container.locator.type,
            container.locator.value,
        )

        # Iterating over all direct sub elements that are not
        # containers themselves.
        for locator in container.sub_locators:
            elements: list[WebElement] = element.find_elements(
                locator.type,
                locator.value,
            )
            if elements:
                data[locator.name] += [element.text for element in elements]
            else:
                # We still want to add something so we won't
                # mess up the index order between cells in
                # different fields in data.
                data[locator.name] = [""]

        # Now that we've extracted all the data from this
        # level, we move to the next level of sub containers.
        for sub_container in container.sub_containers:
            self.extract(
                sub_container,
                element,
                data,
            )

        return data
