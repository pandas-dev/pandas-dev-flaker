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
            "with pytest.raises(ValueError, match=None):\n" "    pass",
            id="match None",
        ),
        pytest.param(
            "with pytest.raises(ValueError, match='foo'):\n" "    pass",
            id="match statement present",
        ),
    ),
)
def test_noop(source):
    assert not results(source)


@pytest.mark.parametrize(
    "source, expected",
    (
        pytest.param(
            "with pytest.raises(ValueError):\n" "    pass",
            "1:5: PDF003 pytest.raises used without 'match='",
            id="no checking of error message",
        ),
    ),
)
def test_violation(source, expected):
    (result,) = results(source)
    assert result == expected
