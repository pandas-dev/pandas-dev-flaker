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
            "import foo\nfoo.remove",
            id="foo.remove",
        ),
    ),
)
def test_noop(source):
    assert not results(source)


@pytest.mark.parametrize(
    "source, expected",
    (
        pytest.param(
            "import os\nos.remove('foo')",
            "2:0: PDF019 found 'os.remove' (use 'tm.ensure_clean' instead)",
            id="os.remove call",
        ),
        pytest.param(
            "from os import remove\nremove('foo')",
            "2:0: PDF019 found 'os.remove' (use 'tm.ensure_clean' instead)",
            id="pytest.xfail used",
        ),
    ),
)
def test_violation(source, expected):
    (result,) = results(source)
    assert result == expected
