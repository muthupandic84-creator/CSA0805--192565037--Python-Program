"""Q6: Climbing stairs – naive recursion, memoisation, and loop."""
from functools import lru_cache
import sys
import time

calls = 0

def ways_naive(n):
    global calls
    calls += 1
    if n <= 1:
        return 1
    return ways_naive(n - 1) + ways_naive(n - 2)

@lru_cache(maxsize=None)
def ways_memo(n):
    global calls
    calls += 1
    if n <= 1:
        return 1
    return ways_memo(n - 1) + ways_memo(n - 2)

def ways_loop(n):
    if n <= 1:
        return 1
    previous, current = 1, 1
    for _ in range(2, n + 1):
        previous, current = current, previous + current
    return current

def main():
    global calls
    print("Hand-check values:")
    for n in range(1, 7):
        print(f"n={n}: {ways_loop(n)}")

    print("\nCall counts:")
    for n in (10, 20, 25, 30):
        calls = 0
        naive_result = ways_naive(n)
        naive_calls = calls
        ways_memo.cache_clear()
        calls = 0
        memo_result = ways_memo(n)
        memo_calls = calls
        print(f"n={n}: naive={naive_result}, calls={naive_calls}; "
              f"memo={memo_result}, calls={memo_calls}")

    print("\nFor n=1000:")
    try:
        print("memoised result:", ways_memo(1000))
    except RecursionError as error:
        print("RecursionError:", error)
        print("Current recursion limit:", sys.getrecursionlimit())
    print("Loop result for n=1000:", ways_loop(1000))
    print("The loop avoids recursion depth and uses O(1) extra space.")

if __name__ == "__main__":
    main()
