import token
import tokenize
from typing import Iterator, Sequence, Tuple

from pandas_dev_flaker._data_tokens import register

MSG = "PDF012 line split in two unnecessarily by 'black' formatter"


@register()
def foo(
    tokens: Sequence[tokenize.TokenInfo],
) -> Iterator[Tuple[int, int, str]]:
    for current_token, next_token in zip(tokens, tokens[1:]):
        if current_token.type == next_token.type == token.STRING:
            yield (*current_token.start, MSG)
