import pandas as pd
import matplotlib.pyplot as plt

def load_and_process(filename, label):
    df = pd.read_csv(filename)
    df = df[df["time_seconds"] != "timeout"]
    df["time_seconds"] = df["time_seconds"].astype(float)
    df["p"] = df["p"].astype(int)

    grouped = df.groupby("order_prime_number").agg({
        "p": "mean",
        "time_seconds": "mean"
    }).reset_index()

    grouped.columns = ["order_prime_number", "avg_p", f"{label}_avg_time"]
    return grouped

# Завантажуємо обидва набори даних
serial = load_and_process("index_calculus_batch_results.csv", "serial")
parallel = load_and_process("index_calculus_parallel_batch_results.csv", "parallel")

# Об'єднуємо по order_prime_number
merged = pd.merge(serial, parallel, on="order_prime_number", how="inner")

# Побудова графіка
plt.figure(figsize=(10, 6))
plt.plot(merged["order_prime_number"], merged["serial_avg_time"], label="Реалізація без розпаралелювання", marker='o')
plt.plot(merged["order_prime_number"], merged["parallel_avg_time"], label="Реалізація з розпаралелюванням", marker='s')

plt.xlabel("Порядок простого числа p")
plt.ylabel("Середній час виконання (секунди)")
plt.title("Порівняння продуктивності Index Calculus: Без розпаралелювання vs З розпаралелюванням")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()