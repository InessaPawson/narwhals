import pandas as pd
import polars as pl
import pytest
from sklearn.utils import check_X_y
from sklearn.utils._testing import create_memmap_backed_data

import narwhals as nw


def test_native_vs_non_native() -> None:
    s = pd.Series([1, 2, 3])
    df = pd.DataFrame({"a": [1, 2, 3], "b": [4, 5, 6]})
    with pytest.raises(TypeError, match="Perhaps you forgot"):
        nw.from_native(df).filter(s > 1)
    s = pl.Series([1, 2, 3])
    df = pl.DataFrame({"a": [1, 2, 3], "b": [4, 5, 6]})
    with pytest.raises(TypeError, match="Perhaps you\n- forgot"):
        nw.from_native(df).filter(s > 1)


def test_validate_laziness() -> None:
    df = pl.DataFrame({"a": [1, 2, 3], "b": [4, 5, 6]})
    with pytest.raises(
        NotImplementedError,
        match=("The items to concatenate should either all be eager, or all lazy"),
    ):
        nw.concat([nw.DataFrame(df), nw.LazyFrame(df)])


def test_memmap() -> None:
    # the headache this caused me...
    x_any = pd.DataFrame({"a": [1, 2, 3], "b": [4, 5, 6]})
    y_any = create_memmap_backed_data(x_any["b"])

    x_any, y_any = create_memmap_backed_data([x_any, y_any])

    x = nw.from_native(x_any)
    x = x.with_columns(y=nw.from_native(y_any, series_only=True))

    # check this doesn't raise
    check_X_y(nw.to_native(x), nw.to_native(x["y"]))
