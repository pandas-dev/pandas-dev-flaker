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
            "a = 'foo' + 'bar'",
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
            "a = 'foo''bar'",
            "1:4: PDF012 line split in two unnecessarily by 'black' formatter",
            id="builtin exec",
        ),
    ),
)
def test_violation(source, expected):
    (result,) = results(source)
    assert result == expected
