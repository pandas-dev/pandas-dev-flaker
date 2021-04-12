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
            "from pandas.core import common as com",
            id="from import, correct alias used",
        ),
        pytest.param(
            "import pandas.core.common as com",
            id="import, correct alias used",
        ),
    ),
)
def test_noop(source):
    assert not results(source)


@pytest.mark.parametrize(
    "source, expected",
    (
        pytest.param(
            "import pandas.core.common",
            "1:0: PDF009 'common' imported from 'pandas.core' without "
            "'com' alias",
            id="import, no alias",
        ),
        pytest.param(
            "from pandas.core import common",
            "1:0: PDF009 'common' imported from 'pandas.core' without "
            "'com' alias",
            id="from import, no alias",
        ),
        pytest.param(
            "from pandas.core.common import foo",
            "1:0: PDF009 'common' imported from 'pandas.core' without "
            "'com' alias",
            id="import from pandas.core.common",
        ),
    ),
)
def test_violation(source, expected):
    (result,) = results(source)
    assert result == expected
