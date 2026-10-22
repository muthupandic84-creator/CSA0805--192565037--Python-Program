"""Compare float and Decimal summation and measure elapsed time."""
from decimal import Decimal
from time import perf_counter

def measure(n):
    items = ["33.40"] * n
    start = perf_counter()
    float_total = sum(float(x) for x in items)
    float_seconds = perf_counter() - start
    start = perf_counter()
    decimal_total = sum((Decimal(x) for x in items), Decimal("0.00"))
    decimal_seconds = perf_counter() - start
    return float_total, decimal_total, float_seconds, decimal_seconds

if __name__ == "__main__":
    for n in (300, 6000, 150000):
        f, d, tf, td = measure(n)
        print(f"n={n:6} float={f:.12f} Decimal={d} difference={Decimal(str(f))-d}")
        print(f"  float_seconds={tf:.6f} decimal_seconds={td:.6f}")
