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
            "import foo\n" "foo.exec('str')",
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
            "exec('str')",
            "1:0: PDF006 builtin exec used",
            id="builtin exec",
        ),
    ),
)
def test_violation(source, expected):
    (result,) = results(source)
    assert result == expected
