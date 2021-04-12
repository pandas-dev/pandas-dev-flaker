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
            "mock = 3",
            id="Assign to mock",
        ),
    ),
)
def test_noop(source):
    assert not results(source)


@pytest.mark.parametrize(
    "source, expected",
    (
        pytest.param(
            "mock = unittest.mock",
            "1:7: PDF016 found 'unittest.mock' "
            "(use 'pytest.monkeypatch' instead)",
            id="unittest.mock",
        ),
        pytest.param(
            "from unittest.mock.foo import bar",
            "1:0: PDF016 found 'unittest.mock' "
            "(use 'pytest.monkeypatch' instead)",
            id="import from unittest.mock",
        ),
        pytest.param(
            "from unittest import mock",
            "1:0: PDF016 found 'unittest.mock' "
            "(use 'pytest.monkeypatch' instead)",
            id="mock imported from unittest",
        ),
    ),
)
def test_violation(source, expected):
    (result,) = results(source)
    assert result == expected
