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
            "import numpy as np\nnp.object_",
            id="access from numpy as np",
        ),
        pytest.param(
            "import numpy\nnumpy.object_",
            id="access from numpy",
        ),
        pytest.param(
            "from numpy import object_",
            id="import from numpy",
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
            id="access from numpy",
        ),
        pytest.param(
            "import numpy as np\nnp.object",
            "2:0: PDF020 found 'np.bool' or 'np.object' "
            "(use 'np.bool_' or 'np.object_' instead)",
            id="access from np",
        ),
        pytest.param(
            "from numpy import object",
            "1:0: PDF020 found 'np.bool' or 'np.object' "
            "(use 'np.bool_' or 'np.object_' instead)",
            id="import from numpy",
        ),
    ),
)
def test_violation(source, expected):
    (result,) = results(source)
    assert result == expected
