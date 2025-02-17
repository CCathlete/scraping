"""
Data related imports.
"""

from .typing import *
import pandas as pd
from enum import Enum
from dataclasses import dataclass

Data: TypeAlias = Union[pd.DataFrame, pd.Series]
Output: TypeAlias = Union[Data, None]


class SupportedOutput(str, Enum):
    """Constants for supported file extensions."""

    # This class inherit from the str and enum meta classes,
    # meaning that all attributes are instances of the class.
    # i.e. SupportedOutput.CSV is an instance of
    # SupportedOutput.

    XML = "xml"
    CSV = "csv"
    JSON = "json"
    HTML = "html"
    XLSX = "xlsx"
    XLS = "xls"
    TSV = "tsv"
    TXT = "txt"
    MD = "md"
    YAML = "yaml"
    YML = "yml"
    TOML = "toml"
    PICKLE = "pickle"
    PARQUET = "parquet"
    CSS = "css"
    JS = "js"
    TS = "ts"
    PY = "py"
    JSX = "jsx"
    TSX = "tsx"
    HTML_TEMPLATE = "html.template"
    CSS_TEMPLATE = "css.template"
    JS_TEMPLATE = "js.template"
    TS_TEMPLATE = "ts.template"
    PY_TEMPLATE = "py.template"
    JSX_TEMPLATE = "jsx.template"
    TSX_TEMPLATE = "tsx.template"


__all__ = [
    "SupportedOutput",
    "Output",
    "Data",
    "pd",
    "dataclass",
]
