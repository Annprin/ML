from typing import List


def hello(name: str) -> str:
    if name:
        return f"Hello, {name}!"
    else:
        return "hello!"


def int_to_roman(num: int) -> str:
    a = ['I', '', 'V', 'X', 'L', 'C', 'D', 'M']
    arab = ''
    k = 1
    while num:
        ost = num % 10
        i = ost % 5
        v = ost / 5
        k1 = k + v
        if i == 4:
            arab = a[0] + a[k1] + arab
        else: 
            arab = arab + i * a[0]
        num /= 10
        k += 2
    return arab


def longest_common_prefix(strs_input: List[str]) -> str:
    pass


def primes() -> int:
    yield


class BankCard:
    def __init__(self, total_sum: int, balance_limit: int):
        pass

