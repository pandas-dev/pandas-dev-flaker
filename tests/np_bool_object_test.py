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
            "import numpy\nnumpy.object_",
            id="foo.random",
        ),
        pytest.param(
            "from numpy import object_",
            id="foo.random",
        ),
    ),
)
def test_noop(source):
    assert not results(source)


@pytest.mark.parametrize(
    "source, expected",
    (
        pytest.param(
            "import numpy\nnumpy.object",
            "2:0: PDF020 found 'np.bool' or 'np.object' "
            "(use 'np.bool_' or 'np.object_' instead)",
            id="os.remove call",
        ),
        pytest.param(
            "import numpy as np\nnp.object",
            "2:0: PDF020 found 'np.bool' or 'np.object' "
            "(use 'np.bool_' or 'np.object_' instead)",
            id="os.remove call",
        ),
    ),
)
def test_violation(source, expected):
    (result,) = results(source)
    assert result == expected
