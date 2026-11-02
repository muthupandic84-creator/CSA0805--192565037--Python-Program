"""Q1: Daily rainfall records - lists, slicing and moving averages."""
import random
import time

WINDOW = 7

def weekly_totals(readings):
    return [sum(readings[i:i + 7]) for i in range(0, len(readings) - 6, 7)]

def extremes(readings):
    if not readings:
        return None, None
    max_value = max(readings)
    min_value = min(readings)
    return (max_value, readings.index(max_value)), (min_value, readings.index(min_value))

def moving_average_naive(readings, window=WINDOW):
    if window <= 0:
        raise ValueError("window must be positive")
    return [sum(readings[i:i + window]) / window
            for i in range(len(readings) - window + 1)]

def moving_average_running(readings, window=WINDOW):
    if window <= 0:
        raise ValueError("window must be positive")
    if len(readings) < window:
        return []
    current = sum(readings[:window])
    result = [current / window]
    for i in range(window, len(readings)):
        current += readings[i] - readings[i - window]
        result.append(current / window)
    return result

def dry_days(readings):
    return [day + 1 for day, amount in enumerate(readings) if amount == 0]

def benchmark():
    random.seed(42)
    print("n,naive_seconds,running_seconds")
    for n in (365, 36_500, 365_000):
        data = [random.uniform(0, 80) for _ in range(n)]
        start = time.perf_counter()
        a = moving_average_naive(data)
        naive = time.perf_counter() - start
        start = time.perf_counter()
        b = moving_average_running(data)
        running = time.perf_counter() - start
        assert len(a) == len(b) and all(abs(x-y) < 1e-9 for x, y in zip(a, b))
        print(f"{n},{naive:.6f},{running:.6f}")

if __name__ == "__main__":
    rainfall = [0, 2, 5, 0, 12, 8, 4, 0, 0, 3, 7, 1, 0, 6]
    print("Weekly totals:", weekly_totals(rainfall))
    print("Maximum/minimum (value, zero-based position):", extremes(rainfall))
    print("7-day moving average:", moving_average_running(rainfall))
    print("Dry days (1-based day numbers):", dry_days(rainfall))
    print("Short input test:", moving_average_running([1, 2, 3]))
    print("Empty input test:", moving_average_running([]))
    benchmark()
