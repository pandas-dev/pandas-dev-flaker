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
        pytest.param(
            "_ = 3",
            id="Underscore assignment",
        ),
        pytest.param(
            "ab, cd, _ = (1, 2, 3)",
            id="Unpacking including an underscore",
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
            "1:0: PDF023 found assignment to single-letter variable",
            id="Single letter variable",
        ),
        pytest.param(
            "bar = a = 1",
            "1:6: PDF023 found assignment to single-letter variable",
            id="Multiple assignment",
        ),
        pytest.param(
            "a, bar = (3, 5)",
            "1:0: PDF023 found assignment to single-letter variable",
            id="Unpacking",
        ),
    ),
)
def test_violation(source, expected):
    (result,) = results(source)
    assert result == expected
