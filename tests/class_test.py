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
            "class Foo: ...",
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
            "foo.__class__()",
            "1:0: PDF008 'foo.__class__' used, (use 'type(foo)' instead)",
            id="builtin exec",
        ),
    ),
)
def test_violation(source, expected):
    (result,) = results(source)
    assert result == expected
