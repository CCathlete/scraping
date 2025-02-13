"""
Data related imports.
"""

from .typing import *
import pandas as pd

Data: TypeAlias = Union[pd.DataFrame, pd.Series]
Output: TypeAlias = Union[Data, None]

__all__ = [
    "Output",
    "Data",
    "pd",
]
