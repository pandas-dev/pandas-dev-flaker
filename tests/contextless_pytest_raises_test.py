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
            "with pytest.raises(ValueError, match=None): pass",
            id="non-builtin exec",
        ),
    ),
)
def test_noop(source):
    assert not results(source)


@pytest.mark.parametrize(
    "source, expected",
    (
        pytest.param(
            "import pytest\n" "pytest.raises(ValueError, match=None)",
            "2:0: PDF005 'pytest.raises' used outside of context manager",
            id="builtin exec",
        ),
        pytest.param(
            "from pytest import raises\n" "raises(ValueError, match=None)",
            "2:0: PDF005 'pytest.raises' used outside of context manager",
            id="builtin exec",
        ),
    ),
)
def test_violation(source, expected):
    (result,) = results(source)
    assert result == expected
