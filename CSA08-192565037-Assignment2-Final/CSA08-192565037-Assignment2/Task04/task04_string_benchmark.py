"""Q4: Compare +=, list+join, and f-string line construction."""
import time
import statistics

def build_plus(parts):
    text = ""
    for part in parts:
        text += part + ";"
    return text

def build_join(parts):
    return "".join(part + ";" for part in parts)

def build_fstring(records):
    return "".join(f"{item};" for item in records)

def measure(fn, data, repeats=3):
    samples = []
    result = None
    for _ in range(repeats):
        start = time.perf_counter()
        result = fn(data)
        samples.append(time.perf_counter() - start)
    return result, samples, statistics.mean(samples)

def main():
    for count in (1_000, 10_000, 200_000):
        items = [f"Item{i}:Rs{i % 50}" for i in range(count)]
        a, ta, avg_a = measure(build_plus, items)
        b, tb, avg_b = measure(build_join, items)
        c, tc, avg_c = measure(build_fstring, items)
        print(f"\nLines: {count:,} | same output: {a == b == c}")
        print(f"+=      samples={ [round(x, 6) for x in ta] } average={avg_a:.6f}s")
        print(f"join    samples={ [round(x, 6) for x in tb] } average={avg_b:.6f}s")
        print(f"f-string samples={ [round(x, 6) for x in tc] } average={avg_c:.6f}s")

if __name__ == "__main__":
    main()
