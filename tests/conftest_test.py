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
            "conftest = 'foo'",
            id="assign to conftest",
        ),
    ),
)
def test_noop(source):
    assert not results(source)


@pytest.mark.parametrize(
    "source, expected",
    (
        pytest.param(
            "import conftest",
            "1:0: PDF010 import from 'conftest' found",
            id="import conftest",
        ),
        pytest.param(
            "from conftest import foo",
            "1:0: PDF010 import from 'conftest' found",
            id="import from conftest",
        ),
        pytest.param(
            "from pandas.conftest import foo",
            "1:0: PDF010 import from 'conftest' found",
            id="import from pandas.conftest",
        ),
    ),
)
def test_violation(source, expected):
    (result,) = results(source)
    assert result == expected
