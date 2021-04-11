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
            "from pandas import testing",
            "1:0: PDF018 don't import from pandas.testing",
            id="straight import",
        ),
        pytest.param(
            "from pandas.testing import foo",
            "1:0: PDF018 don't import from pandas.testing",
            id="import from pandas.testing",
        ),
        pytest.param(
            "import pandas\n" "pandas.testing.foo",
            "2:0: PDF018 don't import from pandas.testing",
            id="access from pandas.testing",
        ),
        pytest.param(
            "import pandas as pd\n" "pd.testing.foo",
            "2:0: PDF018 don't import from pandas.testing",
            id="access from pd.testing",
        ),
        pytest.param(
            "import pandas.testing",
            "1:0: PDF018 don't import from pandas.testing",
            id="import pandas.testing",
        ),
    ),
)
def test_violation(source, expected):
    (result,) = results(source)
    assert result == expected
