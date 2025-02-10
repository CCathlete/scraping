"""
Imports for selenium.
"""

from typing import Union
from typing_extensions import TypeAlias
from selenium import webdriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import (
    TimeoutException,
    NoSuchAttributeException,
    NoSuchElementException,
)

Driver: TypeAlias = Union[
    webdriver.Chrome,
    webdriver.Firefox,
    webdriver.Safari,
    webdriver.Edge,
    webdriver.Ie,
]


__all__ = [
    "Driver",
    "webdriver",
    "WebElement",
    "Select",
    "WebDriverWait",
    "EC",
    "By",
    "TimeoutException",
    "NoSuchAttributeException",
    "NoSuchElementException",
]
