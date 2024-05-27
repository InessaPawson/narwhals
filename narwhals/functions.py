from __future__ import annotations

from typing import TYPE_CHECKING
from typing import Iterable
from typing import Literal

from narwhals.utils import validate_laziness
from narwhals.utils import validate_same_library

if TYPE_CHECKING:
    from narwhals.dataframe import DataFrame
    from narwhals.dataframe import LazyFrame


def concat(
    items: Iterable[DataFrame | LazyFrame],
    *,
    how: Literal["horizontal", "vertical"] = "vertical",
) -> DataFrame | LazyFrame:
    if how not in ("horizontal", "vertical"):
        raise NotImplementedError(
            "Only horizontal and vertical concatenations are supported"
        )
    if not items:
        raise ValueError("No items to concatenate")
    items = list(items)
    validate_same_library(items)
    validate_laziness(items)
    first_item = items[0]
    plx = first_item.__narwhals_namespace__()
    return first_item.__class__(
        plx.concat([df._dataframe for df in items], how=how),
        is_polars=first_item._is_polars,
    )
    """
    Combine multiple DataFrames, LazyFrames, or Series into a single object.

    Parameters:
    items
        DataFrames, LazyFrames, or Series to concatenate.
    how : {'vertical','horizontal'}
    
        * vertical: Stacks Series from DataFrames vertically and fills with `null`
          if the lengths don't match.
        * horizontal: Stacks Series from DataFrames horizontally and fills with `null`
          if the lengths don't match.
        
    Notes:
    Only horizontal and vertical concatenations are supported.
    
    Examples: TO DO
"""
