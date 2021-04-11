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
            "import pytest\n" "@pytest.mark.xfail\n" "def testme(): ...",
            id="pytest.mark.xfail used",
        ),
    ),
)
def test_noop(source):
    assert not results(source)


@pytest.mark.parametrize(
    "source, expected",
    (
        pytest.param(
            "from pytest import xfail\n",
            "1:0: PDF015 found pytest.xfail (use pytest.mark.xfail instead)",
            id="xfail used, imported from pytest",
        ),
        pytest.param(
            "import pytest\n" "@pytest.xfail\n" "def testme(): ...",
            "2:1: PDF015 found pytest.xfail (use pytest.mark.xfail instead)",
            id="pytest.xfail used",
        ),
    ),
)
def test_violation(source, expected):
    (result,) = results(source)
    assert result == expected
