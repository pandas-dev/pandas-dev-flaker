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
            "ab = 3",
            id="Multi-letter assignment",
        ),
    ),
)
def test_noop(source):
    assert not results(source)


@pytest.mark.parametrize(
    "source, expected",
    (
        pytest.param(
            "a = 3",
            "1:0: PDF023 don't assign to single-letter variables",
            id="Single letter variable",
        ),
    ),
)
def test_violation(source, expected):
    (result,) = results(source)
    assert result == expected
