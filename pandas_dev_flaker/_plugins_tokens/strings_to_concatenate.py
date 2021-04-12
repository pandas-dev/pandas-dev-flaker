"""
Taken from:

https://github.com/pandas-dev/pandas/blob/33fec602ffd476c8ca1cda8f2963e06623c51b20/scripts/validate_unwanted_patterns.py#L233-L280  # noqa: E501
"""


import tokenize
from typing import Iterator, Sequence, Tuple

from pandas_dev_flaker._data_tokens import register

MSG = "PDF007 line split in two unnecessarily by 'black' formatter"


@register()
def visit(
    tokens: Sequence[tokenize.TokenInfo],
) -> Iterator[Tuple[int, int, str]]:
    for current_token, next_token in zip(tokens, tokens[1:]):
        if current_token.type == next_token.type == tokenize.STRING:
            yield (*current_token.start, MSG)
