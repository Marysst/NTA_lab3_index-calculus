import random
import math
import time
from typing import List, Dict, Optional
import multiprocessing as mp
import psutil


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

def worker(alpha: int, p: int, n: int, factor_base: List[int]) -> Optional[tuple[List[int], int]]:
    k = random.randint(0, n - 1)
    val = pow(alpha, k, p)
    factorization = trial_factorization(val, factor_base)
    if factorization:
        row = [factorization.get(p_, 0) % n for p_ in factor_base]
        return (row, k % n)
    return None

def index_calculus_parallel(alpha: int, beta: int, n: int, p: int, queue_size: int, num_processes: int = 2, c: float = 3.38, extra_equations: int = 30) -> Optional[int]:
    B = calculate_factor_base_bound(n, c)
    factor_base = generate_factor_base(B)
    t = len(factor_base)

    A, b = [], []
    needed = t + extra_equations
    with mp.Pool(processes=num_processes) as pool:
        while len(A) < needed:
            tasks = [pool.apply_async(worker, args=(alpha, p, n, factor_base)) for _ in range(queue_size)]
            for task in tasks:
                result = task.get()
                if result:
                    row, k_mod = result
                    A.append(row)
                    b.append(k_mod)
                if len(A) >= needed:
                    break

    logs = gaussian_elimination_mod(A, b, n)
    if logs is None:
        return None

    for attempt in range(1000):  # збільшено кількість спроб
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

    return None


def main():
    p = 9583882907
    alpha = 228791781
    beta = 1973175995
    n = p - 1

    best_time = [None, None]
    best_cpu = [None, None]
    N = 20

    for queue_size in [2, 3]:
        total_time = 0
        total_cpu_change = 0
        for run in range(N):
            cpu_before = psutil.cpu_percent(interval=None)
            start = time.time()
            x = index_calculus_parallel(alpha, beta, n, p, queue_size)
            end = time.time()
            cpu_after = psutil.cpu_percent(interval=None)
            cpu = cpu_after - cpu_before
            total_cpu_change += cpu

            duration = end - start
            total_time += duration

        avg_time = total_time / N
        avg_cpu_change = total_cpu_change / N
        print(f"\nСередній час для {queue_size} задач: {avg_time:.4f} с")
        print(f"Середня зміна CPU для {queue_size} задач: {avg_cpu_change:+.1f}%")

        if best_time[0] is None or best_time[1] > avg_time:
            best_time = [queue_size, avg_time]

        if best_cpu[0] is None or best_cpu[1] > avg_cpu_change:
            best_cpu = [queue_size, avg_cpu_change]

    print(f"\n>>> Найкращий час: {best_time[1]:.4f} с при {best_time[0]} задачах у черзі")
    print(f">>> Найменше навантаження CPU: {best_cpu[1]:+.1f}% при {best_cpu[0]} задачах у черзі")


if __name__ == "__main__":
    main()
