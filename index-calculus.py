import random
import math
import time
import sys
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

def verify_result(alpha: int, x: int, beta: int, p: int) -> bool:
    return pow(alpha, x, p) == beta % p

def index_calculus(alpha: int, beta: int, n: int, p: int, c: float = 3.38, extra_equations: int = 30) -> Optional[int]:
    B = calculate_factor_base_bound(n, c)
    factor_base = generate_factor_base(B)
    t = len(factor_base)
    print(f"Факторна база розміром {t}: {factor_base[:10]}{'...' if t > 10 else ''}")

    A, b = [], []
    needed = t + extra_equations
    while len(A) < needed:
        k = random.randint(0, n - 1)
        val = pow(alpha, k, p)
        factorization = trial_factorization(val, factor_base)
        if factorization:
            A.append([factorization.get(p_, 0) % n for p_ in factor_base])
            b.append(k % n)
            if len(A) % 10 == 0:
                print(f"Зібрано {len(A)} рівнянь")

    logs = gaussian_elimination_mod(A, b, n)
    if logs is None:
        print("Система не має розв’язку")
        return None

    print("Отримані логарифми факторної бази:")
    for p_, log in zip(factor_base, logs):
        print(f"log_{alpha}({p_}) ≡ {log} (mod {n})")

    for attempt in range(1000):  
        l = random.randint(0, n - 1)
        val = (beta * pow(alpha, l, p)) % p
        factorization = trial_factorization(val, factor_base)
        if factorization:
            result = -l
            for i, p_ in enumerate(factor_base):
                result += logs[i] * factorization.get(p_, 0)
            x = result % n
            if verify_result(alpha, x, beta, p):
                return x

    print("Не вдалося знайти коректний логарифм β")
    return None


if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python index_calculus.py <alpha> <beta> <p>")
        sys.exit(1)

    alpha = int(sys.argv[1])
    beta = int(sys.argv[2])
    p = int(sys.argv[3])
    n = p - 1

    try:
        print("=== Алгоритм Index-Calculus ===")
        print(f"p = {p}")
        print(f"α = {alpha}")
        print(f"β = {beta}")
        print(f"n = {n}\n")

        start = time.time()
        x = index_calculus(alpha, beta, n, p)
        end = time.time()

        if x is not None:
            print(f"\nЗнайдено x = {x}")
            if verify_result(alpha, x, beta, p):
                print("Перевірка успішна: α^x ≡ β (mod p)")
            else:
                print("Помилка: α^x ≢ β (mod p)")
        else:
            print("Алгоритм не знайшов розв’язку")

        print(f"\nЧас виконання: {end - start:.2f} с")

    except Exception as e:
        print(f"Помилка: {e}")