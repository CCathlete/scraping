"""
Imports for selenium.
"""

from .typing import Union, TypeAlias, get_args, Optional
from selenium import webdriver
from selenium.webdriver.edge.options import Options as EdgeOptions

from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import Select, WebDriverWait as wait
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
    webdriver.Edge,
    webdriver.Ie,
]

DriverOptions: TypeAlias = Union[
    webdriver.ChromeOptions,
    webdriver.FirefoxOptions,
    EdgeOptions,
    webdriver.IeOptions,
]


def init_driver_options(driver_class: type[Driver]) -> DriverOptions:
    """Returns the options for the driver."""
    options_types: tuple[type[DriverOptions]] = get_args(DriverOptions)
    driver_types: tuple[type[Driver]] = get_args(Driver)
    type_dict: dict[type[Driver], type[DriverOptions]] = dict(
        zip(driver_types, options_types)
    )

    # Calling the constructor after we found the right type
    # (class), thus returning an initialised object.
    return type_dict[driver_class]()


def set_options(
    to_set: Optional[list[str]], initialised_opts: DriverOptions
) -> DriverOptions:
    """Activates the options from to_ set in initialised_opts."""
    if to_set is None:
        return initialised_opts

    for opt in to_set:
        if opt == "headless" and hasattr(initialised_opts, "add_argument"):
            initialised_opts.add_argument("--headless")
        elif hasattr(initialised_opts, opt):
            setattr(initialised_opts, opt, True)

    return initialised_opts


__all__ = [
    "DriverOptions",
    "Driver",
    "webdriver",
    "WebElement",
    "Select",
    "wait",
    "EC",
    "By",
    "TimeoutException",
    "NoSuchAttributeException",
    "NoSuchElementException",
    "init_driver_options",
    "set_options",
]
