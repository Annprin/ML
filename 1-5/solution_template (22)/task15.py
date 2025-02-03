from typing import List


def hello(name: str = "") -> str:
    if name:
        return f"Hello, {name}!"
    else:
        return "Hello!"


def int_to_roman(num: int) -> str:
    a = ['I', 'V', 'X', 'L', 'C', 'D', 'M']
    arab = ''
    k = 0
    while num:
        ost = num % 10
        i = ost % 5
        v = ost // 5
        if i == 4:
            arab = a[k] + a[k + 1 + v] + arab
        else: 
            s = a[k + 1] if v else ""
            arab = s + i * a[k] + arab
        num //= 10
        k += 2
    return arab


def longest_common_prefix(strs_input: List[str]) -> str:
    ans = ""
    if strs_input:
        example = strs_input[0].strip()
        max_len = len(example)
        for s in strs_input[1:]:
            s1 = s.strip()
            l = 0
            for i in range(max_len):
                if len(s1) <= i or example[i] != s1[i]:
                    break
                l += 1
            max_len = l
        ans = example[:max_len]
    return ans
            


def primes() -> int:
    k = 2
    while True:
        for i in range(2, int(k ** 0.5) + 1):
            if not (k % i):
                k += 1
                break
        else:
            yield k
            k += 1


class BankCard:
    def __init__(self, total_sum: int, balance_limit: int = None):
        self.total_sum = total_sum
        self.balance_limit = balance_limit

    def __call__(self, sum_spent: int):
        if sum_spent > self.total_sum:
            print(f"Not enough money to spend {sum_spent} dollars.")
            raise ValueError
        self.total_sum -= sum_spent

    def put(self, sum_put):
        self.total_sum += sum_put
        print(f"You put {sum_put} dollars.")

    def __add__(self, b):
        balance = 0
        if self.balance_limit and b.balance_limit:
            balance = self.balance_limit if self.balance_limit > b.balance_limit else b.balance_limit
        elif self.balance_limit:
            balance = self.balance_limit
        else:
            balance = b.balance_limit
        return BankCard(self.total_sum + b.total_sum, balance)
    
    def __str__(self):
        return "To learn the balance call balance."
    
    @property
    def balance(self):
        if self.balance_limit is None:
            return self.total_sum
        if not self.balance_limit:
            print("Balance check limits exceeded.")
            raise ValueError
        self.balance_limit -= 1
        return self.total_sum
