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
            "import foo\nfoo.random",
            id="foo.random",
        ),
        pytest.param(
            "from foo import random",
            id="foo.random",
        ),
        pytest.param(
            "import numpy as np\nnp.random.randn(3)",
            id="pytest.xfail used",
        ),
        pytest.param(
            "import numpy.random",
            id="pytest.xfail used",
        ),
    ),
)
def test_noop(source):
    assert not results(source)


@pytest.mark.parametrize(
    "source, expected",
    (
        pytest.param(
            "from numpy.random.foo import bar",
            "1:0: PDF020 found import from numpy.random",
            id="os.remove call",
        ),
        pytest.param(
            "from numpy.random import foo",
            "1:0: PDF020 found import from numpy.random",
            id="os.remove call",
        ),
        pytest.param(
            "from numpy import random",
            "1:0: PDF020 found import from numpy.random",
            id="os.remove call",
        ),
    ),
)
def test_violation(source, expected):
    (result,) = results(source)
    assert result == expected
