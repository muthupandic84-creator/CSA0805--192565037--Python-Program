"""Q7: Redesign Q6 – replace repeated recursive work with an iterative pair."""
import time

def original_naive(n):
    if n <= 1:
        return 1
    return original_naive(n - 1) + original_naive(n - 2)

def redesigned_loop(n):
    if n <= 1:
        return 1
    previous, current = 1, 1
    for _ in range(2, n + 1):
        previous, current = current, previous + current
    return current

def timed(fn, n):
    start = time.perf_counter()
    result = fn(n)
    return result, time.perf_counter() - start

def main():
    print("Q7 redesign: naive recursive stair count -> iterative two-value update")
    print("Objective: preserve the answer while reducing repeated calls and stack use.")
    for n in (10, 20, 25, 30):
        old_value, old_time = timed(original_naive, n)
        new_value, new_time = timed(redesigned_loop, n)
        print(f"n={n:2}: same={old_value == new_value}, "
              f"naive={old_time:.6f}s, loop={new_time:.6f}s")
    value, elapsed = timed(redesigned_loop, 1000)
    print(f"n=1000: result has {len(str(value))} digits; loop time={elapsed:.6f}s")
    print("Trade-off: iterative version is less directly recursive but uses O(1) extra space.")

if __name__ == "__main__":
    main()
