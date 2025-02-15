"""
Definition of the Container class.
A container is an HTML element that contains other elements.
"""

from .locator import Locator
from src.imports.selenium_imports import WebElement, Driver
from src.imports.typing import Union, Optional, Self


class Container:
    """
    A web element that contains other elements.
    """

    def __init__(
        self,
        name: str,
        # Can't be optional.
        parent_element: Union[WebElement, Driver],
        locator: Optional[Locator] = None,
        element: Optional[WebElement] = None,
        sub_containers: list["Container"] = [],
        sub_locators: list[Locator] = [],
    ) -> None:
        self.name = name
        self.locator: Optional[Locator]

        if locator and not element:
            self.locator = locator
            self.element: WebElement = parent_element.find_element(
                by=locator.type,
                value=locator.value,
            )
        elif element and not locator:
            self.element = element
            self.locator = None
        elif element and locator:
            self.element = element
            self.locator = locator
        else:
            raise ValueError(
                "Either locator, element or both must be provided.",
            )

        self.sub_containers = sub_containers
        self.sub_locators = sub_locators

    def sub_containers_from_elements(
        self,
        elements: list[WebElement] = [],
    ) -> Self:
        """Sets sub containers from a list of web elements."""
        self.sub_containers = [
            Container(
                name=f"{self.name}: {element.tag_name}",
                parent_element=self.element,
                element=element,
            )
            for element in elements
        ]

        return self

    # TODO: Add condition and locators to add to each container.
    def sub_containers_from_common_locator(
        self,
        common_locator: Locator,
    ) -> Self:
        """Sets sub containers from elements of a common
        locator."""
        elements: list[WebElement] = self.element.find_elements(
            by=common_locator.type,
            value=common_locator.value,
        )

        self.sub_containers = [
            Container(
                name=f"{self.name}: {element.tag_name}",
                parent_element=self.element,
                element=element,
            )
            for element in elements
        ]

        return self

    def extract(
        self,
        data: dict[str, list[str]] = {},
    ) -> dict[str, list[str]]:
        """
        Recursively extracts data from all elements and sub
        elements. Gets a dictionary of data and inserts data
        into it.
        """

        # The element of the container itself.
        element: WebElement = self.element

        # Iterating over all direct sub elements that are not
        # containers themselves.
        for locator in self.sub_locators:
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
        # All sub containers are initialised so they contain
        # element and parent_element fields.
        for sub_container in self.sub_containers:
            sub_container.extract(data)

        return data
