import sys
import time
import csv
import os
from index_calculus import index_calculus

def save_to_csv(alpha, beta, p, x, runtime, problem_type, order_prime_number, filename="index_calculus_batch_results.csv"):
    file_exists = os.path.isfile(filename)
    with open(filename, mode="a", newline="") as file:
        writer = csv.writer(file)
        if not file_exists:
            writer.writerow([
                "problem_type", "order_prime_number", "alpha", "beta",
                "p", "result_x", "time_seconds"
            ])
        writer.writerow([
            problem_type, order_prime_number, alpha, beta,
            p, x if x is not None else "timeout", runtime
        ])

if __name__ == "__main__":
    if len(sys.argv) != 6:
        print("Usage: python index_calculus_manual_test.py <problem_type> <order_prime_number> <alpha> <beta> <p>")
        sys.exit(1)

    problem_type = int(sys.argv[1])
    order_prime_number = int(sys.argv[2])
    alpha = int(sys.argv[3])
    beta = int(sys.argv[4])
    p = int(sys.argv[5])

    try:
        start = time.time()
        x = index_calculus(alpha, beta, p - 1, p)
        end = time.time()
        elapsed = end - start

        if x is not None:
            print(f"x = {x}, перевірка: {alpha}^{x} ≡ {pow(alpha, x, p)} ≡ {beta} mod {p}")
            print(f"Час виконання: {elapsed:.6f} секунд")
        else:
            print("Розв’язок не знайдено")

        save_to_csv(alpha, beta, p, x, elapsed, problem_type, order_prime_number)

    except Exception as e:
        print(f"Помилка: {e}")