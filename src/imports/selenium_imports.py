"""
Imports for selenium.
"""

from selenium import webdriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException

__all__ = [
    "webdriver",
    "WebElement",
    "Select",
    "WebDriverWait",
    "EC",
    "By",
    "TimeoutException",
]
