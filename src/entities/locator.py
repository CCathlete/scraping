"""
A module that defines a locator for a web element.
"""

from ..imports.selenium_imports import By


class Locator:
    """A locator for a web element."""

    def __init__(
        self,
        l_type: str = By.XPATH,
        value: str = "h1",
        name: str = "Main header",
    ) -> None:
        self.type = l_type
        self.value = value
        self.name = name
