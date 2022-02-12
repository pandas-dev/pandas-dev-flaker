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
            "def f(foo): pass",
            id="Function argument with no annotation ",
        ),
        pytest.param(
            "def f(foo, other: Series): pass",
            id="Function argument with one annotation ",
        ),
        pytest.param(
            "def p(foo, other: Series | DataFrame ): pass",
            id="Function argument with two annotations",
        ),
        pytest.param(
            "def p(foo, other: Series | Union[int, str] ): pass",
            id="Function argument with two annotations",
        ),
        pytest.param(
            "def q(foo, other: DataFrame | AnyArrayLike | Timestamp): pass",
            id="Function argument with three annotations" "AnyArrayLike",
        ),
        pytest.param(
            "def b(foo, other: DataFrame | Timezone | "
            "Timestamp | Timedelta): pass",
            id="Function argument with four annotations",
        ),
        pytest.param(
            "def f(a: Callable[..., T] | DataFrame | list[int]): pass",
            id="Function annotation containing Subscript type",
        ),
        pytest.param(
            "def f(a: DataFrame | list[int]) -> int | str: pass",
            id="Function return annotation containing Subscript type",
        ),
    ),
)
def test_noop(source):
    assert not results(source)


@pytest.mark.parametrize(
    "source, expected",
    (
        pytest.param(
            "def dot(foo, other: AnyArrayLike | Series): pass",
            "1:13: PDF026 found union between Series and "
            "AnyArrayLike in "
            "type hint",
            id="Series and AnyArrayLike",
        ),
        pytest.param(
            "def bar(foo, other: DataFrame | Series | AnyArrayLike): pass",
            "1:13: PDF026 found union between Series and "
            "AnyArrayLike in "
            "type hint",
            id="Series and AnyArrayLike " "and one other annotation",
        ),
        pytest.param(
            "def bar(foo, other: DataFrame | Series | "
            "AnyArrayLike | NDFrame): pass",
            "1:13: PDF026 found union between Series and "
            "AnyArrayLike in "
            "type hint",
            id="Series and AnyArrayLike " "and two other annotations",
        ),
    ),
)
def test_violation(source, expected):
    (result,) = results(source)
    assert result == expected


@pytest.mark.parametrize(
    "source",
    (
        pytest.param(
            "def f(foo) -> int | str | bool: pass",
            id="Function with multiple return type annotations",
        ),
        pytest.param(
            "def foo(bar: list[int]): pass",
            id="Function with no return type",
        ),
        pytest.param(
            "def foo(self, bar: int) -> int: pass",
            id="Function with one return type annotation",
        ),
    ),
)
def test_noop_returns(source):
    assert not results(source)


@pytest.mark.parametrize(
    "source, expected",
    (
        pytest.param(
            "def bar(foo, other: tuple[Callable[..., T]] | "
            "Series | list[int]) -> Series | AnyArrayLike | "
            "DataFrame: pass",
            "1:0: PDF026 found union between Series and "
            "AnyArrayLike in "
            "type hint",
            id="3 objects in return type",
        ),
        pytest.param(
            "def bar(foo: int, other: tuple[Callable[..., T]] | "
            "Series | list[int]) -> Series | AnyArrayLike: pass",
            "1:0: PDF026 found union between Series and "
            "AnyArrayLike in "
            "type hint",
            id="2 objects in return type",
        ),
        pytest.param(
            "def bar(foo: List[Series | AnyArrayLike]): ...",
            "1:8: PDF026 found union between Series and "
            "AnyArrayLike in "
            "type hint",
            id="List of Series or AnyArrayLike",
        ),
        pytest.param(
            "def bar(foo: List['Series' | 'AnyArrayLike' | 'int']): ...",
            "1:8: PDF026 found union between Series and "
            "AnyArrayLike in "
            "type hint",
            id="String version of Series",
        ),
    ),
)
def test_violation_returns(source, expected):
    (result,) = results(source)
    assert result == expected


@pytest.mark.parametrize(
    "source",
    (
        pytest.param(
            "foo: str = 'string variable'",
            id="Assignment with one annotation",
        ),
        pytest.param(
            "self.bar: DataFrame | Timezone = [1, 2, 3]",
            id="Assignment with multiple annotations",
        ),
        pytest.param("cls.foo = 3", id="Assignment with no annotation"),
    ),
)
def test_noop_assignment(source):
    assert not results(source)


@pytest.mark.parametrize(
    "source, expected",
    (
        pytest.param(
            "self.foo: AnyArrayLike | Timezone | Series = 2",
            "1:0: PDF026 found union between Series and "
            "AnyArrayLike in "
            "type hint",
            id="annotation with assignment",
        ),
        pytest.param(
            "foo: AnyArrayLike | Series",
            "1:0: PDF026 found union between Series and "
            "AnyArrayLike in "
            "type hint",
            id="simple annotation",
        ),
    ),
)
def test_violation_assignment(source, expected):
    (result,) = results(source)
    assert result == expected
