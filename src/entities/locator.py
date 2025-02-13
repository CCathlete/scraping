"""
A module that defines a locator for a web element.
"""

from ..imports.selenium_imports import By


class Locator:
    """A locator for a web element."""

    locator_type: str = By.XPATH
    locator_value: str = "h1"
    locator_name: str = "Main header"

    def __init__(
        self,
        locator_type: str = By.XPATH,
        locator_value: str = "h1",
        locator_name: str = "Main header",
    ) -> None:
        self.locator_type = locator_type
        self.locator_value = locator_value
        self.locator_name = locator_name
