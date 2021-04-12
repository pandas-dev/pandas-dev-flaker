import ast
import tokenize
from io import StringIO

import pytest

from pandas_dev_flaker.__main__ import run


def results(s):
    return {
        "{}:{}: {}".format(*r)
        for r in run(
            ast.parse(s),
            list(tokenize.generate_tokens(StringIO(s).readline)),
        )
    }


@pytest.mark.parametrize(
    "source",
    (
        pytest.param(
            "from pandas import _testing as tm",
            id="imported _testing as tm",
        ),
        pytest.param(
            "import pandas._testing as tm",
            id="imported pandas._testing as tm",
        ),
    ),
)
def test_noop(source):
    assert not results(source)


@pytest.mark.parametrize(
    "source, expected",
    (
        pytest.param(
            "from pandas._testing import foo",
            "1:0: PDF017 found import from 'pandas._testing' "
            "(use 'import pandas._testing as tm')",
            id="import from _testing",
        ),
        pytest.param(
            "from pandas import _testing",
            "1:0: PDF017 found import from 'pandas._testing' "
            "(use 'import pandas._testing as tm')",
            id="imported _testing from pandas",
        ),
        pytest.param(
            "import pandas._testing",
            "1:0: PDF017 found import from 'pandas._testing' "
            "(use 'import pandas._testing as tm')",
            id="imported pandas._testing",
        ),
    ),
)
def test_violation(source, expected):
    (result,) = results(source)
    assert result == expected
