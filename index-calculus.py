import random
import math
import time
from typing import List, Dict, Optional


def is_prime(n: int) -> bool:
    if n < 2:
        return False
    if n in (2, 3):
        return True
    if n % 2 == 0 or n % 3 == 0:
        return False
    sqrt_n = int(math.sqrt(n))
    i = 5
    while i <= sqrt_n:
        if n % i == 0 or n % (i + 2) == 0:
            return False
        i += 6
    return True

def generate_factor_base(B: int) -> List[int]:
    return [p for p in range(2, B + 1) if is_prime(p)]

def calculate_factor_base_bound(n: int, c: float = 3.38) -> int:
    log_n = math.log(n)
    log_log_n = math.log(log_n)
    B = c * math.exp(0.5 * math.sqrt(log_n * log_log_n))
    return int(B)

def trial_factorization(num: int, factor_base: List[int]) -> Optional[Dict[int, int]]:
    factorization = {}
    temp = num
    for p in factor_base:
        count = 0
        while temp % p == 0:
            temp //= p
            count += 1
        if count > 0:
            factorization[p] = count
    if temp == 1:
        return factorization
    return None

def mod_inverse(a: int, m: int) -> int:
    try:
        return pow(a, -1, m)
    except ValueError:
        raise ValueError(f"mod_inverse: {a} has no inverse mod {m}")

def gaussian_elimination_mod(A: List[List[int]], b: List[int], mod: int) -> Optional[List[int]]:
    n = len(A)
    m = len(A[0])
    A = [row[:] for row in A]
    b = b[:]

    for col in range(m):
        pivot_row = None
        for row in range(col, n):
            if A[row][col] % mod != 0:
                try:
                    mod_inverse(A[row][col], mod)
                    pivot_row = row
                    break
                except ValueError:
                    continue
        if pivot_row is None:
            continue
        if pivot_row != col:
            A[col], A[pivot_row] = A[pivot_row], A[col]
            b[col], b[pivot_row] = b[pivot_row], b[col]
        inv = mod_inverse(A[col][col], mod)
        for j in range(m):
            A[col][j] = (A[col][j] * inv) % mod
        b[col] = (b[col] * inv) % mod
        for row in range(n):
            if row != col and A[row][col] != 0:
                factor = A[row][col]
                for j in range(m):
                    A[row][j] = (A[row][j] - factor * A[col][j]) % mod
                b[row] = (b[row] - factor * b[col]) % mod

    solution = [0] * m
    for row in range(n):
        leading_col = next((i for i, val in enumerate(A[row]) if val != 0), None)
        if leading_col is None:
            if b[row] % mod != 0:
                return None
        else:
            solution[leading_col] = b[row] % mod
    return solution
