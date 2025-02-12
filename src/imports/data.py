"""
Data related imports.
"""

from .typing import *
import pandas as pd

Data: TypeAlias = Union[pd.DataFrame, pd.Series]

__all__ = [
    "Data",
    "pd",
]
