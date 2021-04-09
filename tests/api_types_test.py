import ast

import pytest

from pandas_dev_flaker.__main__ import Plugin


def results(s):
    return {"{}:{}: {}".format(*r) for r in Plugin(ast.parse(s)).run()}


@pytest.mark.parametrize(
    "source",
    (
        pytest.param(
            "from pandas.api.types import pandas_dtype",
            id="import from pandas.api.types",
        ),
    ),
)
def test_noop(source):
    assert not results(source)


@pytest.mark.parametrize(
    "source, expected",
    (
        pytest.param(
            "import pandas as pd\n" "pd.api.types.pandas_dtype",
            "2:0: PDF002 pd.api.types used "
            "(import from pandas.api.types instead)",
            id="pd namespace",
        ),
        pytest.param(
            "import pandas\n" "pandas.api.types.pandas_dtype",
            "2:0: PDF002 pd.api.types used "
            "(import from pandas.api.types instead)",
            id="pandas namespace",
        ),
    ),
)
def test_violation(source, expected):
    (result,) = results(source)
    assert result == expected
