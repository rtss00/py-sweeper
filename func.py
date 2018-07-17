import math
import random

__name__ = 'func'


def random_in_range(start: int, end: int, amount: int) -> list:
    ret = []
    if amount > end - start:
        amount %= end - start
    while amount != 0:
        candidate = random.randint(start, end)
        if candidate not in ret:
            ret.append(candidate)
            amount -= 1
    return ret


