import time
import csv
import os
from index_calculus import index_calculus

INPUT_FILE = "dataset_created_during_the_execution_of_lab#2.csv"
OUTPUT_FILE = "index_calculus_batch_results.csv"
TIMEOUT_SECONDS = 300


def save_to_csv(problem_type, order_prime_number, alpha, beta, p, x, elapsed, filename=OUTPUT_FILE):
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
            p, x if x is not None else "timeout", elapsed
        ])


def process_row(row):
    try:
        problem_type = int(row["problem_type"])
        order_prime_number = int(row["order_prime_number"])
        alpha = int(row["alpha"])
        beta = int(row["beta"])
        p = int(row["p"])

        start_time = time.time()
        x = None

        while True:
            if time.time() - start_time > TIMEOUT_SECONDS:
                print(f"[{p}] Перевищено ліміт {TIMEOUT_SECONDS} сек.")
                break

            x = index_calculus(alpha, beta, p - 1, p)
            break

        elapsed = time.time() - start_time

        if x is not None:
            print(f"[{p}] x = {x}, перевірка: {alpha}^{x} ≡ {pow(alpha, x, p)} ≡ {beta} mod {p}")
            print(f"    Час виконання: {elapsed:.4f} сек")
        else:
            print(f"[{p}] Розв’язок не знайдено")

        save_to_csv(problem_type, order_prime_number, alpha, beta, p, x, elapsed)

    except Exception as e:
        print(f"Помилка в рядку {row}: {e}")


def main():
    with open(INPUT_FILE, newline="") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            process_row(row)


if __name__ == "__main__":
    main()